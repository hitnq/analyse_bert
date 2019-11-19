import json
import argparse

def convert_data(data_file,read_data_file,save_file):
    with open(data_file, 'r', encoding='utf-8') as fin:
        data = json.loads(fin.readline())
        sync_part = {'version': 'sync_part', 'data': []}
        example_count = 0
        with open(read_data_file, 'w',
                  encoding='utf-8') as fout:
            for id, attribute in data.items():
                qp_pair = {}
                if attribute['question_tokens'][0][0] != 'who' and \
                    attribute['question_tokens'][0][0] != 'where'and \
                    attribute['question_tokens'][0][0] != 'when':
                    continue
                qp_pair['question'] = ' '.join([token[0] for token in attribute['question_tokens']])
                fout.write(qp_pair['question'] + '\n')
                qp_pair['query_sync_tokens'] = [0]
                fout.write(str(qp_pair['query_sync_tokens']) + ' ')
                for idx in qp_pair['query_sync_tokens']:
                    fout.write(qp_pair['question'].split()[idx] + ' ')
                fout.write('\n')
                qp_pair['paragraph'] = attribute['paragraph']
                fout.write(qp_pair['paragraph'] + '\n')

                answer_len = len(attribute['answer_text'].split())
                ans_char_pos = qp_pair['paragraph'].index(attribute['answer_text'])
                ans_token_pos = attribute['paragraph_offset'][ans_char_pos]
                qp_pair['para_sync_tokens'] = [i+ans_token_pos for i in range(answer_len)]
                fout.write(str(qp_pair['para_sync_tokens']) + ' ')
                for idx in qp_pair['para_sync_tokens']:
                    fout.write(qp_pair['paragraph'].split()[idx] + ' ')
                fout.write('\n')
                fout.write(attribute['answer_text'])
                fout.write('\n')
                fout.write('\n')
                example_count += 1
                sync_part['data'].append(qp_pair)
    with open(save_file, 'w', encoding='utf-8') as fout:
        json.dump(sync_part, fout)
    return example_count

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, default='')
    parser.add_argument('--read_data_file', required=True, default='')
    parser.add_argument('--save_file', required=True, default='')
    args = parser.parse_args()
    example_count = convert_data(args.data_file, args.read_data_file, args.save_file)
    print('convert %d ask_type complete' % example_count)