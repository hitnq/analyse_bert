import json
import argparse
import re
import os
import io
import sys
import nltk
import tqdm
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
# from knockknock import teams_sender
# CHAT_ID: int = 1
# @teams_sender(token="https://outlook.office.com/webhook/656807a2-c249-4e72-955e-2e967c0716f1@72f988bf-86f1-41af-91ab-2d7cd011db47/IncomingWebhook/1057b874a850467ea4c1276c1eab752b/6ae68729-e69b-44d1-9bce-1803a813b0e3")

STOP_WORDS = {"", "", "all", "being", "-","be","do","over", "through", "yourselves", "its", "before",
              "hadn", "with", "had", ",", "should", "to", "only", "under", "ours", "has", "ought", "do",
              "them", "his", "than", "very", "cannot", "they", "not", "during", "yourself", "him",
              "nor", "did", "didn", "'ve", "this", "she", "each", "where", "because", "doing", "some", "we", "are",
              "further", "ourselves", "out", "what", "for", "weren", "does", "above", "between", "mustn", "?",
              "be", "hasn", "who", "were", "here", "shouldn", "let", "hers", "by", "both", "about", "couldn",
              "of", "could", "against", "isn", "or", "own", "into", "while", "whom", "down", "wasn", "your",
              "from", "her", "their", "aren", "there", "been", ".", "few", "too", "wouldn", "themselves",
              ":", "was", "until", "more", "himself", "on", "but", "don", "herself", "haven", "those", "he",
              "me", "myself", "these", "up", ";", "below", "'re", "can", "theirs", "my", "and", "would", "then",
              "is", "am", "it", "doesn", "an", "as", "itself", "at", "have", "in", "any", "if", "!",
              "again", "'ll", "no", "that", "when", "same", "how", "other", "which", "you", "many", "shan",
              "'t", "'s", "our", "after", "most", "'d", "such", "'m", "why", "a", "off", "i", "yours", "so",
              "the", "having", "once"}

def get_only_short_answer_nq(input_path, output_path):
    with open(input_path, 'r') as f:
        all_data = json.loads(f.readline())
        data = all_data['data']
        only_short_data = []
        print('origin dev nq _examples len : ', len(data))
        for example in tqdm.tqdm(data):
            if example['paragraphs'][0]['qas'][0]['is_impossible']:
                continue
            elif example['paragraphs'][0]['qas'][0]['answers'][0]['nq_input_text'] != 'short':
                continue
            else:
                only_short_data.append(example)
        print('only short dev nq _examples len : ',len(only_short_data))  # 3263
        new_all_dev_data = {'version': 'only_short_nq', 'data': only_short_data}
        with open(output_path, 'w') as w:
            json.dump(new_all_dev_data, w)
        return new_all_dev_data

def find_answer_paragraph(only_short_data):
    #find para which answer in and get the pair
    all_sync_pair = []
    record_ids = []
    final_shortcut_data = {'version':'short_cut','data':[]}
    for paragraphs in tqdm.tqdm(only_short_data['data']):
        context = paragraphs['paragraphs'][0]['context']
        question = paragraphs['paragraphs'][0]['qas'][0]['question']
        answers = paragraphs['paragraphs'][0]['qas'][0]['answers']
        qas_id = paragraphs['paragraphs'][0]['qas'][0]['id']
        #print(context[answers[0]['nq_span_start']:answers[0]['nq_span_end']])
        #print(answers[0]['nq_span_text'])
        data = {'title':paragraphs['title'],'paragraphs':[]}
        for answer in answers:
            paragraph_id = answer['nq_candidate_id']
            label = '[ContextId='+str(paragraph_id)+']'
            para_start = context.index(label)
            para_end = 0
            for i in range(para_start+1,len(context)):
                if context[i:i+11]=='[ContextId=':
                    para_end = i
                    break
                if i == len(context)-1:
                    para_end = len(context)
            delete_list = [index.end() for index in re.finditer('=-*[0-9]+\]+',context[para_start:para_end])]
            paragraph = context[para_start+delete_list[-1]+1:para_end]
            query_para_pair,char2token_q,char2token_p = find_question_para_shortcut_pair(question,paragraph)
            if len(query_para_pair)==0:
                continue
            if len(query_para_pair) != 0:
                data['paragraphs'].append({'context': paragraph,
                                           'charoftoken_q': char2token_q,
                                           'charoftoken_p': char2token_p,
                                           'qas': [{'question': question,
                                                    'id': qas_id}]})
                all_sync_pair.append(query_para_pair)
                record_ids.append(qas_id)
        final_shortcut_data['data'].append(data)
    with open('./sync_shortcut.json', 'w') as w:
        json.dump(final_shortcut_data,w)
    print(all_sync_pair)
    record_ids = list(set(record_ids))
    print(record_ids)
    print('examples:',len(record_ids))
    return record_ids,all_sync_pair

def find_question_para_shortcut_pair(question,paragraph):
    char2token_q = []
    char2token_p = []
    query = question.split()
    para = paragraph.split()
    for q in query:
        try:
            word_map = {'word': q,'pos': [m.start() for m in re.finditer(q,question)]}
        except:
            word_map = {'word': q, 'pos': []}
        char2token_q.append(word_map)
    for p in para:
        try:
            word_map = {'word': p, 'pos': [m.start() for m in re.finditer(p, paragraph)]}
        except:
            word_map = {'word': p, 'pos': []}
        char2token_p.append(word_map)
    assert len(query)==len(char2token_q)
    assert len(para)==len(char2token_p)

    sync_pair = {}
    for q in range(len(query)):
        if len(query[q]) < 2 or query[q] in STOP_WORDS:
            continue
        for i in range(len(para)-len(query[q])):
            perfix = ''
            for w in para[i:i+len(query[q])]:
                if w[0].isupper():
                    perfix += w[0]
                else:
                    break
            if len(perfix) != len(query[q]):
                continue
            if perfix.lower() == query[q]:
                sync_pair[' '.join(para[i:i+len(query[q])])] = query[q]
    return sync_pair,char2token_q,char2token_p

def sentence_lemma(sentence):
    tokens = word_tokenize(sentence.lower())
    tagged_sent = pos_tag(tokens)
    wnl = WordNetLemmatizer()
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wn.NOUN
        lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos))  # 词形还原
    return lemmas_sent


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('V'):
        return wn.VERB
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    else:
        return None


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file',default='/data/home/t-jicai/caijie/analyse_bert/all_squadformat_nq_dev_withnqidx.json')
    parser.add_argument('--output_file',default='/data/home/t-jicai/caijie/analyse_bert/only_short_dev.json')
    args = parser.parse_args()
    if os.path.exists(args.output_file):
        only_short_data = json.loads(open(args.output_file, 'r').readline())
    else:
        only_short_data = get_only_short_answer_nq(args.input_file, args.output_file)
    find_answer_paragraph(only_short_data)
    print('convert sync has completed!')

