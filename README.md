# HOW TO THESE YOLOV5 CODE WITH MOBILITY DATASET

+ **Step 1**: Install requirement described in `requirements.txt` file

+ **Step 2**: In the folder `data`, create a folder named `mobility`. Download and copy the train/valid/test data into that folder.
  + For mobility dataset (15 classes), data can be downloaded from this [link](https://drive.google.com/drive/folders/12EiV92VHRoM8R9N9SL-3okPG2TU1fl5b?usp=sharing)
  + For mobility dataset (4 classes of group 2: *Micro Car, SUV, Bus, Van*), data can be downloaded from this [link](https://drive.google.com/drive/folders/12EiV92VHRoM8R9N9SL-3okPG2TU1fl5b?usp=sharing)
  + For both cases, copy file `mobility.yaml` (in downloaded data) and put it into `data` folder

+ **Step 3**: For training, run the code in the file `zrun.bat` with command prompt (terminal in macOS) - edit the batch, epoch, etc. (the argument --img 640 is fixed for pretrained model yolov5l)

+ **Step 4**: For run detection, run the code in the file `zdetect.bat` with command prompt (terminal in macOS) - edit the --conf threshold and the path for image folder.
You can change the **data augmentation configuration** in file `data/hyps/hyp.scratch-low.yaml`
  
+ **Step 5**: Check the results (for training or detect) inside folder `runs`

https://blog.roboflow.com/yolov5-improvements-and-evaluation/
