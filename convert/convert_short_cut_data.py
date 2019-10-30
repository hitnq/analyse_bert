import json
if __name__=='__main__':
    with open('/data/home/t-jicai/caijie/analyse_bert/sync_shortcut.json','r',encoding='utf-8') as f:
        with open('./data/sync_shortcut/read_shortcut_data.txt', 'w',encoding='utf-8') as fout:
            data = json.load(f)['data']
            sync_shortcut = {'version': 'sync_shortcut', 'data': []}
            for para in data:
                if para['paragraphs']:
                    for p in para['paragraphs']:
                        for qa in p['qas']:
                            qp_pair = {}
                            # fout.write(qp_pair['question'] + '\n')
                            #
                            # fout.write(str(qp_pair['query_sync_tokens']) + ' ')
                            # for idx in qp_pair['query_sync_tokens']:
                            #     fout.write(qp_pair['question'].split()[idx] + ' ')
                            # fout.write('\n')
                            #
                            # fout.write(qp_pair['paragraph'] + '\n')
                            #
                            # fout.write(str(qp_pair['para_sync_tokens']) + ' ')
                            # for idx in qp_pair['para_sync_tokens']:
                            #     fout.write(qp_pair['paragraph'].split()[idx] + ' ')
                            # fout.write('\n')
                            # fout.write(attribute['answer_text'])
                            # fout.write('\n')
                            # fout.write('\n')
                            #
                            # sync_part['data'].append(qp_pair)

                            fout.write(qa['question']+'\n')

                            qp_pair['question'] = qa['question']
                            query_index,para_index = qa['sync_pair'].keys(),qa['sync_pair'].values()
                            query_index = [i for i in query_index][0]
                            para_index = [i for i in para_index][0]
                            qp_pair['query_sync_tokens'] = int(query_index)

                            fout.write(p['doc_tokens_query'][int(query_index)] + '\n')
                            # fout.write(qa['question'].strip().split()[int(query_index)] + '\n')

                            qp_pair['para_sync_tokens'] = [para_index]
                            fout.write(p['doc_tokens_para'][para_index] + ' ')

                            for i in range(1,len(p['doc_tokens_query'][int(query_index)])):
                                fout.write(p['doc_tokens_para'][int(para_index)+i] + ' ')
                                qp_pair['para_sync_tokens'].append(para_index+i)
                            qp_pair['paragraph'] = p['context']
                            fout.write('\n')
                            # w.write(p['context'][int(str(qa['sync_pair'])[6]):int(str(qa['sync_pair'])[6])+10] + '\n')
                            fout.write(p['context']+'\n')
                            fout.write('\n')
                            sync_shortcut['data'].append(qp_pair)
            with open('./data/sync_shortcut.json', 'w', encoding='utf-8') as fout:
                json.dump(sync_shortcut, fout)