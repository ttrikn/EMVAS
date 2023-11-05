# E2E-MERA-SC
This is the open source code for paper: Open source code for paper: End-to-End Emotion Recognition Method Based on Multimodal Information from Voice, Text, and Images
## Paper Abstract 

> The burgeoning prevalence of smart cities and smart homes heralds an intensifying interaction between humans and technology. Against this backdrop, crafting a more intuitive and natural interactive experience has become paramount. In sectors such as smart healthcare and intelligent transportation, accurately capturing and comprehending human emotions is crucial. Yet, most of today’s emotion recognition techniques lean heavily on singular modalities, undoubtedly constraining their depth and breadth in capturing emotions, especially in intricate settings. Multimodal emotion recognition, amalgamating in-depth analyses of images, voice, and text, is emerging as a frontrunner. Given these considerations, to further the widespread application of multimodal emotion recognition in smart city domains, including smart healthcare, product recommendations, and smart homes, we have devised an innovative end-to-end multimodal emotion recognition framework. This encompasses three pivotal dimensions: voice, text, and image. To streamline the manual text input phase within the multimodal system, we have integrated automatic speech recognition technology, translating voice into real-time text labels. Additionally, for voice, image, and text, we have engineered an efficient end-to-end feature extraction approach. To delve deeper into the synergistic value across modalities, we’ve also incorporated a self-supervised multi-task learning strategy. Ensuring its efficacy in real-world scenarios, we furnish a comprehensive deployment and implementation guide. Rigorous experimental validation underscores the exemplary performance of this framework, highlighting its vast application potential.

If you are interested in our work, please contact zhuxianxun@shu.edu.cn  

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
