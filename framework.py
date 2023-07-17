import nvisii as nv
import numpy.random

from helperFunctions import *
import variables
from evaluation import *
from inputHandler import *


# position check (clipping) but its not in focus for the project

def main(sceneIndex):
    nv.clear_all()
    print("\n\n...building the scene ", str(sceneIndex) + "...")

    # -------- camera (FOV, x, y, z) --------
    createCamera(0.78, 6, 9, 3)

    # -------- Set the sky/dome --------
    if HDRIs:
        setDome(hdrArray[sceneIndex % len(hdrArray)], True)
    else:
        setDomeSky()

    # -------- table --------
    importTable()

    # -------- robo arm --------
    createRoboArm()

    # -------- lights and objects --------
    doLightsAndObjects(None, None)

    # -------- rendering --------
    print("\n...start rendering...")
    name_render = "renders/render" + str(sceneIndex)
    render(name_render, renWidth, renHeight, variables.renSamples, variables.denoiseFlag)


# render dark image
def darkImage():
    nv.clear_all()
    print("\n\n...building dark image--")

    # -------- camera --------
    createCamera(0.78, 6, 9, 3)

    nv.set_dome_light_intensity(0.01)
    nv.disable_dome_light_sampling()

    # -------- floor --------
    # createFloor()
    importTable()

    # -------- robo arm --------
    createRoboArm()

    # -------- creating lights and objects --------
    doLightsAndObjects(1, None)

    render("renders/renderD", renWidth, renHeight, variables.renSamples, variables.denoiseFlag)


def brightImage():
    nv.clear_all()
    print("\n\nbuilding bright image")

    # -------- camera --------
    createCamera(0.78, 6, 9, 3)

    nv.set_dome_light_intensity(5)

    # -------- floor --------
    # createFloor()
    importTable()

    # -------- robo arm --------
    createRoboArm()

    # -------- creating lights and objects --------
    print("...creating lights:")
    range_temperature = variables.range_temperature
    range_intensity = variables.range_intensity
    createSpecLight(0, 0, 0, 5, range_temperature / 2, range_intensity)
    createSpecLight(1, 2, 2, 8, range_temperature, range_intensity / 3)
    createSpecLight(2, -2, 2, 8, range_temperature, range_intensity / 3)
    createSpecLight(3, 2, -2, 8, range_temperature, range_intensity / 3)
    createSpecLight(4, -2, -2, 8, range_temperature, range_intensity / 3)

    doLightsAndObjects(0, None)

    render("renders/renderB", renWidth, renHeight, variables.renSamples, variables.denoiseFlag)


# main function
# setup
setupInput()

print("\n...loading HDRIs...")
hdrArray = scanDir("./HDRs", True)
if len(hdrArray) > 0:
    HDRIs = True
    random.shuffle(hdrArray)

print("...loading materials...")
matArray = scanDir("./materials", False)

print("...initializing scene creation...")
nv.initialize(headless=True)
for i in range(variables.amountScene):
    main(i)

if variables.EXTRA:
    darkImage()
    brightImage()

if variables.EVAL:
    # evalScore(path, scoreType) -> scoreType: 0=SSIM, 1=FID, other=both
    evalScore("./renders", variables.scoreType)

nv.deinitialize()
print("\n---- ALL DONE ----")
sys.exit()
