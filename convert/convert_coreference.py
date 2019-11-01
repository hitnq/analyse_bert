import json
dict = {'7841177184804949328':{'co_query':[0,1],'co_para':[45,46]},
'427969558370580025':{'co_query':[0,1],'co_para':[41]}
}

with open('/data/home/t-jicai/caijie/analyse_bert/data/nq/qas_is_sync.json', 'r',encoding='utf-8') as fin:
    data = json.loads(fin.readline())
    sync_part = {'version':'sync_part','data':[]}
    with open('/data/home/t-jicai/caijie/analyse_bert/data/nq/coreference/read_coreference.txt','w',encoding='utf-8') as fout:
        for id, attribute in data.items():
            qp_pair = {}
            if id in dict:
                qp_pair['question'] = ' '.join([token[0] for token in attribute['question_tokens']])
                fout.write(qp_pair['question']+'\n')
                qp_pair['query_sync_tokens'] = dict[id]['co_query']
                fout.write(str(qp_pair['query_sync_tokens']) + ' ')
                for idx in qp_pair['query_sync_tokens']:
                    fout.write(qp_pair['question'].split()[idx] + ' ')
                qp_pair['query_sync_tokens'] = [i+len(attribute['question_tokens']) for i in qp_pair['query_sync_tokens']]
                fout.write(str(qp_pair['query_sync_tokens']) + ' ')
                fout.write('\n')
                qp_pair['paragraph'] = attribute['paragraph']
                fout.write(qp_pair['paragraph'] + '\n')
                qp_pair['para_sync_tokens'] = dict[id]['co_para']
                fout.write(str(qp_pair['para_sync_tokens']) + ' ')
                for idx in qp_pair['para_sync_tokens']:
                    fout.write(qp_pair['paragraph'].split()[idx] + ' ')
                fout.write('\n')
                fout.write(attribute['answer_text'])
                fout.write('\n')
                fout.write('\n')
                sync_part['data'].append(qp_pair)
    with open('/data/home/t-jicai/caijie/analyse_bert/data/nq/coreference/coreference.json', 'w', encoding='utf-8') as fout:
        json.dump(sync_part,fout)






