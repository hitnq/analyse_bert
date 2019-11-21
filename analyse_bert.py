import torch
import json
import numpy as np
import argparse
from tqdm import tqdm
import pickle
from pytorch_transformers import *

model_class = BertModel
tokenizer_class = BertTokenizer
sync_pair = set()
tsne_arrays = []
multihead_res = []


def get_query_para(qp_pair):
    question = qp_pair['question']
    query_idx = qp_pair['query_sync_tokens']
    paragraph = qp_pair['paragraph']
    para_idx = qp_pair['para_sync_tokens']
    return question, query_idx, paragraph, para_idx


def get_random_para(data, question):
    random_para = []
    for qp in data:
        para = qp['paragraph']
        query = qp['question']
        if query != question and len(para.split() + query.split()) < 512:
            random_para.append(para)
    res_para = random_para[np.random.randint(0, len(random_para), 1)[0]]
    return res_para, np.random.randint(0, len(res_para.split()), 1).tolist()


def get_random_para_WSC(paragraph):
    index_1 = np.random.randint(0, len(paragraph.split()), 1)[0]
    index_2 = np.random.randint(0, len(paragraph.split()), 1)[0]
    while index_1 == index_2 or paragraph.split()[index_1] == paragraph.split()[index_2]:
        index_1 = np.random.randint(0, len(paragraph.split()), 1)[0]
        index_2 = np.random.randint(0, len(paragraph.split()), 1)[0]
    return [index_1], [index_2]


def get_results(data_path, model_path, different_layer, look_embedding, tsne, distance, random_mode, multihead):
    results = []
    tokenizer = tokenizer_class.from_pretrained(model_path)
    if different_layer:
        if multihead:
            configer = BertConfig.from_pretrained(model_path)
            configer.__setattr__('get_multihead', True)
            configer.__setattr__('output_hidden_states', True)
            model = model_class.from_pretrained(model_path, config=configer)
        else:
            model = model_class.from_pretrained(model_path, output_hidden_states=True)
        if distance == 'cos':
            if not random_mode:
                if 'squad_bert_base' in model_path:
                    output_path = data_path.split('.')[0] + 'diff_res_squad_finetune_cos.txt'
                elif 'nq_bert_base' in args.model_path:
                    output_path = data_path.split('.')[0] + 'diff_res_nq_finetune_cos.txt'
                elif 'bert-base-uncased' in args.model_path:
                    output_path = data_path.split('.')[0] + 'diff_res_cos.txt'
            else:
                if 'squad_bert_base' in model_path:
                    output_path = data_path.split('.')[0] + 'diff_random_res_squad_finetune_cos.txt'
                elif 'nq_bert_base' in args.model_path:
                    output_path = data_path.split('.')[0] + 'diff_random_res_nq_finetune_cos.txt'
                elif 'bert-base-uncased' in args.model_path:
                    output_path = data_path.split('.')[0] + 'diff_random_res_cos.txt'
        elif distance == 'euc':
            if not random_mode:
                if 'squad_bert_base' in model_path:
                    output_path = data_path.split('.')[0] + 'diff_res_squad_finetune_euc.txt'
                elif 'nq_bert_base' in args.model_path:
                    output_path = data_path.split('.')[0] + 'diff_res_nq_finetune_euc.txt'
                elif 'bert-base-uncased' in args.model_path:
                    output_path = data_path.split('.')[0] + 'diff_res_euc.txt'
            else:
                if 'squad_bert_base' in model_path:
                    output_path = data_path.split('.')[0] + 'diff_random_res_squad_finetune_euc.txt'
                elif 'nq_bert_base' in args.model_path:
                    output_path = data_path.split('.')[0] + 'diff_random_res_nq_finetune_euc.txt'
                elif 'bert-base-uncased' in args.model_path:
                    output_path = data_path.split('.')[0] + 'diff_random_res_euc.txt'
    else:
        model = model_class.from_pretrained(model_path)
        output_path = data_path.split('.')[0] + '_res_squad_finetune_euc.txt'
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)['data'][:100]
    count = 0
    # two_embeddings = []
    for qp_pair in tqdm(data):
        question, query_idx, paragraph, para_idx = get_query_para(qp_pair)
        count += 1
        if random_mode:
            if 'WSC' in data_path:
                random_index_1, random_index_2 = get_random_para_WSC(paragraph)
                result = bert(question, random_index_1, paragraph, random_index_2,
                              model, tokenizer, different_layer, look_embedding, tsne, distance, multihead)
            else:
                random_para, random_index = get_random_para(data, question)
                result = bert(question, query_idx, paragraph, para_idx,
                              model, tokenizer, different_layer, look_embedding, tsne, distance, multihead,
                              random_para, random_index)
        else:
            result = bert(question, query_idx, paragraph, para_idx,
                          model, tokenizer, different_layer, look_embedding, tsne, distance, multihead)
        if not result:
            print(count)
            continue
        else:
            results.append(result[0])
            # two_embeddings.append(result[1])
    # import pickle
    # pickle.dump(two_embeddings,open('/data/caijie/analyse_bert/data/probing/bigram_shift/two_embedding.pickle','wb'))

    if tsne:
        from openTSNE import TSNE
        import pickle
        pickle.dump(np.array(tsne_arrays),
                    open('/data/home/t-jicai/caijie/analyse_bert/embedding_vector_tsne.pickle', 'wb'))
        res = TSNE().fit(np.array(tsne_arrays))
        with open('/data/home/t-jicai/caijie/analyse_bert/embedding_vector_tsne.txt', 'w', encoding='utf-8') as fout:
            for r in res:
                fout.write(str(r))
                fout.write('\n')
    with open(output_path, 'w', encoding='utf-8') as fout:
        for res in results:
            fout.write(str(res))
            fout.write('\n')


def get_sync_embedding(outputs, query_sync_token_idx, para_sync_token_idx):
    query_vec = []
    for i in range(len(query_sync_token_idx)):
        query_vec_single = []
        for j in query_sync_token_idx[i]:
            if query_vec_single == []:
                query_vec_single = outputs[j, :].numpy()
            else:
                query_vec_single += outputs[j, :].numpy()
        if query_vec == []:
            query_vec = query_vec_single / len(query_sync_token_idx[i])
        else:
            query_vec += query_vec_single / len(query_sync_token_idx[i])

    para_vec = []
    for i in range(len(para_sync_token_idx)):
        para_vec_single = []
        for j in para_sync_token_idx[i]:

            if para_vec_single == []:
                para_vec_single = outputs[j, :].numpy()
            else:
                para_vec_single += outputs[j, :].numpy()
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
    return cos


def get_dis(vec1, vec2):
    return np.linalg.norm(np.mat(vec1) - np.mat(vec2))


def bert(question, query_idx, paragraph, para_idx,
         model, tokenizer, different_layer, look_embedding, tsne, distance, multihead,
         random_para=None, random_index=None):
    query_idx = [int(item) for item in query_idx]
    para_idx = [int(item) for item in para_idx]
    paragraph = tokenizer.convert_tokens_to_string(tokenizer.tokenize(paragraph))
    question = tokenizer.convert_tokens_to_string(tokenizer.tokenize(question))
    qp_tokens_tokenizer = []
    query_tokens_tokenize = tokenizer.tokenize(question)
    para_tokens_tokenize = tokenizer.tokenize(paragraph)
    qp_tokens_tokenizer.extend(query_tokens_tokenize)
    qp_tokens_tokenizer.extend(para_tokens_tokenize)
    if len(qp_tokens_tokenizer) > 512:
        return []
    if random_para != None and random_index != None:
        random_para = tokenizer.convert_tokens_to_string(tokenizer.tokenize(random_para))
        para_tokens_tokenize = tokenizer.tokenize(random_para)
        query_tokens_tokenize.extend(para_tokens_tokenize)
        qp_tokens_tokenizer = query_tokens_tokenize
        paragraph = random_para
    input_ids = torch.tensor([tokenizer.convert_tokens_to_ids(qp_tokens_tokenizer)])
    qp_string = tokenizer.convert_tokens_to_string(qp_tokens_tokenizer)
    offset = []
    origin_tokens = question.split() + paragraph.split()
    j = 0
    cur_token = ''
    for i in range(len(qp_tokens_tokenizer)):
        if cur_token != '':
            cur_token += qp_tokens_tokenizer[i]
            if '##' in cur_token:
                cur_token = cur_token.replace('##', '')
        else:
            cur_token = qp_tokens_tokenizer[i]
        if not offset:
            if qp_tokens_tokenizer[i].lower() == origin_tokens[j].lower():
                offset = [0]
                j += 1
                cur_token = ''
            else:
                offset = [0]
            continue
        if cur_token != origin_tokens[j].lower() and cur_token != '[UNK]':
            if qp_tokens_tokenizer[i].startswith('##'):
                offset.append(j)
            else:
                offset.append(j)
        else:
            offset.append(j)
            j += 1
            cur_token = ''
    if random_para != None and random_index != None:
        para_idx_add_query = [i + len(question.split()) for i in random_index]
    else:
        para_idx_add_query = [i + len(question.split()) for i in para_idx]
    with torch.no_grad():
        try:
            query_token_idx = list(map(lambda x: offset.index(x), query_idx))
            para_token_idx = list(map(lambda x: offset.index(x), para_idx_add_query))
        except:
            return []
        query_sync_token_idx = []
        para_sync_token_idx = []
        for i in query_token_idx:
            token_index = [i]
            if i + 1 >= len(offset) - 1:
                query_sync_token_idx = [token_index]
                break
            for j in range(i + 1, len(offset)):
                if offset[j] == i:
                    token_index.append(j)
                else:
                    query_sync_token_idx.append(token_index)
                    break

        for i in para_token_idx:
            token_index = [i]
            if i + 1 >= len(offset) - 1:
                para_sync_token_idx = [token_index]
                break
            for j in range(i + 1, len(offset)):
                if offset[j] == i:
                    token_index.append(j)
                else:
                    para_sync_token_idx.append(token_index)
                    break
        assert query_sync_token_idx != []
        assert para_sync_token_idx != []
        model_outputs = model(input_ids)
        if different_layer:
            if multihead:
                multihead_res.append({'query_token': query_sync_token_idx,
                                      'para_token': para_sync_token_idx,
                                      'multihead': model_outputs[-1]})
            outputs_all = model_outputs[2]
            sims = []
            two_embeddings = []
            for outputs in outputs_all[:-1]:
                outputs = torch.squeeze(outputs, 0)
                query_token_embedding, para_token_embedding = get_sync_embedding(outputs,
                                                                                 query_sync_token_idx,
                                                                                 para_sync_token_idx)
                two_embeddings.append([query_token_embedding,para_token_embedding])
                if distance == 'cos':
                    sim = get_cos_sim(query_token_embedding, para_token_embedding)
                    sims.append(sim)
                elif distance == 'euc':
                    sim = get_dis(query_token_embedding, para_token_embedding)
                    sims.append(sim)
            return (sims,two_embeddings)
        else:
            outputs = model_outputs[0]
            outputs = torch.squeeze(outputs, 0)
            if look_embedding:
                with open('/data/home/t-jicai/caijie/analyse_bert/embedding_vector_nq.txt', 'w',
                          encoding='utf-8') as fout:
                    fout.write(str(qp_tokens_tokenizer) + '\n')
                    for i in range(outputs.size(0)):
                        fout.write(str(outputs[i][:].numpy().tolist()) + '\n')
                exit()
            query_token_embedding, para_token_embedding = get_sync_embedding(outputs, query_sync_token_idx,
                                                                             para_sync_token_idx)

            if not query_token_embedding or not para_token_embedding:
                print(1)
            if tsne:
                tsne_arrays.append(query_token_embedding)
                tsne_arrays.append(para_token_embedding)
            if distance == 'cos':
                sim = get_cos_sim(query_token_embedding, para_token_embedding)
                return (sim,)
            elif distance == 'euc':
                sim = get_dis(query_token_embedding, para_token_embedding)
                return (sim,)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', default='')
    parser.add_argument('--model_path', default='')
    parser.add_argument('--different_layer', action='store_true', help='output bert different layer results')
    parser.add_argument('--look_embedding', action='store_true', help='look sentence token embedding')
    parser.add_argument('--t_sne', action='store_true', help='use t-sne to deduce dimension')
    parser.add_argument('--distance', type=str, default='cos', required=True,
                        help='use cos similarity or Euclidean distance')
    parser.add_argument('--random_mode', action='store_true', help='select random paragraph and random index')
    parser.add_argument('--multihead', action='store_true', help='see multihead or not')
    args = parser.parse_args()
    get_results(args.data_file,
                args.model_path,
                args.different_layer,
                args.look_embedding,
                args.t_sne,
                args.distance,
                args.random_mode,
                args.multihead)
    data_path = '/'.join(args.data_file.split('/')[:-1])
    if args.multihead:
        if args.random_mode:
            if 'squad_bert_base' in args.model_path:
                pickle.dump(multihead_res, open(data_path + '/multihead_squad_finetune_random.pickle', 'wb'))
            elif 'nq_bert_base' in args.model_path:
                pickle.dump(multihead_res,open(data_path + '/multihead_nq_finetune_random.pickle','wb'))
            elif 'bert-base-uncased' in args.model_path:
                pickle.dump(multihead_res,open(data_path + '/multihead_random.pickle','wb'))

        else:
            if 'squad_bert_base' in args.model_path:
                pickle.dump(multihead_res, open(data_path + '/multihead_squad_finetune.pickle', 'wb'))
            elif 'nq_bert_base' in args.model_path:
                pickle.dump(multihead_res,open(data_path + '/multihead_nq_finetune.pickle','wb'))
            elif 'bert-base-uncased' in args.model_path:
                pickle.dump(multihead_res,open(data_path + '/multihead.pickle','wb'))

# /data/caijie/analyse_bert/models/nq_bert_base
# /data/home/t-jicai/caijie/analyse_bert/data/nq/ask_type/ask_type.json
