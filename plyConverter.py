import trimesh

def convertPlyToStl(fileName):
    mesh = trimesh.load_mesh("{}.ply".format(fileName))
    mesh.export(file_obj="{}.stl".format(fileName), file_type="stl_ascii")
