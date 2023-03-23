import nvisii
import torch
from fid_score.fid_score import FidScore
from helperFunctions import *


# returns an array of nv.materials to use directly
def getMatArray() -> []:
    res = []
    matArray = scanDir("./materials", False)
    if DEBUG:
        print("get material at:")
    for item in matArray:
        tempPath = "./materials/" + item + "/"
        if DEBUG:
            print(tempPath)
        res.append(setupMat(tempPath, item))

    return res


# sets up a material for the given path (see materials for examples of files)
def setupMat(path, item) -> nv.material:
    tex_ao = nv.texture.create_from_file(item + "_tex_ao", path+"ao.png")
    tex_rough = nv.texture.create_from_file(item + "_tex_rou", path+"rough.png")
    tex_normal = nv.texture.create_from_file(item + "_tex_nor", path+"nor_gl.png")

    temp_mat = nv.material.create(item + '_temp_mat')
    temp_mat.set_ior_texture(tex_ao)
    temp_mat.set_roughness_texture(tex_rough)
    temp_mat.set_normal_map_texture(tex_normal)

    tempArr = scanDir(path, True)
    if "diff.png" in tempArr:
        tex_diff = nv.texture.create_from_file(item + "_tex_dif", path + "diff.png")
        temp_mat.set_subsurface_texture(tex_diff)
        temp_mat.set_base_color_texture(tex_diff)
    if "color.png" in tempArr:
        tex_col = nv.texture.create_from_file(item + "_tex_col", path+"color.png")
        temp_mat. set_base_color_texture(tex_col)
    if "spec.png" in tempArr:
        tex_spec = nv.texture.create_from_file(item + "_tex_spec", path+"spec.png")
        temp_mat.set_specular_texture(tex_spec)

    # displacement not working properly with light rendering, so I disabled it
    #if "disp.png" in tempArr:
    #    tex_disp = nv.texture.create_from_file(item + "_tex_disp", path+"disp.png")
    #    tex_multi_nor_disp = nv.texture.create_multiply(item + "_tex_multi", tex_normal, tex_disp)
    #    temp_mat.set_normal_map_texture(tex_multi_nor_disp)

    return temp_mat


def thisIsIt():
    sphere = nv.entity.create(name="sphere")
    sphere.set_mesh(
        nv.mesh.create_sphere(
            name='sphere',
            radius=.2
        )
    )
    sphere.set_transform(
        nv.transform.create('sphere')
    )
    sphere.set_material(
        nv.material.create('sphere')
    )
    sphere_material = nv.material.get('sphere')
    sphere_material.set_base_color([1, 0, 0])



def thisIsIt2():
    tablePath = "./objects/table/table.obj"
    tableMesh = nvisii.mesh.create_from_file('tableMesh', tablePath)
    #tableMat = setupMat("./objects/table/wood_table_worn/", "table")
    tableMat = nv.material.create("testMat")
    table = nv.entity.create(
        name='table',
        transform=nv.transform.create('tableTransform'),
        material=nv.material.create('tableMaterial'),
        mesh=tableMesh
    )
    table.get_transform().set_rotation((1, 1, 1, 1))
    table.get_transform().set_position((0,0, -2.15))
    table.get_transform().set_scale((.04, .04, .04))
    tableMat.set_base_color_texture(nv.texture.create_from_file("test_tex_dif", "./objects/table/textures/diff.png"))
    table.set_material(tableMat)
    thisIsIt()
    thisIsIt3()


def thisIsIt3():
    scene = nv.import_scene(
        file_path="./objects/roboArm/p0.ply",
        position=(0, -1, 0),
        scale=(1, 1, 1),
        rotation=nv.angleAxis(nv.pi() * .5, (0, 0, 1)),
        args=["verbose"]
    )
    for i_s, s in enumerate(scene.entities):
        print(str(i_s) + ", " + str(s))
        mat = nv.material.create("leftMat")
        mat.set_base_color([0,1,0])
        s.set_material(mat)


#def calcScore():
#    fid = FidScore(("./compareRenders/render0/", "./compareRenders/render1/"), torch.device('cuda:0'), 1)
#    score = fid.calculate_fid_score()
#    fid = FidScore(("./compareRenders/renderBright/", "./compareRenders/renderDark/"), torch.device('cuda:0'), 1)
#    score1 = fid.calculate_fid_score()

#    print("FID-Score between render0 and render1: ", score)
#    print("FID-Score between render_bright and render_dark: ", score1)


nv.initialize(headless=True)
hdrArray = scanDir("./HDRs", True)
matArray = scanDir("./materials", False)
createCamera(0.78, -2.1, 2.1, 2.5)
setDome(hdrArray[4], False)
thisIsIt2()
createSpecLight(0, 2, 4, 5, range_temperature, range_intensity / 3)
nv.configure_denoiser(use_kernel_prediction=True)
render("Test", renWidth, renHeight, 128, denoiseFlag)

nv.deinitialize()

#calcScore()