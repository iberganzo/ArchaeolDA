# ArchaeolDA

## Data Augmentation tool for Deep Learning algorithms 

![Image1_DA](https://user-images.githubusercontent.com/75735764/222118906-95a9c04b-992e-4d36-b677-7c8ac4f46f3b.png)

Data Augmentation (DA) is a technique to MULTIPLY the small amount of training dataset by creating new data from it in order to train your Deep Learning (DL) algorithm, as it is common in Computational Archaeology. This tool is designed for the Mask R-CNN segmentation algorithm entry but the code can be adapted to others.

The methods developed here are random translation, rotation, resizing, elastic deformation, the so-called Doppelgänger technique, and refinement.

Mask R-CNN: https://github.com/matterport/Mask_RCNN

![Image2_DA](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image2_DA.png?token=GHSAT0AAAAAAB7MVZM6OV7WJFH5BM2J2EVMY76IQGA)

### Workflow

1. First of all, you need to annotate all the images you will use as training or validation data. To label the features to be detected you can use VGG Image Annotator (VIA) tool from the University of Oxford (Dutta and Zisserman, 2019).

VGG : https://www.robots.ox.ac.uk/~vgg/software/via/via_demo.html

As an example, to understand the workflow, we will detect different Greek sculptures in pictures. 

![Image3_DA](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image3_DA.png?token=GHSAT0AAAAAAB7NPSMRX3JSS3BY6EGIOFHGY77CFAQ)

Therefore, to automate and accurate the process, we will train a DL segmentation algorithm, but since we only have a single Hellenistic Venus de Milo image as training data, we will implement DA. We will first use VIA tool to label the Venus de Milo we will use for the DA. Use VIA tool to label all the images you will use as training, validation and testing.

![Image4_VGG](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image4_VGG.png?token=GHSAT0AAAAAAB7NPSMR7JEN724A2TG63EOOY77CFZA)

2. Save the labeled images in the `/1_PNG/img/` folder and each corresponding JSON file in the `/1_PNG/json/` folder. Keep the same name for the image as for its associated JSON file. In addition to the `/1_PNG/img/` folder, save each training, validation, and test image to its corresponding folder `/1_PNG/train/`, `/1_PNG/val/` and `/1_PNG/test/`. Now run the python codes `1_PNG`, `2_Polygons` and `3_Objects` to crop the labeled features for use as DA.

```ini
python3 1_PNG.py
python3 2_Polygons.py
python3 3_Objects.py
```

#### Translation

3. Before creating the labeled synthetic images thanks to the DA, we have to attend to a series of configuration parameters in the `4_DA` python code, as well as add several background images (without desired objects) in the `/4_DA/img/` folder.

DA Dataset

```ini
createBackImages = 0 # Background images creation: 0: PNG images, 1: TIFF images, 2: Already created
backImagesStorage = 1 # Number of original background images
backImagesNumberIni = 1 # Initial number of background back%d.png images to use
backImagesNumber = 10 # Number of background back%d.png images to use
numBacksImg = math.ceil(backImagesNumber/backImagesStorage) # Number of back%d.png per background image
cropImagesPerBackImages = 30 # Number of cropped crop%d.png objects to be in each background image
cropImageStoreSize = 1 # List of cropped crop%d.png objects to be used
cropImageStoreSizeInitial = 1 # Initial number of the list of cropped crop%d.png objects to be used
```

DA Configuration

```ini
margin = 200 # Maximun size of an object
fileWeigthTh = 0 # Minimun file size for DA Resizing: 0: All, e.g. 4000: 4 KB
maxPointsNumber = 250 # Maximun number of points in a object polygon
timeoutMin = 5 # Minutes for a timeout during a synthetic image creation
```

Now, run the `4_DA` python code and create new synthetic images. The default DA technique is random translation, copy and paste randomly chosen features for DA into a new random location.

```ini
python3 4_DA.py
```

![Image5_synthTranslate](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image5_synthTranslate.png?token=GHSAT0AAAAAAB7NPSMQQMCT75WEP7GROK2OY77CGWQ)

#### Rotation

Set `daRotate` to 1 in the `4_DA` python code to randomly rotate (between 0 and 359 degrees) the translated features for DA in the synthetic images.

```ini
python3 4_DA.py
```

![Image6_synthRotate](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image6_synthRotate.png?token=GHSAT0AAAAAAB7NPSMR7DLD5YALP3XQOTWGY77CHIQ)

#### Resizing

Set `daResize` to 1,2 or 3 in the `4_DA` python code to randomly resize the translated features for DA in the synthetic images. Also, configure the parameters of this technique to your needs.

```ini
minResized = 45 # Minimun object size after DA Resizing
maxResized = margin - 1 # Maximun object size after DA Resizing
```

```ini
python3 4_DA.py
```

![Image7_synthResize](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image7_synthResize.png?token=GHSAT0AAAAAAB7NPSMR4S6YOVHFE6VNACESY77CH3A)

#### Elastic Deformation

Set `daElastic` to 1 in the `4_DA` python code to randomly elastically deform the translated features for DA in the synthetic images. Also, configure the parameters of this technique to your needs.

```ini
nDiamRMax = 3 # The maximum side ratio for DA Elastic Deformation
```

```ini
python3 4_DA.py
```

![Image8_synthElastic](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image8_synthElastic.png?token=GHSAT0AAAAAAB7NPSMQFLS3OD6ZIUZZ67D2Y77CJIA)

#### Doppelgänger

But what happens when the object for DA have a hole inside like a Doughnut? Will be added as a desired feature to train different random background contexts.

![Image9_DonutShape](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image9_DonutShape.png?token=GHSAT0AAAAAAB7NPSMRSQICPP4TZOUSDRJIY77C22Q)

To avoid this, you can use the so-called Doppelgänger technique from our ArchaeolDA tool. This technique makes it possible to ensure that these random background contexts (the ones in the Doughnut hole) are also included as negative training by copying them out of the object feature.

![Image10_Doppel](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image10_Doppel.png?token=GHSAT0AAAAAAB7NPSMQVDGQE6ZWF3YGA2D6Y77CYFA)

Let's see a case where we will use a Doughnut for DA! Set `doppel` to 1 in the `4_DA` python code to use the Doppelgänger technique.

```ini
python3 4_DA.py
```

As can be seen in the image below, the face of the statue of Homer, which is a ramdon background context, is duplicated to ensure that the algorithm learns exactly what a Doughnut is (positive training) and understands the rest as background (negative training). The same happens for example with the grapes, the leg of the table, Marge's belt and the ceiling of the room.

![Image11_synthDoppel](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image11_synthDoppel.png?token=GHSAT0AAAAAAB7NPSMQFPTZCWHX54VX4SF6Y77DBBQ)

#### Refinement

Sometimes, after the initial training, we find a series of false positives similar to the object feature used to train the algorithm. Therefore, it is recommended to add a refinement step that includes this series of false positives in the training as negative. To do this, the ArchaeolDA tool allows us to include those false positives before creating the DA. We can see an example below where we will use Homer's donut-head as a false positive for Doughnut training. Add the false positives in the `/4_DA/FP/` folder and run the `Refinement` python code from the `/4_DA/` folder.

```ini
backImagesStorage = 1 # Number of original background images
backImagesNumber = 10 # Number of background back%d.png images to use
numBacksImg = math.ceil(backImagesNumber/backImagesStorage) # Number of back%d.png per background image
createBackImages = 0 # Background images creation: 0: PNG images, 1: TIFF images, 2: Already created
imgFP = 50 # Average number of each false positive per background image

rotateFP = 1 # Negative training data rotation
margin = 200 # Maximun size of a false positive
```

```ini
python3 4_DA/Refinement.py
python3 4_DA.py
```

![Image12_synthRefinement](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image12_synthRefinement.png?token=GHSAT0AAAAAAB7NPSMQ7DDM2MVYW5WMULRAY77CVFQ)

#### Image Division

Likewise, this tool allows us to divide the generated images into a more affordable size for computation, keeping the multiple objects created labeled to use them directly in the training of the DL algorithm. A `via_region_data.json` file associated with the training, validation, and test data will be generated.

```ini
tesela = 512 # Image size to train, validate, test and detect in pixels
addPointsNumber = 8 # Number of points between labeled points
```

```ini
python3 5_Split.py
```

```ini
tesela = 512 # Image size to train, validate, test and detect in pixels
trainVal = 0 # 0: To create training data
			# 1: To create validation data
			# 2: To create test data
```

```ini
python3 6_Merge.py
```

```ini
trainVal = 0 # 0: To create training data
			# 1: To create validation data
			# 2: To create test data
```

```ini
python3 7_Data.py
```

![Image13_Divided](https://raw.githubusercontent.com/iberganzo/ArchaeolDA/main/Images/Image13_Divided.png?token=GHSAT0AAAAAAB7NPSMRZY5T23AVPXLV46ZSY77FKQA)

### Citation

To cite this repository:

```ini
Berganzo-Besga, I. ArchaeolDA: Data Augmentation tool for Deep Learning algorithms. GitHub repository 2023. Available online: https://github.com/iberganzo/ArchaeolDA
```
