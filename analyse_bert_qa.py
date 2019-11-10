import torch
import json
import numpy as np
import argparse
import pickle
from tqdm import tqdm
from pytorch_transformers import *
model_class = BertForQuestionAnswering
tokenizer_class = BertTokenizer
sync_pair = set()
tsne_arrays = []
def get_query_para(qp_pair):
    question = qp_pair['question']
    #query_idx = [int(qp_pair['query_sync_tokens'][0])]
    query_idx = qp_pair['query_sync_tokens']
    paragraph = qp_pair['paragraph']
    para_idx = qp_pair['para_sync_tokens']
    return question,query_idx,paragraph,para_idx

def get_results(data_path,model_path):
    results = {}
    output_path = data_path.split('.')[0] + '_res_nq_finetune_qa.pickle'
    with open(data_path,'r',encoding='utf-8') as f:
        data = json.load(f)['data'][:1]
    for qp_pair in tqdm(data):
        question,query_idx,paragraph,para_idx = get_query_para(qp_pair)
        start_logits,end_logits,qp_tokens_tokenizer = bert(question,query_idx,paragraph,para_idx,model_path)
        results[' '.join(qp_tokens_tokenizer)] = (start_logits,end_logits)

    pickle.dump(results,open(output_path,'wb'))

def get_dis(vec1,vec2):
    return np.linalg.norm(vec1 - vec2)

def bert(question,query_idx,paragraph,para_idx,model_path):
    tokenizer = tokenizer_class.from_pretrained(model_path)
    model = model_class.from_pretrained(model_path)
    query_tokens_tokenize = ['[CLS]']
    para_tokens_tokenize = ['[SEP]']
    query_tokens_tokenize.extend(tokenizer.tokenize(question))
    para_tokens_tokenize.extend(tokenizer.tokenize(paragraph))
    query_tokens_tokenize.extend(para_tokens_tokenize)
    qp_tokens_tokenizer = query_tokens_tokenize
    qp_tokens_tokenizer.extend(['[SEP]'])
    if len(qp_tokens_tokenizer) > 512:
        return
    input_ids = torch.tensor([tokenizer.convert_tokens_to_ids(qp_tokens_tokenizer)])
    # qp_string = tokenizer.convert_tokens_to_string(qp_tokens_tokenizer)
    with torch.no_grad():
        outputs = model(input_ids)
        start_logits = torch.squeeze(outputs[0], 0).numpy().tolist()
        end_logits = torch.squeeze(outputs[1], 0).numpy().tolist()
        return start_logits,end_logits,qp_tokens_tokenizer

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', default='')
    parser.add_argument('--model_path', default='')
    args = parser.parse_args()
    get_results(args.data_file,args.model_path)

#/data/home/t-jicai/caijie/analyse_bert/data/models/nq_bert_base
#/data/home/t-jicai/caijie/analyse_bert/data/nq/ask_type/ask_type.json
