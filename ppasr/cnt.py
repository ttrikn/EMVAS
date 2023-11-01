import cntext as ct

# print(ct.load_pkl_dict('HOWNET.pkl'))

diction = {'积极': ['高兴', '快乐', '分享'],
          '消极': ['难过', '悲伤'],
          '副词': ['很', '特别']}

# text = '女说咱们上大学之后还能下现在怎么好吗'
text = '我今天得奖了，很高兴，我要将快乐分享大家。'
# print(ct.sentiment(text=text, diction=diction, lang='chinese'))
# print(ct.sentiment(text=text, diction=ct.load_pkl_dict('HOWNET.pkl')['HOWNET'], lang='chinese'))

# dict1 = ct.sentiment(text=text,
#                      # diction=ct.load_pkl_dict('DUTIR.pkl')['DUTIR'],
#                      diction=ct.load_pkl_dict('HOWNET.pkl')['HOWNET'],
#                      lang='chinese')
# print(dict1)
###情绪识别
dict1 = ct.sentiment(text=text,
                     # diction=ct.load_pkl_dict('DUTIR.pkl')['DUTIR'],
                     diction=diction,
                     # diction=ct.load_pkl_dict('HOWNET.pkl')['HOWNET'],
                     lang='chinese')
print('dict1 : ',dict1)
new_dict1 = {}
for i, (k, v) in enumerate(dict1.items()):
    new_dict1[k] = v
    if i == 2:
        # print(new_dict1)
        break
print(new_dict1)
# print(sorted(new_dict1.items(), key=lambda x: x[1]))
max_dict1 = sorted(new_dict1.items(), key=lambda x: x[1])[
    len(sorted(new_dict1.items(), key=lambda x: x[1])) - 1]
print(max_dict1)
