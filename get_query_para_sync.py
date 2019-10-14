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

def find_answer_paragraph(only_short_data):
    #找到answer所在的para 并得到最后的结果
    all_sync_pair = []
    record_ids = []
    for paragraphs in tqdm.tqdm(only_short_data['data']):
        context = paragraphs['paragraphs'][0]['context']
        question = paragraphs['paragraphs'][0]['qas'][0]['question']
        answers = paragraphs['paragraphs'][0]['qas'][0]['answers']
        qas_id = paragraphs['paragraphs'][0]['qas'][0]['id']
        #print(context[answers[0]['nq_span_start']:answers[0]['nq_span_end']])
        #print(answers[0]['nq_span_text'])
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
            paragraph = context[para_start+delete_list[-1]:para_end]
            query_para_pair = find_question_para_sync_pair(question,paragraph)
            if len(query_para_pair) != 0:
                with open('./sync.txt', 'w') as w:
                    w.write(str(query_para_pair))
                    w.write('\n')
                    w.write('\n')
                    w.write(question)
                    w.write('\n')
                    w.write('\n')
                    w.write(paragraph)
                    w.write('\n')
                    w.write('\n')
                    w.write(answer['text'])
                    w.write('\n')
                    w.write('\n')
                all_sync_pair.append(query_para_pair)
                record_ids.append(qas_id)
    print(all_sync_pair)
    record_ids = list(set(record_ids))
    print(record_ids)
    return record_ids,all_sync_pair

def find_sen_sync(sen_lemma):
    #找到一句话中的所有词的同义词
    all_sen_sync = []
    for word in sen_lemma:
        word_set = wn.synsets(word)
        if len(word_set) != 0:
            word_set_filter = {}
            if word not in word_set_filter:
                word_set_filter[word] = []
            for item in word_set:
                for w in item.lemma_names():
                    if w != word:
                        word_set_filter[word].append(w)
            all_sen_sync.append(word_set_filter)
    return all_sen_sync

def find_question_para_sync_pair(question,paragraph):#try1
    #先找question中所有词的同义词，遍历para中的所有词 看是否能在question的同义词集合中找到。
    question_lemma_has_stop = sentence_lemma(question)
    para_lemma_has_stop = sentence_lemma(paragraph)
    question_lemma = []
    para_lemma = []
    for w in question_lemma_has_stop:
        if w not in STOP_WORDS:
            question_lemma.append(w)
    for w in para_lemma_has_stop:
        if w not in STOP_WORDS:
            para_lemma.append(w)
    sync_pair = {}
    all_question_sync = find_sen_sync(question_lemma)
    all_para_sync = find_sen_sync(para_lemma)
    for q in all_question_sync[0].keys():
        for p in all_para_sync[0].keys():
            compare_set = set(all_question_sync[0][q]) & set(all_para_sync[0][p])
            if len(compare_set) != 0 and p != q:
                sync_pair[q] = p
    return sync_pair

def sentence_lemma(sentence):#将一句话中的所有词转为lemma
    tokens = word_tokenize(sentence.lower())  # 分词
    tagged_sent = pos_tag(tokens) #获取词性
    wnl = WordNetLemmatizer()#词形还原器
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wn.NOUN
        lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos))  # 词形还原
    return lemmas_sent


def get_wordnet_pos(tag):#获取单词的词性
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
    parser.add_argument('--input_file',default='/mnt/caijie/nq/all_squadformat_dev.json')
    parser.add_argument('--output_file',default='/mnt/caijie/nq/only_short_dev.json')
    args = parser.parse_args()
    if os.path.exists(args.output_file):
        only_short_data = json.loads(open(args.output_file, 'r').readline())
    else:
        only_short_data = get_only_short_answer_nq(args.input_file, args.output_file)
    find_answer_paragraph(only_short_data)

