import numpy.random

# variables

# flags
DEBUG = False
HDRIs = False
EVAL = False
EXTRA = False
denoiseFlag = True

# render stuff
renWidth = 1500
renHeight = 1500
renSamples = 512

# rng
rng = numpy.random.default_rng()

# maximum scenes, lights, objects and amount of cameras
amountScene = 2
maxLights, maxObjects = rng.choice(a=7, size=2, replace=False) + 1
amountCameras = 4


# for coordinates distance to origin (0, 0, 0)
distance = 15
xyOffset = numpy.abs(distance)
zLow = 5
zOffset = zLow * -1

# area where stuff can happen is defined here
range_x = range_y = distance * 2
range_z = numpy.abs(distance - zLow)

# for lights
range_intensity = 50
range_temperature = 5000

# for cameras
lookAtX = 0
lookAtY = 0

# evaluation Type
scoreType = 2
