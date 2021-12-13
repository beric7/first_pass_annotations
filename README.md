# first_pass_annotations
First pass annotations for existing models.

<p align="center">
    <img src="/figures/Model_to_Edit_Annotation.png" | width=800 />
</p>
The first pass annotations begin with a trained model. The model may make its semantic segmentation predictions in the form of one-hot encoded vectors or the RGB masks etc. These prediction mask files can be used to generate a text file of class contours. The contour file vertices may be reduced using the discrete curve evolution algorithm to compress the file size and make future annotation edits more workable. Finally the text file may be converted into any file format which is supported by your editor of choice. We have provided a single final format using the open-source [labelme 2016](https://github.com/wkentaro/labelme) JSON format.  


These classes make up the four corrosion condition state categories that bridge inspectors must rate the damage extent for each structural bridge detail. These classes can obviously be tailored to any number of classes or specific target dataset or model. 

:green_circle:\[[Paper](Annotation Study - Bianchi.pdf)\] :green_circle:\[[Sample Dataset](https://doi.org/10.7294/16624663.v1)\] :green_circle:\[[Corresponding Sample Trained models](https://doi.org/10.7294/16628620.v1)\]

The dataset link provided in this repository is the corrosion condition state segmentation dataset. This dataset can be used for the localization of structural damage, and for more futuristic style transfer [SPADE](https://arxiv.org/abs/1903.07291) and [GAN](https://arxiv.org/abs/1912.04958) / [GAN-Inversion](https://arxiv.org/abs/2101.05278) applications. 

## Results
We ran a study across four different images and 24 participants to determine if providing first-pass annotations would even provide benefit to annotators. What we found was that it indeed improved the overall speed and accuracy of their annotations. We also noted the diminishing returns of including too many vertices in the resulting first-pass contours. The two figures below highlight those diminishing returns. The figures of the two graphs were averages of 40 images taken from the test data of the \[[corrosion condition state dataset](https://doi.org/10.7294/16624663.v1)\]. 

<p align="center">
    <img src="/figures/contour_reduction_progression.png.png"  | width=600/>
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

## Evaluating the Trained DeeplabV3+ Model
- Download the DeeplabV3+ :green_circle:[trained model weights](https://doi.org/10.7294/16628620.v1)
- Configure ***run_metrics_evaluation.py***

You will get the f1 score, the jaccard index, and the confusion matrix. We suggest running this in an IDE. 
  
## Visualizing the results from the Trained DeeplabV3+ Model
Once training has converged or when it has stopped, we can used the best checkpoint based on the validation data results. This checkpoint is loaded and our test data is evaluated. 

***run_show_results__.py***
- gets predicted masks
- gets combined mask and image overaly
- gets one-hot-encoded vector images of predictions

## Training with the Structural Material dataset

1. Clone the repository
2. Download the :green_circle:[dataset](https://doi.org/10.7294/16624663.v1)
3. Go into the Training folder
4. Create a DATA folder
5. Copy and paste the Train and Test folders for 512x512 images from the dataset you downloaded into the DATA folder
6. The DATA folder should have a folder called 'Train' and a folder called 'Test'. Inside each of those folders include the mask and image pairs in their respective folders (Masks, Images). 
7. If you have set this up correctly then you are now ready to begin.

Neccesary and optional inputs to the ***main_plus.py*** file:
('-' means it is neccessary, '--' means that these are optional inputs)
```
 -data_directory = dataset directory path (expects there to be a 'Test' and a 'Train' folder, with folders 'Masks' and 'Images')
 -exp_directory = where the stored metrics and checkpoint weights will be stored
 --epochs = number of epochs
 --batchsize = batch size
 --output_stride = deeplab hyperparameter for output stride
 --channels = number of classes (we have four, the default has been set to four). 
 --class_weights = weights for the cross entropy loss function
 --folder_structure = 'sep' or 'single' (sep = separate (Test, Train), single = only looks at one folder (Train). If you want to get validation results instead of getting back your test dataset results then you should use 'single'. If you want to test directly on the Test dataset then you should use 'sep'.
 --pretrained = if there is a pretrained model to start with then include the path to the model weights here. 
```

Run the following command:
```
python main_plus.py -data_directory '/PATH TO DATA DIRECTORY/' -exp_directory '/PATH TO SAVE CHECKPOINTS/' \
--epochs 40 --batch 2
```

During training there are model checkpoints saved every epoch. At these checkpoints the model is compared against the test or validation data. If the test or validation scores are better than the best score, then it is saved. 

## Training with a custom dataset
1. Clone the repository
2. Ensure your image and mask data is 512x512 pixels. *(can use the ***rescale_image.py*** in Pre-processing)*
3. Ensure that if you resized your masks to 512x512 that they did not interpolate the colors into more color classes than you have. The expected format is BGR. *(can use the ***rescale_segmentation.py*** in Pre-processing)*
4. You now need to go into the ***datahandler_plus.py*** file and edit the colors as necessary. For example, the Structural Materials dataset used the following format, which is in the ***datahandler_plus.py*** in this repository.
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
6. Adjust the number of 'channels' in the training command to match the number of channels that you have.
7. Ensure that your DATA folder has a folder called 'Train' and a folder called 'Test'. Inside each of those folders include the mask and image pairs in their respective folders (Masks, Images). 
8. If you have set this up correctly then you are now ready to begin.

## Building a Custom Dataset
(The images in the dataset were annotated using [labelme](https://github.com/wkentaro/labelme). We suggest that you use this tool)

0. **If you are planning to extend on the corrosion dataset, then please read the annotation guidelines provided by the author in the :green_circle: [corrosion dataset](https://doi.org/10.7294/16624663.v1) repository.**

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

```
