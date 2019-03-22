a=fopen('coordinates_brainsight.txt');
for i=1:17
x=fgetl(a);
end
LPA_bs=str2num(x(15:end))
x=fgetl(a);Nasion_bs=str2num(x(18:end))
x=fgetl(a);RPA_bs=str2num(x(15:end))
fclose('all')

a=fopen('coordinates_native.txt');
for i=1:16
x=fgetl(a);
end
LPA_native=str2num(x(15:end))
x=fgetl(a);Nasion_native=str2num(x(18:end))
x=fgetl(a);RPA_native=str2num(x(15:end))

BS=[LPA_bs; RPA_bs; Nasion_bs].';
NATIVE=[LPA_native; RPA_native; Nasion_native].';

% calculate rotation matrix:
[regParams,Bfit,ErrorStats]=absor(BS,NATIVE) % (source,target)

% how to convert from brainsight units to MNI/scanner units:
NEW = regParams.R * BS + regParams.t
R=regParams.R
t=regParams.t

fid = fopen( 'ROTMAT.txt', 'wt' );
  fprintf( fid, '%f\t%f\t%f\n', R(1,1), R(1,2), R(1,3));
  fprintf( fid, '%f\t%f\t%f\n', R(2,1), R(2,2), R(2,3));
  fprintf( fid, '%f\t%f\t%f\n', R(3,1), R(3,2), R(3,3));
  fprintf( fid, '%f\t%f\t%f\n', t(1), t(2), t(3));
fclose(fid);
