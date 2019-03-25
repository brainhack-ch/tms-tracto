import numpy as np
import nibabel as nib
import vtk
import dipy
import dipy.tracking._utils
from dipy.tracking import utils
import scipy.ndimage.morphology

from fury import window, actor

input_tck_filename = "data/sub-TiMeS_WP12_010_ses-G1_acq-1_dwi_mrtrix_iFOD2_500000.tck"
anat_filename = "data/sub-TiMeS_WP12_010_ses-G1_T1w_dwi.nii.gz"

handknob_left = nib.load("data/handknob_left.nii.gz")
handknob_right = nib.load("data/handknob_right.nii.gz")
anat = nib.load(anat_filename)

tck = nib.streamlines.load(input_tck_filename)
streamlines = tck.streamlines
endpoints = [sl[0::len(sl)-1] for sl in tck.streamlines]

lin_T, offset = dipy.tracking.utils._mapping_to_voxel(anat.affine, None)
endpoints = dipy.tracking.utils._to_voxel_coordinates(endpoints, lin_T, offset)

# get labels for label_volume
i, j, k = endpoints.T
endlabels = scipy.ndimage.morphology.binary_dilation(handknob_right.get_data(),
                                                     iterations=4)[i, j, k]

streamlines = tck.streamlines[np.logical_or(endlabels[0,:]==1, endlabels[1,:]==1)]
endpoints = [sl[0::len(sl)-1] for sl in streamlines]
endpoints = dipy.tracking.utils._to_voxel_coordinates(endpoints, lin_T, offset)
i, j, k = endpoints.T


pts = np.loadtxt("data/points.txt")

class UpdateStreamlineTimerCallback():
    def __init__(self, renderer, pts):
        self.iterations = 0
        self.renderer = renderer
        self.pts = pts

    def execute(self, iren, event):
        renderer.RemoveAllViewProps()

        # streamlines

        #current_location = pts[self.iterations]  # change this to read in real time
        current_location = np.loadtxt("data/update_pts.txt")
        mask = np.zeros(handknob_left.shape)
        location = tuple(dipy.tracking._utils._to_voxel_coordinates([current_location], lin_T, offset)[0])
        mask[location]=1
        ##size of the mask
        mask = scipy.ndimage.morphology.binary_dilation(mask, iterations=15)
        endlabels = mask[i, j, k]

        idx = np.logical_or(endlabels[0,:]==1, endlabels[1,:]==1)
        if np.sum(idx)>0:
            active_stream = streamlines[idx]
            stream_actor = actor.line(active_stream)
            renderer.add(stream_actor)

        # Stimulation Location
        roiActor = actor.contour_from_roi(mask,
                                          affine=handknob_right.affine,
                                          color=np.array([1, 1, 1]),
                                          opacity=0.5)
        renderer.AddActor(roiActor)

        # ROI
        roiActor = actor.contour_from_roi(handknob_left.get_data(),
                                          affine=handknob_left.affine,
                                          color=np.array([1, 0, 0]),
                                          opacity=0.5)
        renderer.AddActor(roiActor)
        roiActor = actor.contour_from_roi(handknob_right.get_data(),
                                          affine=handknob_right.affine,
                                          color=np.array([0, 0, 1]),
                                          opacity=0.5)
        renderer.AddActor(roiActor)

        #stream_actor = actor.line([streamlines[self.iterations]])
        #self.renderer.add(stream_actor)
        iren.GetRenderWindow().Render()
        if self.iterations < len(self.pts)-1:
            self.iterations += 1

showManager = window.ShowManager()

# Renderer
renderer = showManager.scene


## inital view

# streamlines
stream_actor = actor.line(streamlines)
renderer.add(stream_actor)

# ROI
roiActor = actor.contour_from_roi(handknob_left.get_data(),
                                  affine=handknob_left.affine,
                                  color=np.array([1, 0, 0]),
                                  opacity=0.5)
renderer.AddActor(roiActor)
roiActor = actor.contour_from_roi(handknob_right.get_data(),
                                  affine=handknob_right.affine,
                                  color=np.array([0, 0, 1]),
                                  opacity=0.5)
renderer.AddActor(roiActor)

# Render Window
renderWindow = showManager.window
renderWindow.AddRenderer(renderer)

# Interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.Initialize()#

# Initialize a timer for the animation
updateStreamlineTimerCallback = UpdateStreamlineTimerCallback(renderer, pts)

##COMMENT this line below to stop updating
renderWindowInteractor.AddObserver('TimerEvent', updateStreamlineTimerCallback.execute)
timerId = renderWindowInteractor.CreateRepeatingTimer(150) #ms
UpdateStreamlineTimerCallback.timerId = timerId


# Begin Interaction
showManager.initialize()


renderWindowInteractor.Start()
