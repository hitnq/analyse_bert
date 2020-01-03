import json
import argparse

ask_type_squad = {'version': 'ask_type_short_answer', 'data': []}


def convert_data(data_file, read_data_file, save_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        with open(read_data_file, 'w', encoding='utf-8') as w:
            data = json.load(f)['data']
            example_count = 0
            for para in data:
                new_para = []
                for p in para['paragraphs']:
                    new_p = []
                    for qa in p['qas']:
                        new_qa = []
                        for answer in qa['answers']:
                            new_answers = []
                            w.write(qa['question'] + '\n')
                            answer_text = answer['text']
                            answer_start = answer['answer_start']
                            answer_loc = p['char_to_word_offset_para'][answer_start]
                            context_list = p['context'].split()

                            if answer_loc-5 < 0:
                                new_context = context_list[0:answer_loc]
                            else:
                                new_context = [context_list[answer_loc-i] for i in range(5,0,-1)]

                            new_context = new_context + answer_text.split()

                            if answer_loc + len(answer_text.split()) != len(context_list):
                                if answer_loc + len(answer_text.split()) + 5 > len(context_list):
                                    new_context = new_context + context_list[answer_loc + len(answer_text.split()):]
                                else:
                                    new_context = new_context + [context_list[answer_loc + len(answer_text.split()) + i] for i in range(1,5)]

                            new_context = ' '.join(new_context)
                            try:
                                answer['answer_start'] = new_context.index(answer_text)
                            except:
                                print(1)
                            p['context'] = new_context
                            new_answers.append(answer)
                            qa['answers'] = new_answers
                        new_qa.append(qa)
                        p['qas'] = new_qa
                        new_p.append(p)
                    para['paragraphs'] = new_p
                example_count += 1
                ask_type_squad['data'].append(para)
            with open(save_file, 'w', encoding='utf-8') as fout:
                json.dump(ask_type_squad, fout)
            return example_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, default='')
    parser.add_argument('--read_data_file', required=True, default='')
    parser.add_argument('--save_file', required=True, default='')
    args = parser.parse_args()
    example_count = convert_data(args.data_file, args.read_data_file, args.save_file)
    print('convert %d long to short complete' % example_count)
