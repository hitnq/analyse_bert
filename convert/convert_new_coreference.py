import json
import argparse
from tqdm import tqdm
import re

coreference = {'version': 'coreference_new', 'data': []}
new_coref = {'version': 'coreference_new', 'data': []}
def convert_data_all(data_file, read_data_file, save_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        with open(read_data_file, 'a+', encoding='utf-8') as w:
            data = json.load(f)['data']
            example_count = 0
            for para in tqdm(data):
                context = para['paragraphs'][0]['context']
                question = para['paragraphs'][0]['qas'][0]['question']
                start_pos = [m.start() for m in re.finditer('``', context)]
                if not start_pos:
                    continue
                for pos in start_pos:
                    coref = ''
                    for index in range(pos + 3, len(context)):
                        if context[index] == "'":
                            coref = context[pos + 3:index - 1].lower()
                    if coref != '' and coref in question:
                        new_coref['data'].append(para)
                        example_count += 1

        #             p = para['paragraphs'][0]
        #             qa = p['qas'][0]
        #             qp_pair = {}
        #             qp_pair['question'] = qa['question']
        #
        #             query_index, para_index = qa['sync_pair'].keys(), qa['sync_pair'].values()
        #             query_index = [i for i in query_index][0]
        #             para_index = [i for i in para_index][0]
        #             # qp_pair['query_sync_tokens'] = [int(query_index)]
        #
        #             ans_token_pos = p['char_to_word_offset_para'][para_index]
        #             res = expand_sync(ans_token_pos, p['context'].split(), p['qas'][0]['answer']['text'])
        #             if res == -1:
        #                 continue
        #             else:
        #                 qp_pair['query_sync_tokens'] = [res + len(qa['question'].split())]
        #
        #             qp_pair['para_sync_tokens'] = [i + ans_token_pos + len(qa['question'].split()) for i in range(len(qa['answer']['text'].split()))]
        #             w.write(qa['question'] + '\n')
        #             # w.write(p['doc_tokens_para'][res])
        #             w.write(str(qp_pair['para_sync_tokens']) + '\n')
        #             w.write(str(qp_pair['query_sync_tokens']) + '\n')
        #
        #             # w.write(str([p['doc_tokens_para'][i - len(qa['question'].split())] for i in qp_pair['para_sync_tokens']]) + ' ')
        #
        #             qp_pair['paragraph'] = p['context']
        #             w.write(p['context'] + '\n')
        #             w.write('\n')
        #             coreference['data'].append(qp_pair)
        #             example_count += 1

        with open(save_file, 'w', encoding='utf-8') as fout:
            json.dump(new_coref, fout)
        return example_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, default='')
    parser.add_argument('--read_data_file', required=True, default='')
    parser.add_argument('--save_file', required=True, default='')
    args = parser.parse_args()
    example_count = convert_data_all(args.data_file, args.read_data_file, args.save_file)
    print('convert %d new coreference complete' % example_count)
