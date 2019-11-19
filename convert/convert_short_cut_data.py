import json
import argparse
def convert_data(data_file,read_data_file,save_file):
    with open(data_file,'r',encoding='utf-8') as f:
        with open(read_data_file, 'w',encoding='utf-8') as fout:
            data = json.load(f)['data']
            example_count = 0
            sync_shortcut = {'version': 'sync_shortcut', 'data': []}
            for para in data:
                if para['paragraphs']:
                    for p in para['paragraphs']:
                        for qa in p['qas']:
                            qp_pair = {}
                            fout.write(qa['question']+'\n')

                            qp_pair['question'] = qa['question']
                            query_index,para_index = qa['sync_pair'].keys(),qa['sync_pair'].values()
                            query_index = [i for i in query_index][0]
                            para_index = [i for i in para_index][0]
                            qp_pair['query_sync_tokens'] = int(query_index)

                            fout.write(p['doc_tokens_query'][int(query_index)] + '\n')

                            qp_pair['para_sync_tokens'] = [para_index]
                            fout.write(p['doc_tokens_para'][para_index] + ' ')

                            for i in range(1,len(p['doc_tokens_query'][int(query_index)])):
                                fout.write(p['doc_tokens_para'][int(para_index)+i] + ' ')
                                qp_pair['para_sync_tokens'].append(para_index+i)
                            qp_pair['paragraph'] = p['context']
                            fout.write('\n')
                            fout.write(p['context']+'\n')
                            fout.write('\n')
                            example_count += 1
                            sync_shortcut['data'].append(qp_pair)
            with open(save_file, 'w', encoding='utf-8') as fout:
                json.dump(sync_shortcut, fout)
            return example_count


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, default='')
    parser.add_argument('--read_data_file', required=True, default='')
    parser.add_argument('--save_file', required=True, default='')
    args = parser.parse_args()
    example_count = convert_data(args.data_file, args.read_data_file, args.save_file)
    print('convert %d sync_shortcut complete' % example_count)