import json
import argparse
from tqdm import tqdm
import re
import random
from nltk.tokenize import sent_tokenize

sentence = {'version': 'sentence_ranking', 'data': []}
all_para = []

def sentence_token_nltk(str):
    sent_tokenize_list = sent_tokenize(str)
    sent_start_pos = [0]
    for i,sent in enumerate(sent_tokenize_list):
        if sent_start_pos[-1]+len(sent)+1 > len(str)-1:
            break
        sent_start_pos.append(sent_start_pos[-1]+len(sent)+1)
    return sent_tokenize_list,sent_start_pos

def convert_data_all(data_file, read_data_file, save_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        with open(read_data_file, 'w', encoding='utf-8') as w:
            data = json.load(f)['data'][:10000]
            example_count = 0
            for para in tqdm(data):
                context = para['paragraphs'][0]['context']
                if len(context.split()) > 400:
                    continue
                question = para['paragraphs'][0]['qas'][0]['question']
                answer_start = para['paragraphs'][0]['qas'][0]['answer']['answer_start']
                sent_tokenize_list,start_pos = sentence_token_nltk(context)
                # start_pos = [m.start() for m in re.finditer(' \. ', context)]
                assert len(sent_tokenize_list) == len(start_pos)
                if not start_pos:
                    continue
                qp_pair = {}
                qp_pair['query_sync_tokens'] = list(range(0,len(question.split())))
                for index,pos in enumerate(start_pos):
                    if answer_start < pos:
                        if index == 0 or index == 1:
                            qp_pair['para_sync_tokens'] = \
                                list(range(0,para['paragraphs'][0]['char_to_word_offset_para'][pos+2]+1))
                        else:
                            qp_pair['para_sync_tokens'] = \
                                list(range(para['paragraphs'][0]['char_to_word_offset_para'][start_pos[index - 1]+2]+1,\
                                            para['paragraphs'][0]['char_to_word_offset_para'][pos+2 if pos+2<len(context) else pos+1]+1))
                        break
                if 'para_sync_tokens' not in qp_pair:
                    qp_pair['para_sync_tokens'] = \
                        list(range(para['paragraphs'][0]['char_to_word_offset_para'][start_pos[-1]], \
                                   para['paragraphs'][0]['char_to_word_offset_para'][len(context)-1]))
                w.write(question + '\n')
                if qp_pair['para_sync_tokens'] == []:
                    print(1)
                assert qp_pair['para_sync_tokens'] != []
                assert qp_pair['query_sync_tokens'] != []
                w.write(str(qp_pair['para_sync_tokens']) + '\n')
                w.write(str(qp_pair['query_sync_tokens']) + '\n')

                # w.write(str([p['doc_tokens_para'][i - len(qa['question'].split())] for i in qp_pair['para_sync_tokens']]) + ' ')
                qp_pair['question'] = question
                qp_pair['paragraph'] = context
                w.write(context + '\n')
                w.write('\n')
                sentence['data'].append(qp_pair)
                example_count += 1

        with open(save_file, 'w', encoding='utf-8') as fout:
            json.dump(sentence, fout)
        return example_count

class Random_pair(object):
    def __init__(self,context,char_to_word_offset_para):
        self.context = context
        self.char_to_word_offset_para = char_to_word_offset_para

def get_all_para(data_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)['data'][:10000]
        for para in tqdm(data):
            context = para['paragraphs'][0]['context']
            if len(context.split()) > 400:
                continue
            sent_tokenize_list, start_pos = sentence_token_nltk(context)
            assert len(sent_tokenize_list) == len(start_pos)
            if not start_pos:
                continue
            random_pair = Random_pair(context,para['paragraphs'][0]['char_to_word_offset_para'])
            all_para.append(random_pair)

def get_random_para():
    sent_num = random.randint(0,len(all_para)-1)
    return all_para[sent_num]

def convert_data_all_random(data_file, read_data_file, save_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        with open(read_data_file, 'w', encoding='utf-8') as w:
            data = json.load(f)['data'][:10000]
            example_count = 0
            for para in tqdm(data):
                context = para['paragraphs'][0]['context']
                if len(context.split()) > 400:
                    continue
                question = para['paragraphs'][0]['qas'][0]['question']
                sent_tokenize_list,start_pos = sentence_token_nltk(context)
                # start_pos = [m.start() for m in re.finditer(' \. ', context)]
                if not start_pos:
                    continue
                random_para = get_random_para()
                answer_start = random.randint(0,len(random_para.context))
                sent_tokenize_list, start_pos = sentence_token_nltk(random_para.context)
                assert len(sent_tokenize_list) == len(start_pos)

                qp_pair = {}
                qp_pair['query_sync_tokens'] = list(range(0,len(question.split())))
                for index,pos in enumerate(start_pos):
                    if answer_start < pos:
                        if index == 0 or index == 1:
                            qp_pair['para_sync_tokens'] = \
                                list(range(0,random_para.char_to_word_offset_para[pos+2]+1))
                        else:
                            qp_pair['para_sync_tokens'] = \
                                list(range(random_para.char_to_word_offset_para[start_pos[index - 1]+2]+1,\
                                            random_para.char_to_word_offset_para[pos+2 if pos+2<len(random_para.context) else pos+1]+1))
                        break
                if 'para_sync_tokens' not in qp_pair:
                    qp_pair['para_sync_tokens'] = \
                        list(range(random_para.char_to_word_offset_para[start_pos[-1]], \
                                   random_para.char_to_word_offset_para[len(random_para.context)-1]))
                w.write(question + '\n')
                if qp_pair['para_sync_tokens'] == []:
                    print(1)
                assert qp_pair['para_sync_tokens'] != []
                assert qp_pair['query_sync_tokens'] != []
                w.write(str(qp_pair['para_sync_tokens']) + '\n')
                w.write(str(qp_pair['query_sync_tokens']) + '\n')

                # w.write(str([p['doc_tokens_para'][i - len(qa['question'].split())] for i in qp_pair['para_sync_tokens']]) + ' ')
                qp_pair['question'] = question
                qp_pair['paragraph'] = random_para.context
                w.write(random_para.context + '\n')
                w.write('\n')
                sentence['data'].append(qp_pair)
                example_count += 1

        with open(save_file, 'w', encoding='utf-8') as fout:
            json.dump(sentence, fout)
        return example_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, default='')
    parser.add_argument('--read_data_file', required=True, default='')
    parser.add_argument('--save_file', required=True, default='')
    parser.add_argument('--random_mode', action='store_true')
    args = parser.parse_args()
    if args.random_mode:
        get_all_para(args.data_file)
        example_count = convert_data_all_random(args.data_file, args.read_data_file, args.save_file)
    else:
        example_count = convert_data_all(args.data_file, args.read_data_file, args.save_file)
    print('convert %d new sentence complete' % example_count)
