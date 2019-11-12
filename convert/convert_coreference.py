import json
import argparse

dict = {'7841177184804949328':{'co_query':[0,1],'co_para':[45,46]},
'4266941701310881018':{'co_query':[0,1,2],'co_para':[29,30]},
'-7522925448152928839':{'co_query':[0],'co_para':[39]},
'5771380493354495364':{'co_query':[0,1,2,3,4,5],'co_para':[44,45]},
'427969558370580025':{'co_query':[0,1],'co_para':[20,21]},
'-3071962219115388524':{'co_query':[13,14],'co_para':[16]},
'3811390334825259145':{'co_query':[0,1,2,3,4,5,6,7,8],'co_para':[29,30]},
'-941068812149476325':{'co_query':[0,1],'co_para':[79]},
'1309551455514971810':{'co_query':[0,1,2,3,4,5],'co_para':[17,18]},
'89315461351975887':{'co_query':[2,3,4],'co_para':[34]},
'-1168989793403787752':{'co_query':[0,1],'co_para':[25]},
'-3597961506867638003':{'co_query':[3],'co_para':[33]},
'3445487594449130678':{'co_query':[65],'co_para':[82]},
'-3868678027793136551':{'co_query':[0,1,2,3,4,5],'co_para':[28]},
'-306047269148399621':{'co_query':[54,55,56,57],'co_para':[65]},
'-79809383000514084':{'co_query':[0,1],'co_para':[35]},
'-3068125462410496906':{'co_query':[0,1,2,3,4,5,6],'co_para':[33]},
'7154779298133928735':{'co_query':[36,37,38],'co_para':[59]},
'-7508077802210462684':{'co_query':[0,1,2],'co_para':[45,46]},
'-7468861661154309979':{'co_query':[11,12,13,14,15,16,17,18],'co_para':[23,24]},
'6709349913690237888':{'co_query':[0,1,2],'co_para':[24]},
'-285233251464285365':{'co_query':[0,1,2,3,4],'co_para':[25]},
'-181305449522045818':{'co_query':[10],'co_para':[21]},
'-3904324028477250548':{'co_query':[0,1,2],'co_para':[30]},
'2971657507733412088':{'co_query':[0,1,2,3,4,5,6,7,8,9],'co_para':[18,19]},
'-4776868923521482167':{'co_query':[0,1,2,3,4,5],'co_para':[17,18]},
'7783713287990799147':{'co_query':[0,1,2,3,4,5,6,7,8],'co_para':[44]},
'7751300523129589463':{'co_query':[0,1,2,3,4,5,6,7],'co_para':[61]},
'-9023951041279840976':{'co_query':[0,1],'co_para':[27,28]},
'6684044978302300497':{'co_query':[0,1,2,3,4,5],'co_para':[24]},
'3341051156900570525':{'co_query':[37,38,39,40],'co_para':[97]},
'-4178862577676891442':{'co_query':[0,1,2,3],'co_para':[46,47]},
'3909896943359765295':{'co_query':[0,1,2,3],'co_para':[32]},
'-5000250825746082607':{'co_query':[77,78],'co_para':[94]},
'2049014792539246395':{'co_query':[0,1,2],'co_para':[19]},
'6531847346000866197':{'co_query':[0,1,2,3,4,5,6,7],'co_para':[49,50]},
'-490131683656374211':{'co_query':[1],'co_para':[26]},
'8940756564723164136':{'co_query':[0,1,2,3,4,5,6],'co_para':[44]},
'-4728101993403799694':{'co_query':[0,1,2,3,4,5],'co_para':[33]},
'-6701160568172828770':{'co_query':[5,6,7,8,9],'co_para':[23]},
'-6086450228764331863':{'co_query':[0,1],'co_para':[49]},
'-8604737317969739469':{'co_query':[0,1,2,3,4],'co_para':[55,56]},
'-376344626609936461':{'co_query':[0,1],'co_para':[30,31]},
'6111475549562700823':{'co_query':[0,1],'co_para':[15]},
'2017793259581190117':{'co_query':[0,1],'co_para':[17]},
'-3893431858803011772':{'co_query':[0,1],'co_para':[56,57]},
'8287797887235142909':{'co_query':[0,1,2,3,4],'co_para':[28]},
'-4848215333786211328':{'co_query':[17,18],'co_para':[35]},
'-6134437282052730515':{'co_query':[0,1,2,3],'co_para':[38,39]},
'-7962664819223382064':{'co_query':[29,30],'co_para':[43]},
'8821570159833945526':{'co_query':[0,1,2,3,4],'co_para':[42]},
'-2058459850967436483':{'co_query':[0,1,2,3],'co_para':[20]},
'-2735691032373652197':{'co_query':[0,1,2,3,4,5],'co_para':[26]},
'6304034126847635298':{'co_query':[0,1],'co_para':[31,32]},
'-2898412749395034924':{'co_query':[0],'co_para':[46]},
'447209470384128282':{'co_query':[0,1,2,3,4],'co_para':[27,28]},
'-3759715711091585135':{'co_query':[0,1,2,3,4,5],'co_para':[21,22]},
'3650292110615736829':{'co_query':[0],'co_para':[32]},
'41407191180683688':{'co_query':[15,16],'co_para':[20]},
'4048014354646657819':{'co_query':[0,1,2,3,4,5],'co_para':[33]},
'-118804411554907172':{'co_query':[0,1],'co_para':[13]},
'-4066978824402068743':{'co_query':[0,1,2,3,4],'co_para':[22]},
'815672871865571502':{'co_query':[0,1,2,3,4],'co_para':[18]},
'5857860711767702982':{'co_query':[0,1,2,3,4,5],'co_para':[17,18]},
'-6004878364472743449':{'co_query':[0,1,2,3,4,5,6],'co_para':[22]},
'6530128976966689511':{'co_query':[0],'co_para':[13]},
'947088081367762245':{'co_query':[0,1,2,3,4],'co_para':[35]},
'-4991176369641378104':{'co_query':[0,1,2],'co_para':[27,28]},
'7530807168111168542':{'co_query':[0,1,2],'co_para':[35]},
'1669639797654860786':{'co_query':[47,48],'co_para':[50,51,52]},
'8350331886779413888':{'co_query':[36],'co_para':[56]},
'7503085205116129029':{'co_query':[0,1,2,3,4,5],'co_para':[42]},
'-5505990784235403264':{'co_query':[2,3,4,5,6,7,8,9],'co_para':[32]},
'-529900975257997672':{'co_query':[0,1,2],'co_para':[27,28]},
'3383302525359750725':{'co_query':[0,1,2,3,4,5],'co_para':[29]},
'-350529248882692508':{'co_query':[0,1],'co_para':[32]},
'-6875263727865407303':{'co_query':[0,1,2],'co_para':[32]},
'6938283870609206044':{'co_query':[0,1,2,3,4,5,6,7,8],'co_para':[33]},
'7350997195569879091': {'co_query':[73],'co_para':[98]},
'-9020446073785944330': {'co_query':[0,1,2],'co_para':[31,32]},
'958320236604379665': {'co_query':[0,1,2,3,4],'co_para':[57]},
'-4205403809844477875': {'co_query':[0,1,2,3,4,5],'co_para':[21,22]},
'-289843514650659093': {'co_query':[0,1],'co_para':[64,65]},
'6248810984813680065': {'co_query':[10,11],'co_para':[13]},
'-827840489801273691': {'co_query':[0,1],'co_para':[33]},
'-4416176860045600265': {'co_query':[0,1,2,3,4,5],'co_para':[102,103]},
'-1635773155576213616': {'co_query':[0,1,2],'co_para':[50,51]},
'-7272866875295834187': {'co_query':[36,37,38,39,40],'co_para':[57,58]},
'8525681493084227596': {'co_query':[0,1,2,3],'co_para':[70,71,72]},
'3088782531883715261': {'co_query':[12],'co_para':[37]},
'-6089121611409468491': {'co_query':[0,1,2,3,4,5,6,7],'co_para':[35]},
'-6726269601434213805': {'co_query':[0,1,2,3,4,5],'co_para':[21,22]},
'376100590570938035': {'co_query':[0],'co_para':[9]},
'-7160885863484526170': {'co_query':[0],'co_para':[43]},
'6304699121124606170': {'co_query':[0,1,2,3,4,5],'co_para':[16]},
'4019902438849394584': {'co_query':[0,1,2],'co_para':[21]},
'-1120260812123069285': {'co_query':[0,1],'co_para':[26]},
'-5550489214924297810': {'co_query':[0,1,2,3,4,5,6],'co_para':[38]},
'-1425912698719166884': {'co_query':[0,1,2,3,4,5],'co_para':[29]},
'-8474377600796597037': {'co_query':[36,37,38],'co_para':[58]},
'8589251048032909819':{'co_query':[0,1,2,3],'co_para':[48,49]}
}
# '/data/home/t-jicai/caijie/analyse_bert/data/nq/qas_is_sync.json'
def convert_data(data_file,read_data_file,save_file):
    with open(data_file, 'r',encoding='utf-8') as fin:
        data = json.loads(fin.readline())
        example_count = 0
        sync_part = {'version':'sync_part','data':[]}
        with open(read_data_file,'w',encoding='utf-8') as fout:
            for id, attribute in data.items():
                qp_pair = {}
                if id in dict:
                    qp_pair['question'] = ' '.join([token[0] for token in attribute['question_tokens']])
                    fout.write(qp_pair['question']+'\n')
                    qp_pair['query_sync_tokens'] = dict[id]['co_query']
                    qp_pair['query_sync_tokens'] = [i+len(attribute['question_tokens']) for i in qp_pair['query_sync_tokens']]
                    fout.write(str(qp_pair['query_sync_tokens']) + ' ')
                    fout.write(str([attribute['paragraph'].split()[i-len(qp_pair['question'].split())] for i in qp_pair['query_sync_tokens']]))
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
                    example_count += 1
        with open(save_file, 'w', encoding='utf-8') as fout:
            json.dump(sync_part,fout)
        return example_count


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, default='')
    parser.add_argument('--read_data_file', required=True, default='')
    parser.add_argument('--save_file', required=True, default='')
    args = parser.parse_args()
    example_count = convert_data(args.data_file, args.read_data_file, args.save_file)
    print('convert %d coreference complete' % example_count)





