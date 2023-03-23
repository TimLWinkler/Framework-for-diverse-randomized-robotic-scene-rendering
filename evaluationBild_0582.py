import nvisii

from helperFunctions import *


def evalBild():
    createCustomeCamera(0.78, 1, 0, 2, -8, 10, 2.5)
    importTable()
    path_left = "./objects/roboArm/p0.ply"
    roboLeft = importFile(path_left, 1.5, 0, 0, 3, 0, 0, 1)
    path_right = "./objects/roboArm/p0.ply"
    roboRight = importFile(path_right, -1.5, 0, 0, 3, 0, 0, 1)

    nameRender = "render_0582"
    render(nameRender, renWidth, renHeight, renSamples, denoiseFlag)



# creating camera at given X, Y, Z and with given field of view
def createCustomeCamera(fov, atX, atY, atZ, eyeX, eyeY, eyeZ):
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
        at=[atX, atY, atZ],
        up=[0, 0, 1],
        eye=[eyeX, eyeY, eyeZ]
    )



nv.initialize(headless=True)
evalBild()

nv.deinitialize()