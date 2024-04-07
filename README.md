# EMVAS
This is the open source code for paper: Open source code for paper: End-to-End Multimodal Emotion Visualization Analysis System.
## Table of Contents
- [Paper Abstract](##PaperAbstract)
- [Preparation](##Preparation)
- [Running](##Running)
- [Training](##Training)

## Paper Abstract 

> With the growing demand for end-to-end visual emotion analysis methods, particularly in fields such as fatigue monitoring for bus drivers and anomaly emotion detection in school students, this paper presents an End-to-End Multimodal Emotion Visualization Analysis System. Unlike traditional methods that rely solely on a single modality for end-to-end emotion analysis, our system comprehensively mines and analyzes emotional information in videos. It implements end-to-end analysis by extracting and integrating three modalities of information from videos: visual, textual, and auditory. Diverging from existing research focused primarily on algorithmic models, our system places greater emphasis on application-level real-time visualization display and analysis, offering detailed data such as timelines of emotional changes and frequencies of emotions. Additionally, we have developed a video preprocessing architecture specifically for extracting slices of unimodal information, including images, text, and voice, from raw videos. The system's effectiveness has been verified through model testing and real-world scenario applications.
> <div align=center>
> <img src="https://github.com/ttrikn/EMVAS/blob/master/script/1.jpg" width="1000"></img>
> </div>
## Preparation
### Datasets
As mentioned in our paper, in order to train our model, you need to download the CH-SIMS dataset here: [CH-SIMS](https://drive.google.com/drive/folders/1A2S4pqCHryGmiqnNSPLv7rEg63WvjCSk).or you can also use other multimodal sentiment datasets.

### Environment

* Python 3.7
* PyTorch 1.12.1
* torchaudio 0.12.1
* torchvision 0.13.1
* transformers 4.29.2
* tqdm 4.65.0
* moviepy 1.0.3
* numpy 1.24.3
* scipy 1.10.1

## Running
To get a quick start, you can run the following command
```
python demo.py
```

## Training
### Training the Speech Recognition Model
To train the model, one must execute the provided training script. The specific parameter configurations can be located in the configs directory of our open-source code. Our model is designed to auto-save either
after each training epoch or every 10,000 batches. If data augmentation techniques are not required, set the augment conf path parameter to None. By default, upon completion of each training epoch, the system
will automatically evaluate the model on the test set and calculate its accuracy. To optimize training efficiency, we utilize a greedy decoding strategy. The model also supports resuming training after 
interruptions. If the last model directory exists within the model directory, the system will automatically load the model upon starting the training. However, if the resume model parameter is explicitly 
specified, it takes precedence.
```
# Single machine, single GPU training
CUDA_VISIBLE_DEVICES =0
python train.py
# Single machine, multi -GPU training
CUDA_VISIBLE_DEVICES =0,1 torchrun -- standalone -- nnodes =1
-- nproc_per_node =2
python train.py
```
### Training the Feature Fusion Model
For feature extraction pertaining to the SIMS dataset, we employ the FeatureExtraction tool. To boost the efficiency during feature extraction, adjust the num workers parameter based on your system’s hardware 
setup.
The training progress can be monitored in real-time by checking the logs in the log directory. The final model will be saved in the saved models directory.
```
# Initialize Feature Extraction with configuration
feaE = FeatureExtraction (" config . json ")
# Run dataset feature extraction
feaE . run_dataset ( dataset_dir =" ...\ CH - SIMS ", out_file =" ...\feature .pkl ", num_workers = n )
# Get configuration for ’mtme ’ and ’sims ’config = get_config (’mtme ’, ’sims ’)
# Set feature path in the configuration
config [’featurePath ’] = out_file
# Execute the MSA run with the given configuration
MSA_run (’mtme ’, ’sims ’, config = config )
```

## Real-World Testing
In order to rigorously validate the accuracy of our system analysis, we recruited 50 volunteers for a practical test, as depicted in figure. During the test, volunteers expressed a range of emotions following scripts designed to mimic authentic emotional responses. Each volunteer participated in an emotion expression test lasting 2-3 minutes, with select script excerpts shown in figure. Analyzing and observing the emotional expressions of these 50 volunteers, the system demonstrated overall effectiveness in emotion recognition. However, it showed a reduced accuracy in scenarios where emotional expressions were less pronounced. Moving forward, we aim to reffne the model to enhance its accuracy in complex emotional recognition contexts.

<div align=center>
<img src="https://github.com/ttrikn/EMVAS/blob/master/script/3.jpg" width="1000"></img>
</div>

## Demonstration of Visualization Cases
To thoroughly evaluate the effectiveness of our system’s visual emotion analysis,as depicted in the figure, three distinct test segments were selected for examination.In the ffrst instance, Volunteer 1, who appeared dejected due to a foot injury, was accurately identiffed by the system as having a negative emotional state. In the second instance, Volunteer 2, speaking in an even, unemotional tone, was determinedby the system to have a neutral emotional state. In the third instance, Volunteer 3,elated by his favorite team’s victory, was correctly identiffed by the system as having a positive emotion. These outcomes corroborate the high precision of our system inemotional analysis, demonstrating the potential applicability of our system model incomplex emotional recognition scenarios.

<div align=center>
<img src="https://github.com/ttrikn/EMVAS/blob/master/script/5.jpg" width="700"></img>
</div>

If you are interested in our work, please contact zhuxianxun@shu.edu.cn  
