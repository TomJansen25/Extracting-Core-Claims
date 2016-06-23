# -*- coding: utf-8 -*-
# Import the required libraries

import nltk, re, csv
from nltk.corpus import stopwords
from collections import Counter
import json

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

# Define core and non-core words

core_words = ["highlight", "constitute", "suggest", "indicate", "demonstrate", "show", "reveal", "provide", "illustrate", "describe", "conclude", "support", "establish", "propose", "advocate", "determine", "confirm", "argue", "imply", "display", "offer", "highlights", "constitutes", "suggests", "indicates", "demonstrates", "shows", "reveals", "provides", "illustrates", "describes", "concludes", "supports", "establishes", "proposes", "advocates", "determines", "confirms", "argues", "implies", "displays", "offers", "underlines", "underline", "underlined", "overall", "sum", "therefore", "thus", "together", "conclusion", "collectively", "altogether", "conclude", "conclusively", "consequently", "study", "results", "findings", "research", "report", "data", "paper", "observations", "experiment", "publication", "analysis"]

non_core_words = ["sought", "addition", "well-replicated", "replicated", "sample", "aimed", "aims", "questionnaire", "survey", "based", "interviews", "cross-sectional", "participants", "descriptive", "CI ", "%"] 

# Function that seperates all the lines and creates a list of the most frequent words in the provided text

def determine_lines_and_frequent_words(text):
    lines = sent_detector.tokenize(text.lower())
    base_words = nltk.tokenize.casual.casual_tokenize(text.lower())
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
        searchObj = re.search( r'(overall|in sum|therefore|thus|together|in conclusion|taken together|collectively|altogether|taken collectively|to conclude|conclusively|all together|all things considered|everything considered|as a result|consequently|conclusion)*.*(the|these|this|the present)*(study|results|findings|research|report|data|observation|experiment|publication|analysis|data set|we)+.*(highlight|constitute|suggest|indicate|demonstrate|show|reveal|provide|illustrate|describe|conclude|support|establish|propose|advocate|determine|confirm|argue|impl|display|offer|underline|allow|found)+', line, re.I)
        if searchObj != None:
            score += 100
        searchObj = re.search( r'\[(\d+)((,*)(\s)*(\d+)*)*\]', line, re.I)
        if searchObj != None:
            score -= 10
        for word in words:
            if word in core_words and line.count(word) == 1:
                score += 3
            if word in frequent_words and line.count(word) == 1:
                score += 1
            if word in non_core_words:
                score -= 2
        sentences[line] = score
    return sentences

# In some cases, two sentences end up with the same score, in such a case an every check is performed to make sure only one sentence is chosen in the end

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

#core_sentences = {}
output = open('output.txt', 'w')

text = "A new approach to functionalize the surface of polyester textiles is described in this study. Functionalization was achieved by incorporating pH/temperature-responsive polyelectrolyte microgels into the textile surface layer using UV irradiation. The aim of functionalization was to regulate polyester wettability according to ambient conditions by imparting stimuli-responsiveness from the microgel to the textile itself. Microgels consisted of pH/thermo-responsive microparticles of poly(N-isopropylacrylamide-co-acrylic acid) either alone or complexed with the pH-responsive natural polysaccharide chitosan. Scanning Electron Microscopy, X-ray Photoelectron Spectroscopy, ζ-potential measurements, and topographical analysis were used for surface characterization. Wettability of polyester textiles was assessed by dynamic wetting, water vapor transfer, and moisture regain measurements. One of the main findings showed that the polyester surface was rendered pH-responsive, both in acidic and alkaline pH region, owing to the microgel incorporation. With a marked relaxation in their structure and an increase in their microporosity, the functionalized textiles exhibited higher water vapor transfer rates both at 20 and 40 °C, and 65% relative humidity compared with the reference polyester. Also, at 40 °C, i.e., above the microgel Lower Critical Solution Temperature, the functionalized polyester textiles had lower moisture regains than the reference. Finally, the type of the incorporated microgel affected significantly the polyester total absorption times, with an up to 300% increase in one case and an up to 80% decrease in another case. These findings are promising for the development of functional textile materials with possible applications in biotechnology, technical, and protective clothing."
text = text.decode('utf-8')

lines = determine_lines_and_frequent_words(text)[0]
frequent_words = determine_lines_and_frequent_words(text)[1]
sentences = assign_sentences_score(lines, frequent_words)
core_sentence = go_over_sentences(sentences)
#core_sentences[text] = core_sentence

print core_sentence
output.write(core_sentence)
#output.write("\n".join(core_sentences))
#json.dump(core_sentences, open("Abstracts_1.txt",'w'))