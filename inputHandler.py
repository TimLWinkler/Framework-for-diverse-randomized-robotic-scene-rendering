import variables
import numpy
import sys
from colorama import Fore, Style


# define Python user-defined exceptions
class InputErrorException(Exception):
    """Raised when parameter input was not correct"""#
    def __init__(self, mode):
        if mode == 1:
            print(Fore.RED + "Error occurred!")
            print(Style.RESET_ALL + "Please check the parameters given and there form.")
            sys.exit()


# returns False if default mode and True if costume or no mode is set
def argSetup() -> bool:
    if variables.DEBUG:
        print("Number of arguments: " + str(len(sys.argv)))
        print("Argument List: " + str(sys.argv))
    if len(sys.argv) > 1:
        if sys.argv[1] == "default":
            return False
        elif sys.argv[1] == "costume":
            return True
        else:  # express mode
            try:
                # check express mode again
                print(sys.argv[1])
                if sys.argv[1] == "express":
                    expressModeHandle(sys.argv[2:])
                else:
                    raise InputErrorException(1)
            except InputErrorException:
                raise InputErrorException(1)
    else:
        return True


# handling express mode arguments
def expressModeHandle(argList):
    start = 0
    objectsFlag = False
    lightFlag = False
    if len(argList) != 13:
        print("Arguments did not match expected amount")
        raise InputErrorException(1)
    for index, elem in enumerate(argList, start):
        if variables.DEBUG: print(elem)
        # EVAL n/0,1,2 -> Eval type set to both
        if index == 0 and elem != "n":
            variables.EVAL = True
            variables.scoreType = int(elem)
        elif index == 0 and elem == "n":
            variables.EVAL = False
        # renSamples int
        elif index == 1:
            variables.renSamples = int(elem)
        # denoiseFlag y/n
        elif index == 2 and elem == "y":
            variables.denoiseFlag = True
        elif index == 2 and elem == "n":
            variables.denoiseFlag = False
        # amountScene int
        elif index == 3:
            variables.amountScene = int(elem)
        # MultiCam n/int
        elif index == 4 and elem != "n":
            variables.multiCam = True
            variables.amountCameras = int(elem)
            variables.scoreType = 2
        # EXTRA y/n
        elif index == 5 and elem == "y":
            variables.EXTRA = True
        elif index == 5 and elem == "n":
            variables.EXTRA = False
        # maxObjects Min Max int
        elif index == 6:
            if int(elem) < int(argList[index + 1]):
                variables.maxObjects = variables.rng.choice(a=int(argList[index + 1]), size=2, replace=False) + int(elem)
                objectsFlag = True
        elif objectsFlag and index == 7:
            continue
        # maxLights Min Maxint
        elif index == 8:
            if int(elem) < int(argList[index + 1]):
                variables.maxLights = variables.rng.choice(a=int(argList[index + 1]), size=2, replace=False) + int(elem)
                lightFlag = True
        elif lightFlag and index == 9:
            continue
        # light intensity range int
        elif index == 10:
            variables.range_intensity = int(elem)
        # light temperature range int
        elif index == 11:
            variables.range_temperature = int(elem)
        # distance int
        elif index == 12:
            variables.distance = int(elem)

        else:
            print("Wrong argument at " + str(elem) + " at " + str(index))
            raise InputErrorException(1)


# handle if we want costume settings or not
def setupInput():
    if argSetup():
        # input if default values or costume setting
        inputCostume = input("Enter 'costume' if you want to setup costume settings: ")
        if inputCostume != "costume":
            if inputCostume != "default":
                # if neither costume nor default is writen, we give 3 extra chances
                for i in range(3):
                    inputCostume = input(
                        "We do not know that input, please enter the mode again (" + str(i) + "/3 tries): ")
                    if inputCostume == "costume":
                        costumeInput()
                        break
                    elif inputCostume == "default":
                        return
                print("We do not understand that input.\nWe will set default mode.")
        else:
            costumeInput()


# handle all costume 11 costume settings
def costumeInput():
    # input if evaluation shall be happening
    inputEval = input("Enter 'y' if u want to have evaluation: ")
    if inputEval == "y":
        variables.EVAL = True
        # input what type of eval
        inputScoreType = input("Enter number of evaluation? (0=SSIM, 1=FID, all other=both): ")
        if inputScoreType == "0":
            variables.scoreType = 0
        elif inputScoreType == "1":
            variables.scoreType = 1
    else:
        variables.EVAL = False

    # input rendering samples (how many rays do get shot into the scene per pixel)
    inputSamples = input("Enter sampling amount of the render (e.g. 512): ")
    variables.renSamples = int(inputSamples)

    # input denoising active or not
    inputDenoise = input("Enter 'n' to deactivate denoising (anything else then 'n' will keep denoising active): ")
    if inputDenoise == "n":
        variables.denoiseFlag = False

    # input amount of scenes to get rendered
    inputSceneAmount = input("Enter amount of scenes (e.g. 5): ")
    variables.amountScene = int(inputSceneAmount)

    # input amount of cams to get rendered in one scene n/int
    inputCamAmount = input("Enter amount of cameras for one scene ('n' means 1, >1 else): ")
    if inputCamAmount != "n":
        variables.multiCam = True
        variables.amountCam = int(inputSceneAmount)
        variables.scoreType = 2

    # input for extra (dark and bright) render
    inputExtra = input("Enter 'y' if we shall render two extra scenes (one extra dark, one extra bright): ")
    if inputExtra == "y":
        variables.EXTRA = True

    # input min and max amount of objects
    inputMinObj = input("Enter minimum amount of objects (e.g. 1): ")
    inputMaxObj = input("Enter maximum amount of objects (e.g. 7): ")
    variables.maxObjects = variables.rng.choice(a=int(inputMaxObj), size=1, replace=False) + int(inputMinObj)

    # input min and max amount of lights
    inputMinLights = input("Enter minimum amount of lights (e.g. 1): ")
    inputMaxLights = input("Enter maximum amount of lights (e.g. 7): ")
    variables.maxLights = variables.rng.choice(a=int(inputMaxLights), size=1, replace=False) + int(inputMinLights)

    # input range for intensity (light)
    inputIntensity = input("Enter maximum for light intensity (e.g. 50): ")
    variables.range_intensity = int(inputIntensity)

    # input range for temperature (light)
    inputTemperature = input("Enter maximum for light temperature (e.g. 5000): ")
    variables.range_temperature = int(inputTemperature)

    # input camera and object area
    inputArea = input("Enter maximum distance from coordinate origin for object and light placement (e.g. 15): ")
    distance = int(inputArea)
    variables.xyOffset = numpy.abs(distance)
    variables.range_x = variables.range_y = distance * 2
    variables.range_z = numpy.abs(numpy.abs(distance) - 5)
