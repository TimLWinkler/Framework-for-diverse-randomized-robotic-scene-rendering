import nvisii as nv
import colorsys
import random
import os
from variables import *


# rendering the image to a file name with given width, height and samples per pixel (spp)
def render(name, width, height, spp, denoise):
    if denoise:
        nv.enable_denoiser()
    else:
        nv.disable_denoiser()
    nv.render_to_file(
        width=width,
        height=height,
        samples_per_pixel=spp,
        file_path=name + ".png"
    )
    print("\nDONE ", name)


# creating camera at given X, Y, Z and with given field of view
def createCamera(fov, eyeX, eyeY, eyeZ):
    camera = nv.entity.create(
        name='camera',
        transform=nv.transform.create('camera'),
        camera=nv.camera.create_from_fov(
            name='camera',
            field_of_view=fov,
            aspect=1
        )
    )
    nv.set_camera_entity(camera)
    camera.get_transform().look_at(
        at=[-1, 0, 0],
        up=[0, 0, 1],
        eye=[eyeX, eyeY, eyeZ]
    )


# scans how many elements (dir doesn't count) are given in the explicit directory
# and returns a list of them
def scanDir(dir, fileFlag) -> [] :
    res = []
    for path in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, path)) and fileFlag:
                res.append(path)
            elif os.path.isdir(os.path.join(dir, path)) and not fileFlag:
                res.append(path)
    return res


# setup dome image via hdr file
def setDome(hdr, cdf):
    path = "./HDRs/" + hdr
    dome = nv.texture.create_from_file("dome", path)
    nv.set_dome_light_texture(dome, enable_cdf=cdf)


# set up function to create lights and objects of given amount
# (0 means no entities will be created)
def doLightsAndObjects(lightCount, objectCount):
    print("\n-- creating lights:")
    if lightCount == None:
        rng_light = rng.choice(maxLights, size=1, replace=False)[0] + 1
        for i in range(rng_light):
            createLight(i)
    else:
        for i in range(lightCount):
            createLight(i)

    print("\n-- creating objects")
    if objectCount == None:
        rng_obj = rng.choice(maxObjects, size=1, replace=False)[0] + 3
        matArray = getMatArray(rng_obj)
        a = numpy.arange(0, 180, 180 / rng_obj, dtype=int)
        for i in range(rng_obj):
            h = a[i]
            t = rng.choice(10, size=1, replace=False)[0]
            if len(matArray) > 0:
                createObj(t, i, h, matArray.pop(0))
            else:
                createObj(t, i, h, None)
    else:
        for i in range(objectCount):
            matArray = getMatArray(objectCount)
            a = numpy.arange(0, 180, 180 / objectCount, dtype=int)
            h = a[i]
            t = rng.choice(10, size=1, replace=False)[0]
            if len(matArray) > 0:
                createObj(t, i, h, matArray.pop(0))
            else:
                createObj(t, i, h, None)


            # create robo arms
def createRoboArm():
    roboArray = scanDir("./objects/roboArm", True)
    # Left arm
    roboleft_rng = rng.choice(len(roboArray), size=1, replace=False)[0]
    path_left = "./objects/roboArm/" + roboArray[roboleft_rng]
    roboLeft = importFile(path_left, 1.5, 0, 0, 3, 0, 0, 1)
    # right arm
    roboright_rng = rng.choice(len(roboArray), size=1, replace=False)[0]
    path_right = "./objects/roboArm/" + roboArray[roboright_rng]
    roboRight = importFile(path_right, -1.5, 0, 0, 3, 0, 0, 1)


# importing an object via pathname at x, y, z with given scale
def importFile(path, x, y, z, scale, xRota, yRota, zRota) -> nv.entity:
    scene = nv.import_scene(
        file_path=path,
        position=(x, y, z),
        scale=(scale, scale, scale),
        rotation= nv.angleAxis(nv.pi() * .5, (xRota, yRota, zRota)),
        args=[] #"verbose"]
    )
    return scene


def importTable():
    tablePath = "./objects/table/table.obj"
    tableMesh = nv.mesh.create_from_file('tableMesh', tablePath)
    tableMat = setupMat("./objects/table/wood_table_worn/", "table")
    table = nv.entity.create(
        name='table',
        transform=nv.transform.create('tableTransform'),
        material=nv.material.create('tableMaterial'),
        mesh=tableMesh
    )
    table.get_transform().set_rotation((1, 1, 1, 1))
    table.get_transform().set_position((0, 2, -2.05))
    table.get_transform().set_scale((.04, .04, .04))
    table.set_material(tableMat)


# creating a floor obj
def createFloor():
    floor = nv.entity.create(
        name="floor",
        mesh=nv.mesh.create_plane("mesh_floor"),
        transform=nv.transform.create("transform_floor"),
        material=nv.material.create("material_floor")
    )
    floor.get_material().set_base_color((0.19, 0.16, 0.19))
    floor.get_material().set_metallic(0)
    floor.get_material().set_roughness(1)
    floor.get_transform().set_scale((5, 5, 1))


# main function to create a light
def createLight(index):
    nameL = "light" + str(index)
    x = rng.choice(range_x * 2, size=1, replace=False)[0] - xyOffset
    y = rng.choice(range_y * 2, size=1, replace=False)[0] - xyOffset
    z = rng.choice(range_z, size=1, replace=False)[0] - zOffset
    temperature = rng.choice(range_temperature, size=1, replace=False)[0] + 1
    intensity = rng.choice(range_intensity, size=1, replace=False)[0] + 1
    light = nv.entity.create(
        name=nameL,
        light=nv.light.create(nameL),
        transform=nv.transform.create(
            name=nameL,
            position=[x, y, z]
        )
    )
    temp = nv.light.get(nameL)
    temp.set_temperature(temperature)
    temp.set_intensity(intensity)
    # DEBUG
    if DEBUG:
        print(nameL, x, y, z, temperature, intensity)


# creates a specific light (with exact location etc.)
def createSpecLight(index, x, y, z, temperature, intensity):
    nameL = "light" + str(index)
    light = nv.entity.create(
        name=nameL,
        light=nv.light.create(nameL),
        transform=nv.transform.create(
            name=nameL,
            position=[x, y, z]
        )
    )
    temp = nv.light.get(nameL)
    temp.set_temperature(temperature)
    temp.set_intensity(intensity)
    # DEBUG
    if DEBUG:
        print(nameL, x, y, z, temperature, intensity)


# main function to create an object (splits into sub functions)
def createObj(type, index, hue, givenMat):
    (x,y) = calcRandPosition()
    (r, g, b) = colorsys.hsv_to_rgb(hue/179, 1.0, 1.0)
    if type == 0:
        createCone(index, x, y, r, g, b, givenMat)
    elif type > 0 and type <= 4:
        createSphere(index, x, y, r, g, b, givenMat)
    elif type > 4 and type <= 8:
        createBox(index, x, y, r, g, b, givenMat)
    else:
        createCylinder(index, x, y, r, g, b, givenMat)



# calculating a random position for the objects to set to
def calcRandPosition() -> (float, float):
    xObj = 300
    x = rng.choice(xObj * 2, size=1, replace=False)[0] - xObj
    y = rng.choice(xObj, size=1, replace=False)[0] + 1
    return x/100, y/100



# creating a cone for the scene
def createCone(index, x, y, r, g, b, givenMat):
    nameCo = "Obj" + str(index) + "_Cone"
    print(nameCo, x, y)
    obj = nv.entity.create(
        name=nameCo,
        mesh=nv.mesh.create_cone(nameCo, radius=.25, size=.25),
        transform=nv.transform.create(nameCo),
        material=nv.material.create(nameCo)
    )
    obj.get_transform().set_position((x, y, 0.25))
    if givenMat == None:
        obj.get_material().set_base_color((r, g, b))
        roughness = rng.choice(10, size=1, replace=False)[0]
        obj.get_material().set_roughness(roughness/10)
        # Objects can be made to be "alpha transparent", which simulates little holes in the
        # mesh that let light through. The smaller the alpha, the more little holes.
        obj.get_material().set_alpha(1.0)
    else:
        obj.set_material(givenMat)


# creating sphere
def createSphere(index, x, y, r, g, b, givenMat):
    nameSp = "Obj" + str(index) + "_Sphere"
    print(nameSp, x, y)
    obj = nv.entity.create(
        name=nameSp,
        mesh=nv.mesh.create_sphere(nameSp, radius=.25),
        transform=nv.transform.create(nameSp),
        material=nv.material.create(nameSp)
    )
    obj.get_transform().set_position((x, y, 0.25))
    if givenMat == None:
        obj.get_material().set_base_color((r, g, b))
        roughness = rng.choice(10, size=1, replace=False)[0]
        obj.get_material().set_roughness(roughness / 10)
        # Objects can be made to be "alpha transparent", which simulates little holes in the
        # mesh that let light through. The smaller the alpha, the more little holes.
        obj.get_material().set_alpha(1.0)
    else:
        obj.set_material(givenMat)


# creating cylinder
def createCylinder(index, x, y, r, g, b, givenMat):
    nameCy = "Obj" + str(index) + "_Cylinder"
    print(nameCy, x, y)
    obj = nv.entity.create(
        name=nameCy,
        mesh=nv.mesh.create_cylinder(nameCy, radius=.25, size=.25),
        transform=nv.transform.create(nameCy),
        material=nv.material.create(nameCy)
    )
    obj.get_transform().set_position((x, y, 0.25))
    if givenMat == None:
        obj.get_material().set_base_color((r, g, b))
        roughness = rng.choice(10, size=1, replace=False)[0]
        obj.get_material().set_roughness(roughness / 10)
        # Objects can be made to be "alpha transparent", which simulates little holes in the
        # mesh that let light through. The smaller the alpha, the more little holes.
        obj.get_material().set_alpha(1.0)
    else:
        obj.set_material(givenMat)


# creating box
def createBox(index, x, y, r, g, b, givenMat):
    nameBx = "Obj" + str(index) + "_Box"
    print(nameBx, x, y)
    obj = nv.entity.create(
        name=nameBx,
        mesh=nv.mesh.create_box(nameBx, size=[.25, .25, .25]),
        transform=nv.transform.create(nameBx),
        material=nv.material.create(nameBx)
    )
    obj.get_transform().set_position((x, y, 0.25))
    if givenMat == None:
        obj.get_material().set_base_color((r, g, b))
        roughness = rng.choice(10, size=1, replace=False)[0]
        obj.get_material().set_roughness(roughness / 10)
        # Objects can be made to be "alpha transparent", which simulates little holes in the
        # mesh that let light through. The smaller the alpha, the more little holes.
        obj.get_material().set_alpha(1.0)
    else:
        obj.set_material(givenMat)


# returns an array of nv.materials to use directly
def getMatArray(maxCount) -> []:
    res = []
    matArray = scanDir("./materials", False)
    random.shuffle(matArray)
    if DEBUG:
        print("\nget material at:")
    i = 0
    for item in matArray:
        tempPath = "./materials/" + item + "/"
        if DEBUG:
            print(tempPath)
        res.append(setupMat(tempPath, item))
        i = i+1
        if i >= maxCount:
            break
    random.shuffle(res)
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