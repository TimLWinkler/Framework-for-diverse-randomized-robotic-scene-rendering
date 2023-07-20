from evaluation import *        # imports helperFunctions too
from inputHandler import *      # imports variables too


# -------- camera (FOV, x, y, z) --------
camX, camY, camZ = randomCamCoor()
createCamera(0.78, camX, camY, camZ)


# -------- Set the sky/dome --------
hdrArray = scanDir("./HDRs", True)
if len(hdrArray) > 0:
    variables.HDRIs = True
    random.shuffle(hdrArray)

if variables.HDRIs:
    setDome(hdrArray[rng.choice(len(hdrArray), 1, False)][0], True)
else:
    setDomeSky()


# -------- table --------
importTable()


# -------- lights and objects --------
doLightsAndObjects(None, None)


# -------- rendering --------
if variables.multiCam:
    handleMultiCam("TEST", camX, camY, camZ)
else:
    path = "renders/renderTEST"
    render(path, renWidth, renHeight, variables.renSamples, variables.denoiseFlag)
