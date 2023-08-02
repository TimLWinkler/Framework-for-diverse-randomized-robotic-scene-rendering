# A Framework for diverse randomized robotic scene rendering

<<<<<<< HEAD
This framework got created to generate more diverse synthetic data for any Machine Learning or Robotic project.
We mainly coded in Python.

## Installation

We highly recommend that you first install [NViSII](https://github.com/owl-project/NVISII) by:

```bash
pip install nvisii
```

After that, you can download this repository and use it.

## Getting Started

We wrote a default example to cover the basic functionality of our framework.

Starting our framework can be done by either use the express version via console:

```bash
python3 framework.py express n 10 y 1 2 y 1 4 1 5 50 5000 10
```

where the parameters from left to right mean:
Evaluation, rendering Samples, denoising, amount of scenes, amount of cameras per scene, extra scenes,
minimum amount of objects, maximum amount of objects, minimum amount of lights, maximum amount of lights,
light intensity, light temperature, distance from the center

All of these variables will get explained further later.

You can start the framework with default values too, by:

```bash
python3 framework.py default
```

, as well as with a costume input, by:

```bash
python3 framework.py 
```

or 

```bash
python3 framework.py costume
```

## Variables

More variables are listed in the [variables.py](https://github.com/TimLWinkler/Framework-for-diverse-randomized-robotic-scene-rendering/blob/4b795c1de255402cf2777b6c908696d54b01ccdc/variables.py)

Evaluation: boolean if you want an evaluation.
'n' for no evaluation, '0' for evaluation with SSIM, '1' for FID-Score and '2' for both SSIM and FID-Score

- Rendering Samples: Integer for how many sampling per pixel will be cast.

- Denoising: boolean if denoising should be active ('y') or not ('n')

- Amount of scenes: Integer for how many scenes shall be generated

- Amount of Cameras: Integer for how many cameras per scene shall be created

- Extra scenes: boolean to generate two extra scenes (one bright and one dark)

- Minimum and maximum amount of objects: Integer

- Minimum and maximum amount of lights: Integer

- Light intensity: Integer for the light intensity

- Light temperature: Integer for the light temperature

- Distance from the Center: Integer for the maximum distance from the center (0, 0, 0)


## Costume Files

To further customize the scenes and renderings, you can integrate your own objects, HDRI's and materials.

- Objects:
To use new objects or scenes, please use the importFile(.) function from our [helperFunctions.py](https://github.com/TimLWinkler/Framework-for-diverse-randomized-robotic-scene-rendering/blob/4b795c1de255402cf2777b6c908696d54b01ccdc/helperFunctions.py)
Insert the new file into the 'objects' folder to preserve the structure of the project please.

* HDRI's:
Using new HDRI's can be done by simply placing a new HDRI file into the corresponding 'HDRs' folder.
To insure the usage of the new HDRI, you need to either manually set it as a dome texture or delete all other HDRI's from the folder.

- Materials:
New materials can be set by placing the new material inside the 'materials' folder.
The new material has to have at least an image of ambient occlusion ('ao.png'), roughness ('rough.png') and normal ('nor_gl.png') to function.

=======
This README will be added in the furture
>>>>>>> 4b795c1de255402cf2777b6c908696d54b01ccdc
