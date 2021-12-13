# first_pass_annotations
First pass annotations for existing models.

<p align="center">
    <img src="/figures/Model_to_Edit_Annotation.png" | width=800 />
</p>
The first pass annotations begin with a trained model. The model may make its semantic segmentation predictions in the form of one-hot encoded vectors or the RGB masks etc. These prediction mask files can be used to generate a text file of class contours. The contour file vertices may be reduced using the discrete curve evolution algorithm to compress the file size and make future annotation edits more workable. Finally the text file may be converted into any file format which is supported by your editor of choice. We have provided a single final format using the open-source [labelme](https://github.com/wkentaro/labelme) JSON format. 

:green_circle:\[[Paper](https://github.com/beric7/first_pass_annotations/blob/main/Annotation%20Study%20-%20Bianchi.pdf)\] :green_circle:\[[Sample Dataset](https://doi.org/10.7294/16624663.v1)\] :green_circle:\[[Corresponding Sample Trained models](https://doi.org/10.7294/16628620.v1)\]

The dataset link provided in this repository is the corrosion condition state segmentation dataset. This dataset can be used for the localization of structural damage, and for more futuristic style transfer [SPADE](https://arxiv.org/abs/1903.07291) and [GAN](https://arxiv.org/abs/1912.04958) / [GAN-Inversion](https://arxiv.org/abs/2101.05278) applications. 

## Algorithm Description
<p align="center">
    <img src="/figures/algorithm_description.png"  | width=600/>
</p>

## Results
We ran a study across four different images and 24 participants to determine if providing first-pass annotations would even provide benefit to annotators. What we found was that it indeed improved the overall speed and accuracy of their annotations. We also noted the diminishing returns of including too many vertices in the resulting first-pass contours. The two figures below highlight those diminishing returns. The figures of the two graphs were averages of 40 images taken from the test data of the \[[corrosion condition state dataset](https://doi.org/10.7294/16624663.v1)\]. 

<p align="center">
    <img src="/figures/contour_reduction_progression.png"  | width=600/>
</p>

<p align="center">
    <img src="/figures/diminishing returns.png"  | width=600/>
</p>

## Requirements
The most important environment configurations are the following:
- Pytorch >= 1.4
- Python >= 3.6
- tqdm
- matplotlib
- sklearn
- cv2
- Pillow
- pandas
- shutil

The four semantic classes in the sample images in this respository are:
```
Good (Background)
Fair
Poor
Severe
```
These classes make up the four corrosion condition state categories that bridge inspectors must rate the damage extent for each structural bridge detail. These classes can obviously be tailored to any number of classes or specific target dataset or model. 

## Pre-processing

```
# color mapping corresponding to classes
# ---------------------------------------------------------------------
# 0 = Good (Black)
# 1 = Fair (Red)
# 2 = Poor (Green)
# 3 = Severe (Yellow)
# ---------------------------------------------------------------------
self.mapping = {(0,0,0): 0, (0,0,128): 1, (0,128,0): 2, (0,128,128): 3}
```

## Building a Custom Dataset
(The images in the dataset were annotated using [labelme](https://github.com/wkentaro/labelme). We suggest that you use this tool)


1. Before beginning to annotate, we suggest that you use jpeg for the RGB image files. We advised against beginning with images which are already resized. 

2. We have put together a tutorial on tips and tricks on how to use the labelme software in this [youtube video](https://www.youtube.com/watch?v=XtYUPe_JfRw). We also made a [video on youtube](https://www.youtube.com/watch?v=Zd4YmSMLYFQ) showing how to set up labelme with Anaconda prompt.

3. After annotating you will have matching JSON and jpeg files, indicating the annotation and image pair respectfully. 

4. You will take these files and generate masks and one-hot-encoded vector files using ***run_labelme2voc_.py*** file in Pre-processing. Then you can re-scale these images and masks using the respective files in Pre-processing. You can also use the random sort function we have created to randomly split the data. 

The ***labels_corrosion_segmentation.txt*** file contains the class labels needed for the ***run_labelme2voc_.py*** function. If your classes are different then they need to be reflected in this particular file.

## Citation
Corrosion Condition State Dataset: 
```
Bianchi, Eric; Hebdon, Matthew (2021): Corrosion Condition State Semantic Segmentation Dataset. 
University Libraries, Virginia Tech. Dataset. https://doi.org/10.7294/16624663.v1 
```

Corrosion Condition State Model:
```
Bianchi, Eric; Hebdon, Matthew (2021): Trained Model for the Semantic Segmentation of Structural Material. 
University Libraries, Virginia Tech. Software. https://doi.org/10.7294/16628620.v1 
```

Paper:
```
Bianchi, Eric; Hebdon, Matthew (2021): Editing Semantic Model Predictions for Extending Datasets. University Libraries, Virginia Tech.
```
