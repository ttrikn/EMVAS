from transformers import BertTokenizerFast, BertModel
from ..baseExtractor import baseTextExtractor
import torch
import numpy as np


class bertExtractor(baseTextExtractor):
    """
    Text feature extractor using BERT
    Ref: https://huggingface.co/docs/transformers/model_doc/bert
    Pretrained models: https://huggingface.co/models
    """
    def __init__(self, config, logger):
        try:
            logger.info("Initializing BERT text feature extractor...")
            super().__init__(config, logger)
            self.device = self.config.get('device', torch.device('cpu'))
            self.tokenizer = BertTokenizerFast.from_pretrained(self.config['pretrained'])
            self.model = BertModel.from_pretrained(self.config['pretrained']).to(self.device)
            self.finetune = self.config.get('finetune', False)
        except Exception as e:
            logger.error("Failed to initialize bertExtractor.")
            raise e
    
    def extract(self, text):
        try:
            input_ids = self.tokenizer.encode(text, return_tensors='pt').to(self.device)
            # encoded_inputs = self.tokenizer(text, add_special_tokens=True, return_tensors='pt', padding='max_length', truncation=True, max_length=50).to(self.config['device'])
            with torch.no_grad():
                last_hidden_state = self.model(input_ids).last_hidden_state
                # last_hidden_state = self.model(encoded_inputs['input_ids'], encoded_inputs['attention_mask'], encoded_inputs['token_type_ids']).last_hidden_state
            return last_hidden_state.squeeze().cpu().numpy()
        except Exception as e:
            self.logger.error(f"Failed to extract text features with BERT for '{text}'.")
            raise e

    def tokenize(self, text):
        """
        For compatibility with feature files generated by MMSA DataPre.py

        Returns:
            input_ids: input_ids,
            input_mask: attention_mask,
            segment_ids: token_type_ids
        """
        try:
            # input_ids = self.tokenizer.encode(text, add_special_tokens=True)
            # input_ids = np.expand_dims(input_ids, 1)
            # input_mask = np.ones_like(input_ids)
            # segment_ids = np.zeros_like(input_ids)
            # text_bert = np.concatenate([input_ids, input_mask, segment_ids], axis=1)
            text_bert = self.tokenizer(text, add_special_tokens=True, return_tensors='np')
            text_bert = np.concatenate([text_bert['input_ids'].transpose(), text_bert['attention_mask'].transpose(), text_bert['token_type_ids'].transpose()], axis=1)
            return text_bert
        except Exception as e:
            self.logger.error(f"Failed to tokenize text with BERT for '{text}'.")
            raise e

    def get_word_ids(self, text) -> list:
        """
        Get word_id mapping for each token. 
        Words are split by space instead of tokenizer-specific settings which may include
        punctuations. This is for ASR compatibility.
        """
        try:
            encoding = self.tokenizer(text.split(), is_split_into_words=True)
            return encoding.word_ids()
        except Exception as e:
            self.logger.error(f"Failed to get tokens with BERT for '{text}'.")
            raise e