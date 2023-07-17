import numpy
import shutil
import torch
import cv2

from fid_score.fid_score import FidScore
from skimage.metrics import structural_similarity as ssim
from helperFunctions import *


# preparing the evaluation process by creating a new directory
def prepEval():
    try:
        shutil.rmtree("./renders/evaluation")
        os.mkdir("./renders/evaluation")
        os.mkdir("./renders/evaluation/compareRenders")
    except OSError as error:
        print("An ERROR occurred while preparing the evaluation: " + str(error))
        pass


# prepare the FID-Score by getting all the names/dirs of the images
# returns an array with all named paths to the folders of the compare images
def prepFID(path) -> []:
    renders_array = scanDir(path, True)
    for r in renders_array:
        r_dir = path + "/evaluation/compareRenders/" + r.strip('.png')
        try:
            os.mkdir(r_dir)
        except OSError as error:
            print("_prepFID ERROR_: " + str(error))
            pass
        shutil.copy(path + "/" + r, r_dir + "/" + r)

    compare_array = scanDir(path + "/evaluation/compareRenders", False)
    res = []
    for e in compare_array:
        res.append(path + "/evaluation/compareRenders/" + e)

    # clear the score_sheet.txt for new scores
    temp = open(path + "/evaluation/score_sheet.txt", "w")
    temp.close()
    return res


# calculation of SSIM for two given images (their paths)
def prepSSIM(img1_path, img2_path) -> float:
    img1 = cv2.imread(img1_path, 1)
    img2 = cv2.imread(img2_path, 1)
    return ssim(img1, img2, channel_axis=2)


# writing the score into the score_sheet.txt
# for better visual: https://www.geeksforgeeks.org/string-alignment-in-python-f-string/
def writeScore(render1, render2, score, path):
    str_render1 = "render" + str(render1) # str(render1).split('/')[-1]
    str_render2 = "render" + str(render2) # str(render2).split('/')[-1]
    text = [str_render1 + " / " + str_render2 + " scored:  " + score + "\n"]
    with open(path + "/evaluation/score_sheet.txt", "a") as f:
        f.write('\n'.join(text))
    f.close()


# writing the average score of the img for better selection
def writeScoreFinal(imgNameArray, scoreArray, path):
    for i in range(len(imgNameArray)):
        renderName = str(imgNameArray[i]).split('/')[-1].strip(".png")
        text = ["\n" + renderName + " got an avg score of: FID=" + str(
            round(scoreArray[i][0], 3)) + "\tSSIM=" + str(round(scoreArray[i][1], 3)) + "\n"]
        with open(path + "/evaluation/score_sheet.txt", "a") as f:
            f.write('\n'.join(text))
        f.close()


# evaluate the images after we rendered them with SSIM, FID-Score or both
# scoreType: 0 = SSIM, 1 = FID-Score, else = both
def evalScore(path, scoreType):
    print("... starting evaluation ...")
    prepEval()
    temp = []
    if scoreType != 1:
        compare_array_SSIM = scanDir(path, True)
        temp = [[0.0] * 2] * len(compare_array_SSIM)
    if scoreType != 0:
        compare_array_FID = prepFID(path)
        temp = [[0.0] * 2] * len(compare_array_FID)
    avg_score = numpy.array(temp)
    for ren1 in range(len(temp)):
        for ren2 in range(len(temp)):
            # no need to compare the rendered image with itself or twice with the same rendered image
            if ren2 > ren1:
                score = ""

                # write FID-Score
                if scoreType != 0:
                    fid = FidScore((compare_array_FID[ren1], compare_array_FID[ren2]), torch.device('cuda:0'), 1)
                    score_FID = round(fid.calculate_fid_score() / 600, 3)
                    score = score + "FID=" + str(score_FID)
                    # calculate average
                    avg_score[ren1][0] += (score_FID / (len(temp) - 1))
                    avg_score[ren2][0] += (score_FID / (len(temp) - 1))

                # write SSIM-Score
                if scoreType != 1:
                    score_SSIM = prepSSIM(path + "/" + compare_array_SSIM[ren1], path + "/" + compare_array_SSIM[ren2])
                    score = score + "\tSSIM=" + str(round(score_SSIM, 3))
                    # calculate average
                    avg_score[ren1][1] += (score_SSIM / (len(temp) - 1))
                    avg_score[ren2][1] += (score_SSIM / (len(temp) - 1))

                # write score into the sheet
                writeScore(ren1, ren2, score, path)

    # write average score into the sheet
    if scoreType != 0:
        writeScoreFinal(compare_array_FID, avg_score, path)
    else:
        writeScoreFinal(compare_array_SSIM, avg_score, path)
