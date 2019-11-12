import json
import argparse
from tqdm import tqdm
def convert_data(data_file,read_data_file,save_file):
    WSC_data = {'version':'WSC_coreference','data':[]}
    example_count = 0
    with open(data_file,'r',encoding='utf-8') as fin:
        with open(read_data_file, 'w', encoding='utf-8') as fout:
            for example in tqdm(fin.readlines()):
                qp_pair = {}
                data = json.loads(example)
                if data['label'] and len(data['text'].split()) < 512:
                    qp_pair['question'] = ''
                    fout.write(qp_pair['question'] + '\n')
                    query_token_list = [data['target']['span1_index']+i for i in range(len(data['target']['span1_text'].split()))]
                    para_token_list = [data['target']['span2_index']+i for i in range(len(data['target']['span2_text'].split()))]
                    qp_pair['query_sync_tokens'] = query_token_list
                    qp_pair['paragraph'] = data['text']
                    qp_pair['para_sync_tokens'] = para_token_list
                    fout.write(str(qp_pair['query_sync_tokens']) + ' ')
                    for i in qp_pair['query_sync_tokens']:
                        fout.write(qp_pair['paragraph'].split()[i]+' ')
                    fout.write(str(qp_pair['para_sync_tokens']) + ' ')
                    for i in qp_pair['para_sync_tokens']:
                        fout.write(qp_pair['paragraph'].split()[i]+' ')
                    fout.write('\n')
                    fout.write(qp_pair['paragraph'])
                    fout.write('\n')
                    fout.write('\n')
                    WSC_data['data'].append(qp_pair)
                    example_count += 1
        with open(save_file, 'w', encoding='utf-8') as fout:
            json.dump(WSC_data, fout)
        return example_count

if __name__=='__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--data_file',required=True,help='WSC data file path')
    argparser.add_argument('--read_data_file',required=True,help='read WSC data')
    argparser.add_argument('--save_file',required=True,help='save file path')
    args = argparser.parse_args()
    example_count = convert_data(args.data_file,args.read_data_file,args.save_file)
    print('convert %d WSC examples completed!' % example_count)