import json
import argparse
import random
random_list_train = random.sample(range(1,70000),10000)
random_list_test = random.sample(range(70000,100000),5000)
boundary = {'version': 'boundary', 'data': []}

def convert_single_example(data):
    new_data = {'paragraphs':[]}
    new_para = {}
    context = data['paragraphs'][0]['context']
    ans_start = data['paragraphs'][0]['qas'][0]['answers'][0]['answer_start']
    answer_text = data['paragraphs'][0]['qas'][0]['answers'][0]['text']
    ans_end = ans_start + len(answer_text)
    while ans_start > 0 :
        ans_start -= 1
        if context[ans_start] in ['?',';','.','!',']']:
            break
    while ans_end < len(context)-1:
        ans_end += 1
        if context[ans_end] in ['?',';','.','!','[']:
            break
    new_context = context[ans_start:ans_end+1]
    new_para['context'] = new_context
    assert answer_text in new_context
    data['paragraphs'][0]['qas'][0]['answers'][0]['answer_start'] = new_context.index(answer_text)
    new_para['qas'] = data['paragraphs'][0]['qas']
    new_data['paragraphs'].append(new_para)
    return new_data

def convert_data_all_squad(data_file,read_data_file,save_file):
    with open(data_file,'r',encoding='utf-8') as fin:
        with open(read_data_file, 'w', encoding='utf-8') as w:
            example_count = 0
            data = json.load(fin)['data']
            print(len(data))
            for i in random_list_test:
                new_data = convert_single_example(data[i])
                boundary['data'].append(new_data)
                example_count += 1
        with open(save_file, 'w', encoding='utf-8') as fout:
            json.dump(boundary, fout)
    return example_count

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, default='')
    parser.add_argument('--read_data_file', required=True, default='')
    parser.add_argument('--save_file', required=True, default='')
    args = parser.parse_args()
    example_count = convert_data_all_squad(args.data_file, args.read_data_file, args.save_file)
    print('convert %d boundary complete' % example_count)