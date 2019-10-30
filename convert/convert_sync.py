import json
if __name__=='__main__':
    with open('/data/home/t-jicai/caijie/analyse_bert/data/sync_sync.json','r') as f:
        with open('./data/sync_sync/read_sync_data.txt', 'w') as w:
            data = json.load(f)['data']
            sync_sync = {'version': 'sync_sync', 'data': []}
            for para in data:
                if para['paragraphs']:
                    for p in para['paragraphs']:
                        for qa in p['qas']:
                            qp_pair = {}

                            w.write(qa['question']+'\n')
                            qp_pair['question'] = qa['question']

                            query_index, para_index = qa['sync_pair'].keys(), qa['sync_pair'].values()
                            query_index = [i for i in query_index][0]
                            para_index = [i for i in para_index][0]
                            qp_pair['query_sync_tokens'] = [query_index]
                            w.write(p['doc_tokens_query'][int(query_index)] + '\n')

                            qp_pair['para_sync_tokens'] = [para_index]
                            w.write(p['doc_tokens_para'][para_index] + ' ')

                            # w.write(p['doc_tokens_query'][int(str(qa['sync_pair'])[2])] +'\n')
                            # w.write(p['context'][int(str(qa['sync_pair'])[6]):int(str(qa['sync_pair'])[6])+10] + '\n')
                            qp_pair['paragraph'] = p['context']
                            w.write('\n')
                            # w.write(p['context'][int(str(qa['sync_pair'])[6]):int(str(qa['sync_pair'])[6])+10] + '\n')
                            w.write(p['context'] + '\n')
                            w.write('\n')
                            sync_sync['data'].append(qp_pair)
            with open('./data/sync_sync/sync_sync.json', 'w', encoding='utf-8') as fout:
                json.dump(sync_sync, fout)