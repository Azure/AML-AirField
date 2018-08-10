import sys, os
import json
import csv
import numpy as np
from aml_response  import AMLResponse

from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH

def init():
    global sentence_tokenizer
    global model
    global emoji_desc, emoji_unicode

    max_token = 30
    with open(VOCAB_PATH, 'r') as f:
        vocabulary = json.load(f)
    
    sentence_tokenizer = SentenceTokenizer(vocabulary, max_token)
    model = torchmoji_emojis(PRETRAINED_PATH)

    with open('data/emoji_codes.json') as f:
        emoji_desc = json.load(f)

    with open('data/wanted_emojis.csv') as f:
        emoji_unicode = list(csv.reader(f))


def run(request):
    try:
        input = request.get_data(False).decode('utf-8')
        tokenized, _, _ = sentence_tokenizer.tokenize_sentences([input])
        prob = model(tokenized)
    
        t_tokens = tokenized[0]
        t_score = [input]
        t_prob = prob[0]        
        
        top_k = 5
        ind = np.argpartition(t_prob, -top_k)[-top_k:]
        ind_top = ind[np.argsort(t_prob[ind])][::-1]
        
        # Match emoji description
        t_emojis = [emoji_desc[str(ind)] for ind in ind_top]
        # Match emoji unicode
        t_unicode = [emoji_unicode[ind][0] for ind in ind_top]

        t_score.append(sum(t_prob[ind_top]).item())
        t_score.extend(t_emojis)
        t_score.extend(t_unicode)
        t_score.extend([t_prob[ind].item() for ind in ind_top])

        return t_score

    except Exception as e:
        return str(e)

