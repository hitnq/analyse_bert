import torch
import json
import numpy as np
import argparse
from tqdm import tqdm
from pytorch_transformers import *
model_class = BertModel
tokenizer_class = BertTokenizer
sync_pair = set()

def get_query_para(qp_pair):
    question = qp_pair['question']
    query_idx = qp_pair['query_sync_tokens']
    paragraph = qp_pair['paragraph']
    para_idx = qp_pair['para_sync_tokens']
    return question,query_idx,paragraph,para_idx

def get_results(data_path,model_path,different_layer):
    results = []
    if different_layer:
        output_path = data_path.split('.')[0] + 'diff_res_nq_finetune.txt'
    else:
        output_path = data_path.split('.')[0] + '_res.txt'
    with open(data_path,'r',encoding='utf-8') as f:
        data = json.load(f)['data'][0:100]
    for qp_pair in tqdm(data):
        question,query_idx,paragraph,para_idx = get_query_para(qp_pair)
        query_tokens = question.split()
        para_tokens = paragraph.split()
        combine_tokens = ''
        # for idx in query_idx:
        #     combine_tokens += query_tokens[idx]
        # for idx in para_idx:
        #     combine_tokens += para_tokens[idx]
        # if combine_tokens in sync_pair:
        #     continue
        # else:
        #     sync_pair.add(combine_tokens)

        result = bert(question,query_idx,paragraph,para_idx,model_path,different_layer)
        if not result:
            continue
        else:
            results.append(result)
    with open(output_path,'w',encoding='utf-8') as fout:
        for res in results:
            fout.write(str(res))
            fout.write('\n')

def get_sync_embedding(outputs, query_sync_token_idx, para_sync_token_idx):
    query_vec = []
    for i in range(len(query_sync_token_idx)):
        query_vec_single = []
        for j in query_sync_token_idx[i]:
            if query_vec_single == []:
                query_vec_single = outputs[j,:].numpy()
            else:
                query_vec_single += outputs[j,:].numpy()
        if query_vec == []:
            query_vec = query_vec_single / len(query_sync_token_idx[i])
        else:
            query_vec += query_vec_single / len(query_sync_token_idx[i])

    para_vec = []
    for i in range(len(para_sync_token_idx)):
        para_vec_single = []
        for j in para_sync_token_idx[i]:
            try:
                if para_vec_single == []:
                    para_vec_single = outputs[j, :].numpy()
                else:
                    para_vec_single += outputs[j, :].numpy()
            except:
                print(1)
        if para_vec == []:
            para_vec = para_vec_single / len(para_sync_token_idx[i])
        else:
            para_vec += para_vec_single / len(para_sync_token_idx[i])

    return [vec / len(query_sync_token_idx) for vec in query_vec], \
           [vec / len(para_sync_token_idx) for vec in para_vec]

def get_cos_sim(vector_a, vector_b):
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim

def get_dis(vec1,vec2):
    return np.linalg.norm(vec1 - vec2)

def bert(question,query_idx,paragraph,para_idx,model_path,different_layer):
    tokenizer = tokenizer_class.from_pretrained(model_path)
    if different_layer:
        model = model_class.from_pretrained(model_path,output_hidden_states=True)
    else:
        model = model_class.from_pretrained(model_path)
    query_tokens_tokenize = tokenizer.tokenize(question)
    para_tokens_tokenize = tokenizer.tokenize(paragraph)
    query_tokens_tokenize.extend(para_tokens_tokenize)
    qp_tokens_tokenizer = query_tokens_tokenize
    if len(qp_tokens_tokenizer) > 512:
        return []
    input_ids = torch.tensor([tokenizer.convert_tokens_to_ids(qp_tokens_tokenizer)])
    qp_string = tokenizer.convert_tokens_to_string(qp_tokens_tokenizer)
    offset = []
    origin_tokens = question.split()+paragraph.split()
    j = 0
    cur_token = ''
    for i in range(len(qp_tokens_tokenizer)):
        if cur_token != '':
            cur_token += qp_tokens_tokenizer[i]
            if '##' in cur_token:
                cur_token = cur_token.replace('##','')
        else:
            cur_token = qp_tokens_tokenizer[i]
        if not offset:
            if qp_tokens_tokenizer[i].lower()==origin_tokens[j].lower():
                offset = [0]
                j += 1
                cur_token = ''
            else:
                offset = [0]
            continue
        if cur_token != origin_tokens[j].lower():
            if qp_tokens_tokenizer[i].startswith('##'):
                offset.append(j)
            else:
                offset.append(j)
        else:
            offset.append(j)
            j += 1
            cur_token = ''
    para_idx_add_query = [i + len(question.split()) for i in para_idx]
    with torch.no_grad():
        try:
            query_token_idx = list(map(lambda x:offset.index(x),query_idx))
            para_token_idx = list(map(lambda x:offset.index(x),para_idx_add_query))
        except:
            return []
        query_sync_token_idx = []
        para_sync_token_idx = []
        for i in query_token_idx:
            token_index = [i]
            for j in range(i+1,len(offset)):
                if offset[j] == i:
                    token_index.append(j)
                else:
                    query_sync_token_idx.append(token_index)
                    break

        for i in para_token_idx:
            token_index = [i]
            for j in range(i + 1, len(offset)):
                if offset[j] == i:
                    token_index.append(j)
                else:
                    para_sync_token_idx.append(token_index)
                    break
        if different_layer:
            outputs_all = model(input_ids)[2]
            cos_sims = []
            for outputs in outputs_all[:-1]:
                outputs = torch.squeeze(outputs, 0)
                query_token_embedding, para_token_embedding = get_sync_embedding(outputs,
                                                                                 query_sync_token_idx,
                                                                                 para_sync_token_idx)
                cos_sim = get_cos_sim(query_token_embedding, para_token_embedding)
                cos_sims.append(cos_sim)
            return cos_sims
        else:
            outputs = model(input_ids)[0]
            outputs = torch.squeeze(outputs, 0)

            query_token_embedding,para_token_embedding = get_sync_embedding(outputs,query_sync_token_idx,para_sync_token_idx)
            cos_sim = get_cos_sim(query_token_embedding,para_token_embedding)
            return cos_sim

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', default='')
    parser.add_argument('--model_path', default='')
    parser.add_argument('--different_layer',action='store_true', help='output bert different layer results')
    args = parser.parse_args()
    get_results(args.data_file,args.model_path,args.different_layer)

#/data/home/t-jicai/caijie/analyse_bert/data/models/nq_bert_base
