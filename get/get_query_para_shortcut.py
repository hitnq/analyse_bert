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
            query_para_pair, doc_tokens_query, doc_tokens_para, \
            char_to_word_offset_query, char_to_word_offset_para = \
                find_question_para_shortcut_pair(question,paragraph)
            if len(query_para_pair) != 0:
                data['paragraphs'].append({'context': paragraph,
                                           'doc_tokens_query': doc_tokens_query,
                                           'doc_tokens_para': doc_tokens_para,
                                           'char_to_word_offset_query': char_to_word_offset_query,
                                           'char_to_word_offset_para': char_to_word_offset_para,
                                           'qas': [{'question': question,
                                                    'sync_pair': query_para_pair,
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

def is_whitespace(c):
    if c == " " or c == "\t" or c == "\r" or c == "\n" or ord(c) == 0x202F:
        return True
    return False

def get_char_of_token(sentence):
    doc_tokens_original = []
    char_to_word_offset_origin = []
    pre_is_white_space = True
    for c in sentence:
        if is_whitespace(c):
            pre_is_white_space = True
        else:
            if pre_is_white_space:
                doc_tokens_original.append(c)
            else:
                doc_tokens_original[-1] += c
            pre_is_white_space = False
        char_to_word_offset_origin.append(len(doc_tokens_original) - 1)
    return doc_tokens_original,char_to_word_offset_origin

def find_question_para_shortcut_pair(question,paragraph):
    doc_tokens_query, char_to_word_offset_query = get_char_of_token(question)
    doc_tokens_para, char_to_word_offset_para = get_char_of_token(paragraph)

    sync_pair = {}
    for q in range(len(doc_tokens_query)):
        if len(doc_tokens_query[q]) < 2 or doc_tokens_query[q] in STOP_WORDS:
            continue
        for i in range(len(doc_tokens_para)-len(doc_tokens_query[q])):
            perfix = ''
            for w in doc_tokens_para[i:i+len(doc_tokens_query[q])]:
                if w[0].isupper():
                    perfix += w[0]
                else:
                    break
            if len(perfix) != len(doc_tokens_query[q]):
                continue
            if perfix.lower() == doc_tokens_query[q]:
                sync_pair[q] = i
    #print(sync_pair)
    return sync_pair,doc_tokens_query,doc_tokens_para,\
           char_to_word_offset_query,char_to_word_offset_para

def sentence_lemma(doc_tokens):
    tagged_sent = pos_tag(doc_tokens)
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

