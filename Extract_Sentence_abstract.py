# -*- coding: utf-8 -*-
# Import the required libraries

import nltk, re, csv, os
from nltk.corpus import stopwords
from collections import Counter
import json
import numpy as np
from difflib import SequenceMatcher

def check_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

# Define core and non-core words

core_words = ["highlight", "constitute", "suggest", "indicate", "demonstrate", "show", "reveal", "provide", "illustrate", "describe", "conclude", "support", "establish", "propose", "advocate", "determine", "confirm", "argue", "imply", "display", "offer", "highlights", "constitutes", "suggests", "indicates", "demonstrates", "shows", "reveals", "provides", "illustrates", "describes", "concludes", "supports", "establishes", "proposes", "advocates", "determines", "confirms", "argues", "implies", "displays", "offers", "underlines", "underline", "underlined", "overall", "sum", "therefore", "thus", "together", "conclusion", "collectively", "altogether", "conclude", "conclusively", "consequently", "study", "results", "findings", "research", "report", "data", "paper", "observations", "experiment", "publication", "analysis"]

non_core_words = ["sought", "addition", "well-replicated", "replicated", "sample", "aimed", "aims", "questionnaire", "survey", "based", "interviews", "cross-sectional", "participants", "descriptive", "CI ", "%", "interview", "participant", "cc by 3.0", "previously"] 

# Function that seperates all the lines and creates a list of the most frequent words in the provided text

def determine_lines_and_frequent_words(abstract, path):
    lines = sent_detector.tokenize(abstract)
    text = open(path)
    body = "==== Body"
    refs = "==== Refs"
    started = False
    body_text = ''
    for line in text:
        if refs in line:
            started = False
        if body in line:
            started = True
        if started:
            body_text += line
    body_text = body_text.decode('utf-8')
    
    base_words = nltk.tokenize.casual.casual_tokenize(body_text.lower())
    words = [word for word in base_words if word not in stopwords.words()]
    counts = Counter(words)

    frequent_words = []
    for word, count in counts.most_common(10):
        frequent_words.append(word)
    return lines, frequent_words

# This function assigns every sentence with a score based on some parameters

def assign_sentences_score(lines, frequent_words):
    sentences = {}
    for line in lines:
        score = 0
        words = nltk.tokenize.casual.casual_tokenize(line)
        words = [word for word in words if word != '[' or ']']
        searchObj = re.search( r'(overall|in sum|therefore|thus|together|in conclusion|concluding|taken together|collectively|altogether|taken collectively|to conclude|conclusively|all together|all things considered|everything considered|as a result|consequently|conclusion|thus|as expressed)*.*(the|these|this|the present|our)*(study|results|findings|research|report|data|observation|experiment|publication|analysis|data set|we)+.*(highlight|constitute|suggest|indicate|demonstrate|show|reveal|provide|illustrate|describe|conclude|support|establish|propose|advocate|determine|confirm|argue|impl|display|offer|underline|allow|found|find)+', line, re.I)
        if searchObj != None:
            score += 25
        for word in words:
            if word.lower() in core_words and line.count(word) == 1:
                score += 10
            if word.lower() in frequent_words and line.count(word) == 1:
                score += 5
            if word.lower() in non_core_words:
                score -= 5
        if len(line) >= 400:
            score -= 50
        sentences[line] = score
    return sentences

# In some cases, two sentences end up with the same score, in such a case an extra check is performed to make sure only one sentence is chosen in the end

def perform_extra_check(candidate_sentences, frequent_words):
    less_frequent_words = frequent_words[:5]
    sentences = {}
    for sentence in candidate_sentences:
        score = 0
        words = nltk.tokenize.casual.casual_tokenize(sentence)
        for word in words:
            if word in less_frequent_words:
                score += 1
        sentences[sentence] = score
    return sentences

# When all the sentences have an assigned score, this function goes over all the sentences and picks the sentence(s) with the highest score

def go_over_sentences(sentences):
    scores = sentences.values()
    highest_score = max(scores)
    core_sentence_counter = 0
    candidate_sentences = []
    for sentence, score in sentences.iteritems():
        if score == highest_score:
            core_sentence_counter += 1
    for sentence, score in sentences.iteritems():
        if score == highest_score and core_sentence_counter == 1:
            core_sentence = sentence
        if score == highest_score and core_sentence_counter > 1:
            candidate_sentences.append(sentence)
    if candidate_sentences:
        less_frequent_words = frequent_words[:5]
        sentences = perform_extra_check(candidate_sentences, less_frequent_words)
        scores = sentences.values()
        highest_score = max(scores)
        for sentence, score in sentences.iteritems():
            if score == highest_score:
                core_sentence = sentence
    return core_sentence

# Provide the directory here with all the articles that should be processed

directory='C:/Users/..'
csvfile = open('Results/results_abstract.csv', 'wb')
fieldnames = ['File', 'Sentence']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
writer.writeheader()

for file in os.listdir(directory):
    path = directory + file
    
    text = open(path)

    front = "==== Front"
    body = "==== Body"
    graphical_abstract = "Graphical Abstract"
    started = False
    abstract = ''
    
    for line in text:
        if body in line or graphical_abstract in line:
            started = False
        if started:
            abstract += line
        if front in line:
            started = True
    
    abstract = abstract.decode('utf-8')
    lines, frequent_words = determine_lines_and_frequent_words(abstract, path)
    sentences = assign_sentences_score(lines, frequent_words)
    core_sentence = go_over_sentences(sentences)
    core_sentence = core_sentence.replace('\n', ' ').replace(';',',')
    core_sentence = core_sentence.encode('utf-8')
    
    writer.writerow({'File': file, 'Sentence': core_sentence})
    
# DO NOT FORGET TO DECODE EXTRACTED RESULTS BEFORE NEXT STEP!