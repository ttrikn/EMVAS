from MSA_FET import FeatureExtractionTool, get_default_config


# initialize with default librosa config which only extracts audio features
#fet = FeatureExtractionTool("openface")

# alternatively initialize with a custom config file
fet = FeatureExtractionTool("custom_config.json")

# extract features for single video 提取单个视频特征，首先把视频和字幕放在这个文件夹下
infile1 = "E:\\MMSA-FET-master\\src\\MSA_FET\\input\\input2.mp4"
textfile1 = "E:\\MMSA-FET-master\\src\\MSA_FET\\input\\input2.txt"
outfile1 = "E:\\MMSA-FET-master\\src\\MSA_FET\\feature\\feature2.pkl"
feature1 = fet.run_single(in_file=infile1, text_file=textfile1, out_file=outfile1)
#print(feature1)
#然后再回到mmsa里

# extract for dataset & save features to file 提取数据集特征，首先这里提取数据集特征
fet.run_dataset(
   dataset_dir="E:\\MMSAdatasets\\MOSI",
  out_file="E:\\MMSA-FET-master\\src\\feature.pkl",
   num_workers=0
)

#结束之后会在这里生成数据集的特征文件