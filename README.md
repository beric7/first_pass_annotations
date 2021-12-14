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
In case you only have a model's color mask prediction images (RGB), we wrote a script to convert those images into one-hot-encoded-vectors (ohev). This option is good if you do not want to write code for a model which is not compatible with the our script ***run_show_results_ohev.py***, in the validation folder. The ohevs are our choice for the input into our contouring algorithm, and are great if you need to resize the prediction data. 

**Step 1:** In the file ***run_mask_to_ohev.py***, define the mask directory and where you would like to store the resulting one-hot-encoded-vector files (ohev). 

```
mask_dir = './sample_data/masks/'
ohev_dest = './ohev/'
```

**Step 2:** In the file ***mask_to_ohev.py***, define the colors to correspond to the class numbers in the ohev file. In this case we only have four classes 0-3, but you may have more or less depending on your model. Unfortunately this method requires you to know the exact RGB value of the prediction mask, however, finding these values are not to hard to do on your own, and they are often listed with off the shelf models or datasets. 

<p align="left">
    <img src="/figures/CorrespondingClassColors.png"  | width=400/>
</p>

```
# color mapping corresponding to classes
# ---------------------------------------------------------------------
# 0 = Good (Black)
# 1 = Fair (Red)
# 2 = Poor (Green)
# 3 = Severe (Yellow)
# ---------------------------------------------------------------------
mapping = {(0,0,0): 0, (0,0,128): 1, (0,128,0): 2, (0,128,128): 3}
```
**Step 3:** Run the ***run_mask_to_ohev.py***

## Generating Masks with a Pre-trained Model
If you do not have the RGB value masks or the one-hot-encoded-vector files, do not worry, we wrote a script for that too. If you have a pytorch model, than you are more than likely able to generate the one-hot-encoded-vectors (ohevs) using our code. Open up ***run_show_results_ohev.py*** in the validation folder. Then follow the steps listed below. 

**Step 1:** Find the path to the stored weights of your model. If you want to test a model you can download the corrosion condition state model at \[[Corresponding Sample Trained models](https://doi.org/10.7294/16628620.v1)\]
```
model = torch.load(f'./PATH TO STORED MODEL WEIGHTS.pt', map_location=torch.device('cuda'))
```
**Step 2:** Input the: image directory, destination for the prediction masks, destination for the mask and image overlays, and the destination for the one-hot-encoded-vector prediction files. As a note, the model will make predictions on the image directory that you give it. 
```
source_image_dir = './PATH TO SOURCE IMAGES/'
destination_mask = './DESTINATION MASK FOLDER/'
destination_overlays = './DESTINATION OVERLAY FOLDER/'
destination_ohev = './DESTINATION OHEV FOLDER/'
```
**Step 3:** Alter the color mapping values in the file ***show_results_ohev.py***. 
```
# color mapping corresponding to classes:
# ---------------------------------------------------------------------
# 'one_hot_number' = 'class_name', (RGB), (BGR)
# 0 = background (good), (0,0,0), (0,0,0)
# 1 = fair, (128,0,0), (0,0,128)
# 2 = poor, (0,128,0), (0,128,0)
# 3 = severe, (128,128,0), (0,128,128)
# ---------------------------------------------------------------------

mapping = {0:np.array([0,0,0], dtype=np.uint8), 1:np.array([0,0,128], dtype=np.uint8),
           2:np.array([0,128,0], dtype=np.uint8), 3:np.array([0,128,128], dtype=np.uint8)}  
```
**Step 4:** Run ***run_show_results_ohev.py***

## Generate Editable Predictions
At this point you should have your predictions in the one-hot-encoded-vector format. We are now ready to contour them and convert them into an editable format. As stated before, we will convert the predictions into a JSON format compatible with [labelme](https://github.com/wkentaro/labelme). We do also convert the predictions into a text file format so that you can generate them into a different file format which may suit the needs of your target editor. You should be in the first_pass_annotations folder and open ***run_contour_semantic_segmentation.py*** file. 

**Step 1:** Determine file paths
```
ohev_directory = './sample_data/ohev/'
image_dir = './sample_data/Masks/'
destination = './output_files/contours_3_pass/'
text_dest = './output_files/text_3_pass/'
json_dest = './output_files/json_3_pass/'
```
**Step 2:** The ***dce_pass*** variable controls the number of DCE passes to run on the contours. We suggest doing three passes. Optionally, set the boolean ***AREA*** to True if you wish to hault the DCE passes early if the area of the original area changes too much. This option is great if you do not want to blindy remove contours. When this option ***AREA*** is set to TRUE then you can set the number of DCE passes very high since it will stop before removing too much information.  
```
AREA = True

# NUMBER OF DCE PASSES, WE RECOMMEND (3) IF NOT MORE...
# EACH DCE PASS REDUCES THE NUMBER OF POINTS BY 1/2, UNLESS THE AREA CHANGES
# TOO MUCH (if the original area changes by 5%).
dce_pass = 3
```
**Step 3:** Run ***run_contour_semantic_segmentation.py***.

## Editing Files in Labelme
At this point you have JSON files which are now compatible with the lableme software, and can be opened up inside of labelme to be edited. To do this you will first need to download labelme. Then copy the JSON files and image files into a joint folder. The JSON files should be named the same as the image files, just with different extensions. Open the joint JSON and image file inside of labelme to view and edit the files. We have put together a tutorial on tips and tricks on how to use the labelme software in this [youtube video](https://www.youtube.com/watch?v=XtYUPe_JfRw). We also made a [video on youtube](https://www.youtube.com/watch?v=Zd4YmSMLYFQ) showing how to set up labelme with Anaconda prompt.

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
Bianchi, Eric; A. Lynn, Abbott (2021): Editing Semantic Model Predictions for Extending Datasets. University Libraries, Virginia Tech.
```
