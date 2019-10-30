import json
import argparse
import re
import os
import io
import sys
import nltk
import tqdm
import numpy as np
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer

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
        for example in data:
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

def get_w_in_q_count(word,question):
    count = 0
    for q in question:
        if q == word:
            count += 1
    return count

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

def get_tf_idf(all_questions_sents):
    tfidf = {}
    doc_has_w_map = {}
    for question in all_questions_sents:
        for w in question:
            if w in doc_has_w_map:
                doc_has_w_map[w] += 1
            else:
                doc_has_w_map[w] = 1
    for q in all_questions_sents:
        for w in q:
            tf = get_w_in_q_count(w, q) / len(q)
            if w not in tfidf:
                idf = np.log(len(all_questions_sents) / (doc_has_w_map[w] + 1))
                tfidf[w] = tf * idf
    with open(args.tfidf_file,'w') as fout:
        json.dump(tfidf,fout)
    return tfidf

def find_answer_paragraph(only_short_data):
    #找到answer所在的para 并得到最后的结果
    all_questions_words = []
    all_questions_sents = []
    all_questions_sents_len = []
    tfidf = {}
    query_para_pair = {}
    final_shortcut_data = {'version': 'short_cut', 'data': []}
    for paragraphs in tqdm.tqdm(only_short_data['data']):
        context = paragraphs['paragraphs'][0]['context']
        question = paragraphs['paragraphs'][0]['qas'][0]['question']
        answers = paragraphs['paragraphs'][0]['qas'][0]['answers']
        qas_id = paragraphs['paragraphs'][0]['qas'][0]['id']
        data = {'title': paragraphs['title'], 'paragraphs': []}
        answer_paras = {'answers':[],'para':[],'answer_start':[]} 
        doc_tokens_query, char_to_word_offset_query = get_char_of_token(question)
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
            delete_list = [index.end() for index in re.finditer('=-*[0-9]+\]+',
                                                                context[para_start:para_end])]
            paragraph = context[para_start+delete_list[-1]+1:para_end]
            doc_tokens_para, char_to_word_offset_para = get_char_of_token(paragraph)
            answer_paras['question_tokens'] = doc_tokens_query
            answer_paras['question_offset'] = char_to_word_offset_query
            answer_paras['paragraph_tokens'].append(doc_tokens_para)
            answer_paras['paragraph_offset'] = char_to_word_offset_query
            answer_paras['answers'].append(answer['text'])
            answer_paras['answers_start'].append(paragraph.index(answer['text']) if paragraph.index(answer['text']) else -1)
        
        all_questions_sents.append(doc_tokens_query)
        all_questions_sents_len.append(len(doc_tokens_query))
        all_questions_words.extend(doc_tokens_query)
        query_para_pair[question] = answer_paras
    if os.path.exists(args.tfidf_file):
        tfidf = json.load(open(args.tfidf_file,'r'))
    else:
        tfidf = get_tf_idf(all_questions_sents)
    # with open('./sync_sync.json', 'w') as w:
        # json.dump(final_shortcut_data,w)
    return tfidf,query_para_pair


def get_question_key(attributes,tfidf):
    new_query_item = []
    sent_spans = []
    answer_in_span = []
    for q in attributes['question']:
        if tfidf[q] > 0.5:
            new_query_item.append(q)
    for para in attributes['para']:
        sent_end = [m.start() for m in re.finditer('\\s+[?|.|;|!]+\\s+',para)]
        sent_end = list(map(lambda x:x+2,sent_end))
        if len(sent_end) == 0:
            sent_end = [len(para)]
        sent_start = [0] + sent_end
        sent_spans.append(list(zip(sent_start,sent_end)))
    for i in range(len(sent_spans)):
        for sent in sent_spans[i]:
            if attributes['answer_start'][i] >= sent[0] and \
                attributes['answer_start'][i] + len(attributes['answers'][i]) <= sent[1]:
                answer_in_span.append(sent)

    for i in range(len(answer_in_span)):
        print(new_query_item)
        print(value['para'][i][answer_in_span[i][0]:answer_in_span[i][1]])
        in_para = False
        for new in new_query_item:
            if new in value['para'][i][answer_in_span[i][0]:answer_in_span[i][1]]:
                in_para = True
                break
            else:
                continue
        if in_para:
            print(new_query_item)
            print(value['para'][i][answer_in_span[i][0]:answer_in_span[i][1]])

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file',default='/data/home/t-jicai/caijie/analyse_bert/all_squadformat_nq_train_withnqidx.json')
    parser.add_argument('--output_file',default='/data/home/t-jicai/caijie/analyse_bert/only_short_train.json')
    parser.add_argument('--tfidf_file',default='/data/home/t-jicai/caijie/analyse_bert/tfidf.json')
    args = parser.parse_args()
    if os.path.exists(args.output_file):
        only_short_data = json.loads(open(args.output_file, 'r').readline())
    else:
        only_short_data = get_only_short_answer_nq(args.input_file, args.output_file)
    tfidf,query_para_pair = find_answer_paragraph(only_short_data)
    for questiuon,attributes in query_para_pair.items():
        get_question_key(attributes,tfidf)




