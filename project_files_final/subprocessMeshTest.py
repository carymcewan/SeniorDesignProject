import subprocess
import os

command = "echo DOG"
command = "meshlabserver -i scan.ply -o mesh.stl -s script.mlx"

# p = subprocess.call(["meshlabserver", "-i scan.ply -o mesh.stl -s script.mlx"], stdout=subprocess.PIPE)
# os.system("meshlabserver -i scan.ply -o mesh.stl -s script.mlx")
# while p == None:
#     print("Damn! Still running")

process = subprocess.Popen("meshlabserver -i scan.ply -o mesh.stl -s script.mlx"command, shell=True, stdout=subprocess.PIPE)
process.wait()
print(process.returncode)
# print(process.communicate())
print("COMPLETE")