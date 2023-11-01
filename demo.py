import torch
import glob
import os
from MMSA import MMSA_run
from MMSA import MMSA_test
from MMSA import get_config_regression
from MSA_FET import FeatureExtractionTool, get_default_config
from MSA.wav2text import video2text
from MSA.detect import is_video_complete
from app01.PPASRmaster.zimu import predict_audio
import pymysql
import time


def demo(infile1):
	filename = video2text(infile1)
	textfile1 = f"D://djangoproject//MSA/slicetext/{filename}/"
	fet = FeatureExtractionTool("D://djangoproject/MSA/MMSA-FET-master/src/MSA_FET/custom_config.json")
	config = get_config_regression('tfn', 'sims')
	config['post_fusion_dim'] = 32
	# feature1 = fet.run_single(in_file=infile1, text_file=textfile1, out_file=outfile1)
	# config['featurePath'] = outfile1
	#fea = "/home/abc/data/wyy/MSA-FET-master/src/MSA_FET/feature/feature10_chinese.pkl"
	model = "D://djangoproject//MSA/MMSA/saved_models/tfn-sims.pth"
	wav_files = glob.glob(os.path.join(textfile1, "*.txt"))
	result = []
	for text in wav_files:
		headname = os.path.basename(text)
		headname = headname.split(".")[0]
		invideo = f"D://djangoproject/MSA/slicevideo/{filename}/{headname}.mp4"
		intext = f"D://djangoproject/MSA/slicetext/{filename}/{headname}.txt"

		flag , duration=  is_video_complete(invideo)

		print(invideo+"检验结果为："+str(flag))
		if not flag:
			continue

		outfile1 = f"D://djangoproject/MSA/MSA-FET-master/src/MSA_FET/feature/feature{headname}.pkl"
		fet.run_single(in_file=invideo, text_file=intext, out_file=outfile1)
		num = MMSA_test(config, model, outfile1, 0)

		print(infile1)
		file_name = infile1.split('/')[-1]
		print(file_name)
		# 连接mysql
		conn = pymysql.connect(port=3306, user='root', password='', charset='utf8', db='gx_day16')
		cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

		# 记录检测时间
		texttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		print(texttime)

		sql2 = "insert into app01_mult_list(img_name, detection_date, multResult) values (%s,%s,%s)"
		cursor.execute(sql2, [file_name, texttime, num])
		conn.commit()
		# 关闭
		cursor.close()
		conn.close()

		result.append(num)
		# if result_num < -1 or result_num > 1:
		# 	emo = "其他情绪"
		# elif result_num < -0.7:
		# 	emo = "愤怒"
		# elif result_num < -0.4:
		# 	emo = "焦虑"
		# elif result_num < -0.1:
		# 	emo = "疲惫"
		# elif result_num < 0.1:
		# 	emo = "中性"
		# elif result_num < 0.4:
		# 	emo = "轻松"
		# elif result_num < 0.7:
		# 	emo = "开心"
		# else:
		# 	emo = "兴奋"
		#result.append(emo)·

	print("done")
	print(result)
	return result

def realtimedemo(infile1, infile2):
	text = predict_audio(infile1)
	realtimetext = "D://djangoproject/MSA/realtiming/text/realtime.txt"
	with open(realtimetext, "w", encoding="utf-8") as file:
		file.write(str(text))
	print("结果已保存到", realtimetext)
	with open(realtimetext, "r", encoding='utf-8') as file:
		if not bool(file.read()):
			num = 0
			print("音频和文本模态为空，请录制音频")
		else:
			print("文件不为空")
			fet = FeatureExtractionTool(
				"D://djangoproject/MSA/MMSA-FET-master/src/MSA_FET/custom_config.json")
			config = get_config_regression('tfn', 'sims')
			config['post_fusion_dim'] = 32
			outfilereal = "D://djangoproject/MSA/realtiming/feature.pkl"
			fet.run_single(in_file=infile2, text_file=realtimetext, out_file=outfilereal)
			config['featurePath'] = outfilereal
			# #fea = "/home/abc/data/wyy/MSA-FET-master/src/MSA_FET/feature/feature10_chinese.pkl"
			model = "D://djangoproject//MSA/MMSA/saved_models/tfn-sims.pth"
			num = MMSA_test(config, model, outfilereal, 0)
			print(num)

	return num
	# 	result.append(num)
	# 	# if result_num < -1 or result_num > 1:
	# 	# 	emo = "其他情绪"
	# 	# elif result_num < -0.7:
	# 	# 	emo = "愤怒"
	# 	# elif result_num < -0.4:
	# 	# 	emo = "焦虑"
	# 	# elif result_num < -0.1:
	# 	# 	emo = "疲惫"
	# 	# elif result_num < 0.1:
	# 	# 	emo = "中性"
	# 	# elif result_num < 0.4:
	# 	# 	emo = "轻松"
	# 	# elif result_num < 0.7:
	# 	# 	emo = "开心"
	# 	# else:
	# 	# 	emo = "兴奋"
	# 	#result.append(emo)·
	#
	# print("done")
	# print(result)
	# return result

def offlinedemo(infile1):
	filename = video2text(infile1)
	textfile1 = f"D://djangoproject//MSA/slicetext/{filename}/"
	fet = FeatureExtractionTool("D://djangoproject/MSA/MMSA-FET-master/src/MSA_FET/custom_config.json")
	config = get_config_regression('tfn', 'sims')
	config['post_fusion_dim'] = 32
	# feature1 = fet.run_single(in_file=infile1, text_file=textfile1, out_file=outfile1)
	# config['featurePath'] = outfile1
	#fea = "/home/abc/data/wyy/MSA-FET-master/src/MSA_FET/feature/feature10_chinese.pkl"
	model = "D://djangoproject//MSA/MMSA/saved_models/tfn-sims.pth"
	wav_files = glob.glob(os.path.join(textfile1, "*.txt"))
	result = []
	for text in wav_files:
		headname = os.path.basename(text)
		headname = headname.split(".")[0]
		invideo = f"D://djangoproject/MSA/slicevideo/{filename}/{headname}.mp4"
		intext = f"D://djangoproject/MSA/slicetext/{filename}/{headname}.txt"

		flag , duration=  is_video_complete(invideo)
		print(invideo+"检验结果为："+str(flag))
		if not flag:
			continue

		outfile1 = f"D://djangoproject/MSA/MSA-FET-master/src/MSA_FET/feature/feature{headname}.pkl"
		fet.run_single(in_file=invideo, text_file=intext, out_file=outfile1)
		result_num = MMSA_test(config, model, outfile1, 0)
		if result_num < -1 or result_num > 1:
			emo = "其他情绪"
		elif result_num < -0.7:
			emo = "愤怒"
		elif result_num < -0.4:
			emo = "焦虑"
		elif result_num < -0.1:
			emo = "疲惫"
		elif result_num < 0.1:
			emo = "中性"
		elif result_num < 0.4:
			emo = "轻松"
		elif result_num < 0.7:
			emo = "开心"
		else:
			emo = "兴奋"
		result.append(emo)
	print("done")
	print(result)
	return result





if __name__=="__main__":
	demo("D:/djangoproject/MSA/20230214-192557.mp4")
	# infileaudio = "E:/app/pycharm/PyCharm2020.1/pytest/djangoproject/MSA/sliceaudio/20221207-141735/20221207-141735_007.wav"
	# infilevideo = "E:/app/pycharm/PyCharm2020.1/pytest/djangoproject/MSA/slicevideo/20221207-141735/20221207-141735_007.mp4"
	# result = realtimedemo(infileaudio, infilevideo)
	# print(result)

