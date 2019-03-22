import numpy as np
import nibabel as nib
import vtk

import dipy.viz
from fury.window import ShowManager
import fury

input_tck_filename = "data/sub-TiMeS_WP12_010_ses-G1_acq-1_dwi_mrtrix_iFOD2_500000.tck"
anat_filename = "data/sub-TiMeS_WP12_010_ses-G1_T1w_dwi.nii.gz"

tck = nib.streamlines.load(input_tck_filename)
streamlines = tck.streamlines[:5000]
#anat = nib.load(anat_filename)

handknob_left = nib.load("data/handknob_left.nii.gz")
handknob_right = nib.load("data/handknob_right.nii.gz")

pts = [[-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63], [-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63],[-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63], [-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63],[-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63], [-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63],[-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63], [-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63],[-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63], [-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63],[-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63], [-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63],[-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63], [-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63],[-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63], [-40, -12, 63],[-40, -12, 63],[-30, -12, 63],[-35, -12, 63]]

class UpdateStreamlineTimerCallback():
    def __init__(self, renderer, pts):
        self.iterations = 0
        self.renderer = renderer
        self.pts = pts

    def execute(self, iren, event):
        renderer.RemoveAllViewProps()
        # Stimulation Location
        source = vtk.vtkSphereSource()
        source.SetCenter(pts[self.iterations])
        source.SetRadius(20.0)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        actor = vtk.vtkActor()
        actor.GetProperty().SetColor(1, 1, 1)
        actor.GetProperty().SetOpacity(0.5)
        actor.SetMapper(mapper)
        renderer.AddActor(actor)
        # streamlines

        stream_actor = fury.actor.line(streamlines[1000:5000])
        renderer.add(stream_actor)

        # ROI
        actor = fury.actor.contour_from_roi(handknob_left.get_data(),
                                            affine=handknob_left.affine,
                                            color=np.array([1, 0, 0]),
                                            opacity=0.5)
        renderer.AddActor(actor)
        actor = fury.actor.contour_from_roi(handknob_right.get_data(),
                                            affine=handknob_right.affine,
                                            color=np.array([0, 0, 1]),
                                            opacity=0.5)
        renderer.AddActor(actor)

        #stream_actor = actor.line([streamlines[self.iterations]])
        #self.renderer.add(stream_actor)
        iren.GetRenderWindow().Render()
        if self.iterations < len(self.pts)-1:
            self.iterations += 1

showManager = ShowManager()

# Renderer
renderer = showManager.scene


## inital view
source = vtk.vtkSphereSource()
source.SetCenter(pts[0])
source.SetRadius(20.0)
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())
actor = vtk.vtkActor()
actor.GetProperty().SetColor(1, 1, 1)
actor.GetProperty().SetOpacity(0.5)
actor.SetMapper(mapper)
renderer.AddActor(actor)
# streamlines

stream_actor = fury.actor.line(streamlines[1000:5000])
renderer.add(stream_actor)

# ROI
actor = fury.actor.contour_from_roi(handknob_left.get_data(),
                                    affine=handknob_left.affine,
                                    color=np.array([1, 0, 0]),
                                    opacity=0.5)
renderer.AddActor(actor)
actor = fury.actor.contour_from_roi(handknob_right.get_data(),
                                    affine=handknob_right.affine,
                                    color=np.array([0, 0, 1]),
                                    opacity=0.5)
renderer.AddActor(actor)

# Render Window
renderWindow = showManager.window
renderWindow.AddRenderer(renderer)

# Interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.Initialize()#

# Initialize a timer for the animation
updateStreamlineTimerCallback = UpdateStreamlineTimerCallback(renderer, pts)
renderWindowInteractor.AddObserver('TimerEvent',
                                   updateStreamlineTimerCallback.execute)
timerId = renderWindowInteractor.CreateRepeatingTimer(300) #ms
UpdateStreamlineTimerCallback.timerId = timerId


# Begin Interaction
showManager.initialize()
renderWindowInteractor.Start()
