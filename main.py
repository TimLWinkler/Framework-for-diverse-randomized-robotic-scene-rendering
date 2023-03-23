import nvisii as nv
import numpy.random


from helperFunctions import *
from variables import *

#      TODO's:
# Scores
# position check (clipping) but its not focus for the project

def main(imageNumber):
    nv.clear_all()
    print("\n\nbuilding the scene for render", str(imageNumber) + "...")


# -------- camera --------
    createCamera(0.78, 6, 9, 3)


# -------- Set the sky/dome --------
    dome_rng = rng.choice(len(hdrArray), size=1, replace=False)[0]
    setDome(hdrArray[imageNumber], True)


# -------- floor --------
    #createFloor()
    importTable()


# -------- robo arm --------
    createRoboArm()


# -------- creating lights and objects --------
    doLightsAndObjects(None, None)

# -------- rendering --------
    nameRender = "renders/render" + str(imageNumber)
    render(nameRender, renWidth, renHeight, renSamples, denoiseFlag)


# render dark image
def darkImage():
    nv.clear_all()
    print("\n\n--build dark image--")

# -------- camera --------
    createCamera(0.78, 6, 9, 3)


    nv.set_dome_light_intensity(0.01)
    nv.disable_dome_light_sampling()

# -------- floor --------
    #createFloor()
    importTable()

# -------- robo arm --------
    createRoboArm()

# -------- creating lights and objects --------
    doLightsAndObjects(1, None)

    render("renders/render_dark", renWidth, renHeight, renSamples, denoiseFlag)


def brightImage():
    nv.clear_all()
    print("\n\nbuild bright image")

# -------- camera --------
    createCamera(0.78, 6, 9, 3)

    nv.set_dome_light_intensity(5)

# -------- floor --------
    #createFloor()
    importTable()

# -------- robo arm --------
    createRoboArm()

# -------- creating lights and objects --------
    print("-- creating lights:")
    createSpecLight(0, 0, 0, 5, range_temperature/2, range_intensity)
    createSpecLight(1, 2, 2, 8, range_temperature, range_intensity/3)
    createSpecLight(2, -2, 2, 8, range_temperature, range_intensity/3)
    createSpecLight(3, 2, -2, 8, range_temperature, range_intensity/3)
    createSpecLight(4, -2, -2, 8, range_temperature, range_intensity/3)

    doLightsAndObjects(0, None)

    render("renders/render_bright", renWidth, renHeight, renSamples, denoiseFlag)


# evaluate the images after we rendered them
def FIDScore_eval():
    pass

# call main function
hdrArray = scanDir("./HDRs", True)
random.shuffle(hdrArray)
matArray = scanDir("./materials", False)
nv.initialize(headless=True)
for i in range(3):
    main(i)
#darkImage()
#brightImage()

nv.deinitialize()