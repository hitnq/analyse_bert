import json
data = []
with open('./data/sync_sync/sync_sync_squad.json','r',encoding='utf-8') as fin:
    data = json.load(fin)['data']
qp_set = set()
new_sync_data = {'version':'sync_sync','data':[]}
for pair in data:
    question = pair['question']
    paragraph = pair['paragraph']
    question_token = pair['query_sync_tokens']
    paragraph_token = pair['para_sync_tokens'][0]
    combine = ''
    combine += question.split()[question_token]
    combine += paragraph.split()[paragraph_token]
    if question.split()[question_token] == paragraph.split()[paragraph_token] or \
            question.split()[question_token].lower() == paragraph.split()[paragraph_token].lower() or\
            question.split()[question_token].lower()+'s' == paragraph.split()[paragraph_token].lower() or\
            question.split()[question_token].lower() == paragraph.split()[paragraph_token].lower()+'s' or\
            question.split()[question_token].lower()+'ed' == paragraph.split()[paragraph_token].lower() or\
            question.split()[question_token].lower() == paragraph.split()[paragraph_token].lower()+'ed':
        continue
    if combine in qp_set:
        continue
    else:
        qp_set.add(combine)
        pair['query_sync_tokens'] = [pair['query_sync_tokens']]
        new_sync_data['data'].append(pair)
        print(question.split()[question_token])
        print(paragraph.split()[paragraph_token])
print(len(new_sync_data['data']))
with open('./data/sync_sync/sync_sync_new_squad.json','w',encoding='utf-8') as fout:
    json.dump(new_sync_data,fout)