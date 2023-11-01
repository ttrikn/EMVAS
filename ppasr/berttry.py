import torch
import argparse
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer
global emotiontext
import time

# args = parse_args()
# device = torch.device(args.device)
device = torch.device("cpu")
model = AutoModelForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=6)
print(f'Loading checkpoint:  ...')
# checkpoint = torch.load(args.model_path)
checkpoint = torch.load('wb/best.pt', map_location='cpu')
missing_keys, unexpected_keys = model.load_state_dict(checkpoint['state_dict'], strict=True)
print(f'missing_keys: {missing_keys}\n'
      f'===================================================================\n')
print(f'unexpected_keys: {unexpected_keys}\n'
      f'===================================================================\n')

label = {0: '快乐', 1: '愤怒', 2: '悲伤', 3: '恐惧', 4: '惊讶', 5: '中性'}
tokenizer = AutoTokenizer.from_pretrained('bert-base-chinese')
token = tokenizer('你是不是有病', padding='max_length', truncation=True, max_length=140)
# token = tokenizer(args.input, padding='max_length', truncation=True, max_length=140)
input_ids = torch.tensor(token['input_ids']).unsqueeze(0)
model.eval()
model.to(device)
input_ids.to(device)
with torch.no_grad():
    output = model(input_ids)
pred = np.argmax(output.logits.detach().cpu().numpy(), axis=1).tolist()[0]
print(f'##################### result: {label[pred]} #####################')

