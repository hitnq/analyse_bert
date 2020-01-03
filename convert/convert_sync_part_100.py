import json
import argparse

dict = {'-1936643027092382569': {'sync_query': [8, 9], 'sync_para': [19]},
        '-384048589792328422': {'sync_query': [13, 14], 'sync_para': [6]},
        '-7868511982046979937': {'sync_query': [7], 'sync_para': [22]},
        '-267370223438082630': {'sync_query': [1], 'sync_para': [13]},
        '-911941420321650021': {'sync_query': [6, 7], 'sync_para': [17, 18]},
        '1422903471239876802': {'sync_query': [1, 2], 'sync_para': [118]},
        '1810372956287276049': {'sync_query': [3, 4], 'sync_para': [1, 2, 3]},
        '-329823809464222133': {'sync_query': [4], 'sync_para': [49, 50, 51]},
        '-3071962219115388524': {'sync_query': [1], 'sync_para': [4, 5]},
        '1309551455514971810': {'sync_query': [6, 7, 8], 'sync_para': [20, 21]},
        '-1168989793403787752': {'sync_query': [7, 8], 'sync_para': [14]},
        '-3597961506867638003': {'sync_query': [1], 'sync_para': [101]},
        '4524621993123037311': {'sync_query': [5, 6, 7], 'sync_para': [35, 36]},
        '-3868678027793136551': {'sync_query': [1], 'sync_para': [46, 47, 48]},
        '3592887855495641220': {'sync_query': [8], 'sync_para': [3]},
        '-3068125462410496906': {'sync_query': [1], 'sync_para': [168]},
        '-7468861661154309979': {'sync_query': [9], 'sync_para': [71]},
        '6709349913690237888': {'sync_query': [1], 'sync_para': [56]},
        '8191106171720881704': {'sync_query': [5, 6, 7], 'sync_para': [134, 135]},
        '-3299627514945841716': {'sync_query': [7, 8], 'sync_para': [3]},
        '-181305449522045818': {'sync_query': [1], 'sync_para': [16, 17, 18]},
        '7435252652800675105': {'sync_query': [8], 'sync_para': [10, 11, 12, 13]},
        '7783713287990799147': {'sync_query': [1], 'sync_para': [1]},
        '-5298888036394841032': {'sync_query': [0, 1], 'sync_para': [0]},
        '8523438358559990568': {'sync_query': [4], 'sync_para': [19]},
        '8940756564723164136': {'sync_query': [1], 'sync_para': [16]},
        '-6701160568172828770': {'sync_query': [3, 4], 'sync_para': [85]},
        '3111993442496334429': {'sync_query': [1], 'sync_para': [17, 18, 19]},
        '-5596204188938390305': {'sync_query': [1, 2, 3, 4], 'sync_para': [12, 13]},
        '-1817136919340598169': {'sync_query': [2, 6, 7], 'sync_para': [80, 81, 82]},
        '-942375155725422961': {'sync_query': [1, 5], 'sync_para': [26, 27]},
        '2286728099234825318': {'sync_query': [6, 7], 'sync_para': [1, 2]},
        '2442455938708003123': {'sync_query': [1], 'sync_para': [45, 55]},
        '4000610939981303347': {'sync_query': [3, 4], 'sync_para': [2, 3]},
        '-8316462548373917649': {'sync_query': [8, 9], 'sync_para': [59]},
        '-4743456997471914973': {'sync_query': [7], 'sync_para': [17, 18]},
        '7202811509886249373': {'sync_query': [3, 4], 'sync_para': [1, 3, 4]},
        '-2731094842300103219': {'sync_query': [1, 7], 'sync_para': [2, 3]},
        '261677806626104572': {'sync_query': [6, 7], 'sync_para': [56, 57, 58]},
        '7286454870579705076': {'sync_query': [1], 'sync_para': [18]},
        '5776195653069481446': {'sync_query': [7], 'sync_para': [0, 1, 2]},
        '-6134437282052730515': {'sync_query': [2, 3], 'sync_para': [32, 33, 34, 35, 36]},
        '300437499633294415': {'sync_query': [1], 'sync_para': [26]},
        '447209470384128282': {'sync_query': [1], 'sync_para': [50, 51]},
        '-3759715711091585135': {'sync_query': [6, 7], 'sync_para': [11, 12]},
        '9221155040830592910': {'sync_query': [5, 6, 7], 'sync_para': [2, 3, 4, 5]},
        '-7224249590163180142': {'sync_query': [1], 'sync_para': [2, 3, 4]},
        '-8150373725253512225': {'sync_query': [6, 7], 'sync_para': [10, 11]},
        '-3301899739983460841': {'sync_query': [6], 'sync_para': [3]},
        '4482920277039245803': {'sync_query': [1], 'sync_para': [112, 113, 114]},
        '-8502415722850021018': {'sync_query': [1], 'sync_para': [0, 1]},
        '7657679678613217058': {'sync_query': [7], 'sync_para': [10, 12, 13]},
        '8702062837938010916': {'sync_query': [6, 7, 8], 'sync_para': [56, 57, 58, 59]},
        '-7642270459387920353': {'sync_query': [2, 3, 4], 'sync_para': [2, 3]},
        '-4478456263205619081': {'sync_query': [4, 5], 'sync_para': [3, 4]},
        '-3296977285905055030': {'sync_query': [1], 'sync_para': [8, 9, 10, 11]},
        '7214324592019569285': {'sync_query': [1, 5], 'sync_para': [22, 23]},
        '-5782926581968900804': {'sync_query': [1], 'sync_para': [118]},
        '-8408180440642663270': {'sync_query': [6, 7], 'sync_para': [2, 3, 4, 5, 6]},
        '-344147762763097273': {'sync_query': [7, 8], 'sync_para': [52, 53, 54]},
        '8074190686488334081': {'sync_query': [2, 3], 'sync_para': [7, 8, 9, 10, 11]},
        '-3880768033572145817': {'sync_query': [3], 'sync_para': [1]},
        '6782139549184082662': {'sync_query': [1, 8], 'sync_para': [5, 6]},
        '8704046441982292961': {'sync_query': [4, 5, 6, 7], 'sync_para': [6, 7, 8, 9, 10, 11, 12, 13]},
        '-7523318980616359210': {'sync_query': [1], 'sync_para': [5, 6, 9]},
        '-2661767287831181663': {'sync_query': [1], 'sync_para': [7, 8]},
        '3526597300242364097': {'sync_query': [2, 3, 4], 'sync_para': [0, 1]},
        '4086289057400176528': {'sync_query': [1, 5], 'sync_para': [14, 15]},
        '2049119502040603392': {'sync_query': [1, 7], 'sync_para': [19, 25]},
        '-3254745754392014990': {'sync_query': [1], 'sync_para': [5, 6, 7]},
        '-3703281941220174621': {'sync_query': [1, 4], 'sync_para': [43, 47]},
        '368926807467533527': {'sync_query': [3, 4, 5, 6, 7], 'sync_para': [194, 195, 196, 197]},
        '-3893116332950023205': {'sync_query': [9, 10], 'sync_para': [26, 27, 28]},
        '2888181863922467062': {'sync_query': [1], 'sync_para': [8, 9, 10, 11]},
        '8350331886779413888': {'sync_query': [9, 10, 11], 'sync_para': [26, 27]},
        '6075163611670541987': {'sync_query': [8, 9], 'sync_para': [20, 26]},
        '-918760088294569785': {'sync_query': [7], 'sync_para': [17, 18]},
        '6530128976966689511': {'sync_query': [4, 5], 'sync_para': [14]},
        '-6998934444953478464': {'sync_query': [7], 'sync_para': [0, 1, 2]},
        '1502598426047034875': {'sync_query': [3], 'sync_para': [4, 5]},
        '563437725243856846': {'sync_query': [1, 8], 'sync_para': [52, 53]},
        '-2954183909629608670': {'sync_query': [5, 6, 7, 8], 'sync_para': [38, 39]},
        '-7701057934018524667': {'sync_query': [7], 'sync_para': [20]},
        '-661708683524023283': {'sync_query': [5], 'sync_para': [23]},
        '4380043672133751613': {'sync_query': [3], 'sync_para': [1]},
        '8351166662038850433': {'sync_query': [10, 11], 'sync_para': [2, 3, 4]},
        '-2438649373752884979': {'sync_query': [1], 'sync_para': [6]},
        '1000826765218219644': {'sync_query': [3, 4], 'sync_para': [65, 66]},
        '-8675408303437804867': {'sync_query': [6, 7], 'sync_para': [31, 32, 33]},
        '-8918348481808900770': {'sync_query': [7, 8], 'sync_para': [52, 53, 54]},
        '5952683277995361374': {'sync_query': [9, 10], 'sync_para': [2, 3]},
        '-9196017876796754634': {'sync_query': [3, 4], 'sync_para': [65, 66]},
        '-3095089351077634994': {'sync_query': [1], 'sync_para': [13, 14]},
        '1400242720942992403': {'sync_query': [4], 'sync_para': [2]},
        '933434885312058363': {'sync_query': [3], 'sync_para': [12]},
        '6658774759333239774': {'sync_query': [1], 'sync_para': [2, 3, 4]},
        '-4475245671781649533': {'sync_query': [7], 'sync_para': [3, 4, 5]},
        '5560002299831524798': {'sync_query': [2, 3], 'sync_para': [0, 1]},
        '-3098976541115711955': {'sync_query': [2], 'sync_para': [18]},
        '2256159845986641982': {'sync_query': [7, 8], 'sync_para': [4, 5]},
        '-4199309333708845046': {'sync_query': [7, 8], 'sync_para': [106, 107, 108]}
        }
sync_part = {'version': 'sync_part', 'data': []}


def convert_data_100(data_file, read_data_file):
    with open(data_file, 'r', encoding='utf-8') as fin:
        data = json.loads(fin.readline())
        example_count = 0
        with open(read_data_file, 'w', encoding='utf-8') as fout:
            for id, attribute in data.items():
                qp_pair = {}
                if id in dict:
                    qp_pair['question'] = ' '.join([token[0] for token in attribute['question_tokens']])
                    fout.write(qp_pair['question'] + '\n')
                    qp_pair['query_sync_tokens'] = dict[id]['sync_query']
                    fout.write(str(qp_pair['query_sync_tokens']) + ' ')
                    for idx in qp_pair['query_sync_tokens']:
                        fout.write(qp_pair['question'].split()[idx] + ' ')
                    fout.write('\n')
                    qp_pair['paragraph'] = attribute['paragraph']
                    fout.write(qp_pair['paragraph'] + '\n')
                    qp_pair['para_sync_tokens'] = dict[id]['sync_para']
                    fout.write(str(qp_pair['para_sync_tokens']) + ' ')
                    for idx in qp_pair['para_sync_tokens']:
                        fout.write(qp_pair['paragraph'].split()[idx] + ' ')
                    fout.write('\n')
                    fout.write(attribute['answer_text'])
                    fout.write('\n')
                    fout.write('\n')
                    example_count += 1
                    sync_part['data'].append(qp_pair)
        # with open(save_file, 'w', encoding='utf-8') as fout:
        #     json.dump(sync_part, fout)
        return sync_part, example_count

def expand_sync(question,para,query_index_num,para_index_num):
    query_list = question.split()
    para_list = para.split()
    query_index = [query_index_num]
    para_index = [para_index_num]
    if query_index_num != 0:
        if query_list[query_index_num - 1].lower() in ['is','as','was','and','get','the','a','of','to','for','at','being','with']:
            query_index = [query_index_num - 1] + query_index
    if query_index_num != len(query_list)-1:
        if query_list[query_index_num - 1].lower() in ['as','by','in','from','of','on','out','into','and','over','to','for','at','being','with']:
            query_index = query_index + [query_index_num + 1]
    if para_index_num != 0:
        if para_list[para_index_num - 1].lower() in ['is','as','was','and','get','the','a','of','to','for','at','being','with']:
            para_index = [para_index_num - 1] + para_index
    if para_index_num != len(para_list)-1:
        if para_list[para_index_num - 1].lower() in ['as','by','in','from','of','on','out','into','and','over','to','for','at','being','with']:
            para_index = para_index + [para_index_num + 1]

    return (query_index if isinstance(query_index,list) else [query_index],
            para_index if isinstance(para_index,list) else [para_index])

def convert_data(data_file, read_data_file, save_file, sync_part, example_count):
    with open(data_file, 'r', encoding='utf-8') as f:
        with open(read_data_file, 'a+', encoding='utf-8') as w:
            data = json.load(f)['data']
            for para in data:
                qp_pair = {}
                qp_pair['question'] = para['question']

                query_index, para_index = para['query_sync_tokens'][0], para['para_sync_tokens']
                query_index_expand, para_index_expand = expand_sync(para['question'],para['paragraph'],query_index[0],para_index[0])
                if len(query_index_expand) == 1 and len(para_index_expand) == 1:
                    continue
                query_list = para['question'].split()
                para_list = para['paragraph'].split()
                qp_pair['query_sync_tokens'] = query_index_expand
                w.write(para['question']+'\n')
                w.write(str([query_list[index] for index in query_index_expand]))
                w.write(str(query_index_expand)+'\n')
                qp_pair['para_sync_tokens'] = para_index_expand
                w.write(str([para_list[index] for index in para_index_expand]))
                w.write(str(para_index_expand) + '\n')
                qp_pair['paragraph'] = para['paragraph']
                w.write(para['paragraph'] + '\n')
                w.write('\n')
                sync_part['data'].append(qp_pair)
                example_count += 1
            with open(save_file, 'w', encoding='utf-8') as fout:
                json.dump(sync_part, fout)
            return example_count

    # with open(data_file, 'r', encoding='utf-8') as fin:
    #     data = json.loads(fin.readline())
    #     with open(read_data_file, 'a+', encoding='utf-8') as fout:
    #         for id, attribute in data.items():
    #             qp_pair = {}
    #             if id in dict:
    #                 qp_pair['question'] = ' '.join([token[0] for token in attribute['question_tokens']])
    #                 fout.write(qp_pair['question'] + '\n')
    #                 qp_pair['query_sync_tokens'] = dict[id]['sync_query']
    #                 fout.write(str(qp_pair['query_sync_tokens']) + ' ')
    #                 for idx in qp_pair['query_sync_tokens']:
    #                     fout.write(qp_pair['question'].split()[idx] + ' ')
    #                 fout.write('\n')
    #                 qp_pair['paragraph'] = attribute['paragraph']
    #                 fout.write(qp_pair['paragraph'] + '\n')
    #                 qp_pair['para_sync_tokens'] = dict[id]['sync_para']
    #                 fout.write(str(qp_pair['para_sync_tokens']) + ' ')
    #                 for idx in qp_pair['para_sync_tokens']:
    #                     fout.write(qp_pair['paragraph'].split()[idx] + ' ')
    #                 fout.write('\n')
    #                 fout.write(attribute['answer_text'])
    #                 fout.write('\n')
    #                 fout.write('\n')
    #                 example_count += 1
    #                 sync_part['data'].append(qp_pair)
    #     with open(save_file, 'w', encoding='utf-8') as fout:
    #         json.dump(sync_part, fout)
    #     return sync_part,example_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, default='')
    parser.add_argument('--read_data_file', required=True, default='')
    parser.add_argument('--save_file', required=True, default='')
    parser.add_argument('--sync_file', required=True, default='')
    args = parser.parse_args()
    sync_part, example_count = convert_data_100(args.data_file, args.read_data_file)
    example_count = convert_data(args.sync_file, args.read_data_file, args.save_file, sync_part, example_count)
    print('convert %d sync_part complete' % example_count)
