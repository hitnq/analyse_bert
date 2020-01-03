import json
import argparse
from tqdm import tqdm
import re
import random
from nltk.tokenize import sent_tokenize

sentence = {'version': 'sentence_ranking_same_para', 'data': []}


def sentence_token_nltk(str):
    sent_tokenize_list = sent_tokenize(str)
    sent_start_pos = [0]
    for i, sent in enumerate(sent_tokenize_list):
        if sent_start_pos[-1] + len(sent) + 1 > len(str) - 1:
            break
        sent_start_pos.append(sent_start_pos[-1] + len(sent) + 1)
    return sent_tokenize_list, sent_start_pos


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
                sent_tokenize_list, start_pos = sentence_token_nltk(context)
                # start_pos = [m.start() for m in re.finditer(' \. ', context)]
                if len(start_pos) == 1:
                    continue
                assert len(sent_tokenize_list) == len(start_pos)
                if not start_pos:
                    continue
                qp_pair = {}
                qp_pair['query_sync_tokens'] = list(range(0, len(question.split())))
                for index, pos in enumerate(start_pos):
                    if answer_start < pos:
                        if index == 0 or index == 1:
                            qp_pair['para_sync_tokens'] = \
                                list(range(0, para['paragraphs'][0]['char_to_word_offset_para'][pos + 2] + 1))
                        else:
                            qp_pair['para_sync_tokens'] = \
                                list(range(
                                    para['paragraphs'][0]['char_to_word_offset_para'][start_pos[index - 1] + 2] + 1, \
                                    para['paragraphs'][0]['char_to_word_offset_para'][
                                        pos + 2 if pos + 2 < len(context) else pos + 1] + 1))
                        break
                if 'para_sync_tokens' not in qp_pair:
                    qp_pair['para_sync_tokens'] = \
                        list(range(para['paragraphs'][0]['char_to_word_offset_para'][start_pos[-1]], \
                                   para['paragraphs'][0]['char_to_word_offset_para'][len(context) - 1]))
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
                sent_tokenize_list, start_pos = sentence_token_nltk(context)
                # start_pos = [m.start() for m in re.finditer(' \. ', context)]
                if not start_pos:
                    continue
                answer_start = random.randint(0, len(context))
                sent_tokenize_list, start_pos = sentence_token_nltk(context)
                if len(start_pos) == 1:
                    continue
                assert len(sent_tokenize_list) == len(start_pos)
                while True:
                    random_index = random.randint(0,len(start_pos)-1)
                    if answer_start >= start_pos[random_index]:
                        if random_index != len(start_pos)-1 and answer_start >= start_pos[random_index + 1]:
                            break
                    else:
                        break
                qp_pair = {}
                qp_pair['query_sync_tokens'] = list(range(0, len(question.split())))
                for index, pos in enumerate(start_pos):
                    if start_pos[random_index] == pos:
                        qp_pair['para_sync_tokens'] = \
                            list(range(para['paragraphs'][0]['char_to_word_offset_para'][start_pos[index]],\
                                        para['paragraphs'][0]['char_to_word_offset_para'][start_pos[index+1] \
                                        if index+1 < len(start_pos) else len(context)-1]))

                        break
                if 'para_sync_tokens' not in qp_pair or qp_pair['para_sync_tokens']==[]:
                    qp_pair['para_sync_tokens'] = [para['paragraphs'][0]['char_to_word_offset_para'][start_pos[-1]]]
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, default='')
    parser.add_argument('--read_data_file', required=True, default='')
    parser.add_argument('--save_file', required=True, default='')
    parser.add_argument('--random_mode', action='store_true')
    args = parser.parse_args()
    if args.random_mode:
        example_count = convert_data_all_random(args.data_file, args.read_data_file, args.save_file)
    else:
        example_count = convert_data_all(args.data_file, args.read_data_file, args.save_file)
    print('convert %d new sentence complete' % example_count)
