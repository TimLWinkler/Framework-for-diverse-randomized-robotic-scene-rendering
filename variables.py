import numpy.random

# variables
DEBUG = True

# render stuff
renWidth = 500
renHeight = 500
renSamples = 256
denoiseFlag = True

# rng
rng = numpy.random.default_rng()

# maximum lights and objects set
maxLights = 5
maxObjects = 5


# for coordinates
xLow = yLow = -15
xHigh = yHigh = 15
zLow = 5
zHigh = 15
xyOffset = numpy.abs(xLow)
zOffset = -zLow

# area where stuf can happen is defined here
range_x = numpy.abs(xLow - xHigh)
range_y = numpy.abs(yLow - yHigh)
range_z = numpy.abs(-zLow + zHigh)

# for lights
range_intensity = 50
range_temperature = 5000