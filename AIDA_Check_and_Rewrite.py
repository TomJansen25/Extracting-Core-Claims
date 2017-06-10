# -*- coding: utf-8 -*-
# Import required libraries

import nltk, re, csv
from stat_parser import Parser, display_tree
parser = Parser()
from nltk.tree import Tree
from nltk.stem.wordnet import WordNetLemmatizer

# Define all the lists that are checked for the requirements

not_atomic_list = ["and that", "and also", "but ", "so that", "while ", "however ", "whereas ", "on the other hand", "in addition to", "respectively", "as well as", "thereby", "though ",  "thus ", " hence ", "therefore", "yet ", " including ", "in contrast", "contrary to", " beside", "aside from", "other than", "explaining", "which explains"]
not_independent_list = ["this study ", "our study", "the results ", "results ", "the findings ", "the present study ", "these findings ", "these results ", "this research ", "this data ", "the data ", "these data", "our data", "these observations", "this experiment ", "this publication ", "this analysis", "these analyses", "evidence", "this paper ", "the paper ", "this report ", "the report ", "this effect ", "we ", "compared with", "and other", "previous ", "previously", "the bacterium "]
not_declarative_list = ["?", "!"]
not_absolute_list = ["probabl", "perhaps", "potentially", "putative", "maybe", "plausible", "possible", "likely", "feasible", "hypothetical", "may", "could ", " seem ", "appears to", "appear to", " appear ", " might ", " suggest ", "minimally sufficient", "is predicted", "is foreseen", "is envisioned", "revealed that", "reveals that", "significant", "significantly", "to reveal", " estimated ", " estimate"]

# From here on, all the functions are defined that check whether the sentence fulfills the AIDA rules,
# and if they do not, the sentence is rewritten with individual functions per requirement
# (Yes, for the moment nothing is done when a sentence is not atomic or not independent..)

def check_if_atomic(sentence, parsed_sentence, tags):
    counter = 0
    atomic_check = re.compile("|".join(not_atomic_list))
    tree = Tree('s', parsed_sentence)
    for child in tree:
        string = str(child)
        if string.startswith("(S"):
            counter += 1
    if atomic_check.search(sentence_lower):
        return False
    elif counter > 1:
        return False
    else:
        return True

def make_atomic(sentence):
    return sentence

def check_if_independent(sentence):
    independent_check = re.compile("|".join(not_independent_list))
    if independent_check.search(sentence_lower):
        return False
    else:
        return True
    
def make_independent(sentence):
    return sentence
    
def check_if_declarative(sentence, tags):
    if sentence[0].isupper() == False:
        if sentence[1].isupper() == False:
            return False
        else:
            return True
    elif sentence[-1] != ".":
        return False
    elif "NN" not in tags and "NNP" not in tags and "NNPS" not in tags and "NNS" not in tags:
        return False
    elif "?" in sentence or "!" in sentence:
        return False
    elif "VB" not in tags and "VBN" not in tags and "VBP" not in tags and "VBZ" not in tags and "VBD" not in tags:
        return False
    else:
        return True
    
def make_declarative(sentence, tags):
    if sentence[-1] == "!":
        sentence = sentence[:-2] + "."
    elif sentence[-1] != "." and sentence[-1] != "!" and sentence[-1] != "?":
        sentence = sentence + "."
    if sentence[0].isupper() == False:
        if sentence[1].isupper() == False:
            return False
        else:
            return True
    return sentence
        
def check_if_absolute(sentence, sentence_lower, tags):
    absolute_check = re.compile("|".join(not_absolute_list))
    searchObj = re.search( r'(the|these|this|the present)*(study|results|findings|research|report|data|observation|experiment|publication|analysis|data set|dataset|we|it is)+.*(highlight|constitute|suggest|indicate|demonstrate|show|reveal|provide|illustrate|describe|conclude|support|establish|propose|advocate|determine|confirm|argue|impl|display|offer|underline|allow)+', sentence_lower, re.I)
    if searchObj != None:
        return False
    elif absolute_check.search(sentence_lower):
        return False
    elif re.search( r'is a(.){0,20}(candidate|contender|contestant)+', sentence) != None:
        return False
    elif "MD" or "VBD" in tags:
        return False
    else:
        return True

def make_absolute(sentence, tokenized, tagged):
    sentence = sentence.decode('utf-8')
    predictions = ["is predicted to", "is foreseen to", "is envisioned to"]
    searchObj = re.search( r'(overall|in sum|therefore|thus|together|in conclusion|taken together|collectively|altogether|taken collectively|to conclude|conclusively|all together|all things considered|everything considered|as a result|consequently|conclusion)*.*(the|these|this|the present)*(study|results|findings|research|report|data|observation|experiment|publication|analysis|data set|dataset|we|it is)+.*(hypothesis|highlight|constitute|suggest|indicate|demonstrate|show|reveal|provide|illustrate|describe|conclude|support|establish|propose|advocate|determine|confirm|argue|impl|display|offer|underline|allow|provide increased support for|found)+((.){0,10}(that))+', sentence, re.I)
    if searchObj != None:
        sentence = sentence.replace((searchObj.group() + " "), "")
    for prediction in predictions:
        if prediction in sentence:
            for i, tag in enumerate(tagged):
                if tag[0] == "predicted" or tag[0] == "foreseen" or tag[0] == "envisioned" and tagged[i-1][0] == "is" and (tagged[i-2][1] == "NNP" or tagged[i-2][1] == "NN"):
                    replace = str(tagged[i+2][0])
                    sentence = sentence.replace(replace, replace + "s")
                    sentence = sentence.replace(prediction, "")
                else:
                    sentence = sentence.replace(prediction, "")
    for i, tag in enumerate(tagged):
        if tag[1] == "MD" and (tagged[i-1][1] == "NNS" or tagged[i-1][1] == "NNPS") and tokenized[i+1] == "be":
            replace = str(tag[0] + " " + tokenized[i+1])
            sentence = sentence.replace(replace, "are")
        if tag[1] == "MD" and (tagged[i-1][1] == "NN" or tagged[i-1][1] == "NNP") and tokenized[i+1] == "be":
            replace = str(tag[0] + " " + tokenized[i+1])
            sentence = sentence.replace(replace, "is")
        if tag[1] == "MD" and tokenized[i+1] == "be":
            replace = str(tag[0] + " " + tokenized[i+1])
            sentence = sentence.replace(replace, "is")
        if tag[1] == "MD" and tokenized[i+1] != "be" and (tagged[i-1][1] == "NNS" or tagged[i-1][1] == "NNPS"):
            replace = str(tag[0] + " " + tokenized[i+1])
            sentence = sentence.replace(replace, tokenized[i+1])
        if tag[1] == "MD" and tokenized[i+1] != "be":
            replace = str(tag[0] + " " + tokenized[i+1])
            sentence = sentence.replace(replace, tokenized[i+1] + "s")
        if tag[0] in not_absolute_list:
            sentence = sentence.replace(tag[0], "")
        if tag[1] == "VBD" and tag[0] == "was":
            sentence = sentence.replace(tag[0], "is")
        if tag[1] == "VBD" and tag[0] == "were":
            sentence = sentence.replace(tag[0], "are")
        if tag[1] == "VBD" and tag[0] == "had" and (tagged[i-1][1] == "NNS" or tagged[i-1][1] == "NNPS"):
            sentence = sentence.replace(tag[0], "have")
        if tag[1] == "VBD" and tag[0] == "had" and (tagged[i-1][1] == "NN" or tagged[i-1][1] == "NNP"):
            sentence = sentence.replace(tag[0], "has")
        if tag[1] == "VBD" and (tagged[i-1][1] == "NNS" or tagged[i-1][1] == "NNPS"):
            replace = WordNetLemmatizer().lemmatize(tag[0],'v')
            sentence = sentence.replace(tag[0], replace)
        if tag[1] == "VBD" and (tagged[i-1][1] == "NN" or tagged[i-1][1] == "NNP"):
            replace = WordNetLemmatizer().lemmatize(tag[0],'v')
            sentence = sentence.replace(tag[0], replace + "s")
    if "  " in sentence:
        sentence = sentence.replace("  ", " ")
    return sentence

def final_check(sentence):
    searchObj = re.search( r'(\d)*(\.)*( )*(Results:|Conclusions:|Conclusion:|Discussion:|Discussion|Results|Conclusions|Conclusion|Findings)+', sentence)
    if searchObj != None:
        sentence = sentence.replace(searchObj.group(), "")
    headings = ["\nDiscussion\n", "\nMain findings\n", "\nConclusions\n", "\nKey findings\n", "\nConclusion\n", "\nResults\n", "Discussion\n", "Main findings\n", "Conclusions\n", "Key findings\n", "Conclusion\n", "Results\n"]
    for heading in headings:
        if heading in sentence:
            sentence = sentence.replace(heading, "")
    if "\n" in sentence:
        sentence = sentence.replace("\n", " ")
    if sentence.startswith("  "):
        sentence = sentence[2:]
    if sentence.startswith(" "):
        sentence = sentence[1:]
    if sentence[0].isupper() == False:
        if sentence[1].isupper() == False:
            sentence = sentence[0].upper() + sentence[1:]
    return sentence

csvfile = open('Results/results_AIDA_check_1.csv', 'wb')
fieldnames = ['Sentence', 'Atomic', 'Independent', 'Declarative', 'Absolute', 'AIDA', 'Rewritten_Sentence']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
writer.writeheader()

# After processing, provide the path of the file where the results are stored. 

sentences = []
extracted_sentences = open('C:/Users/../Results/results_abstract.csv')
extracted_reader = csv.DictReader(extracted_sentences, delimiter='|')
for row in extracted_reader:
    sentences.append(row['Sentence'])

for sentence in sentences:
    sentence = sentence.decode('utf-8')
    sentence_lower = sentence.lower()
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    tags = []
    for tag in tagged:
        tags.append(tag[1])
    parsed = parser.parse(sentence)

    # Here, the given sentence is checked against every requirement and given a True or False based on whether it fulfills that rule or not

    def perform_AIDA_check():
        if check_if_atomic(sentence, parsed, tags):
            Atomic = True
        else:
            Atomic = False
        if check_if_independent(sentence):
            Independent = True
        else:
            Independent = False
        if check_if_declarative(sentence, tags):
            Declarative = True
        else:
            Declarative = False
        if check_if_absolute(sentence, sentence_lower, tags):
            Absolute = True
        else:
            Absolute = False
        return Atomic, Independent, Declarative, Absolute
    
    Atomic, Independent, Declarative, Absolute = perform_AIDA_check()
    
    if Atomic == True and Independent == True and Declarative == True and Absolute == True:
        AIDA = True
    else:
        AIDA = False
        if Atomic == False:
            rewritten_sentence = make_atomic(sentence)
        if Independent == False:
            rewritten_sentence = make_independent(sentence)
        if Declarative == False:
            rewritten_sentence = make_declarative(sentence, tags)
        if Absolute == False:
            rewritten_sentence = make_absolute(sentence, tokenized, tagged)
        rewritten_sentence = final_check(rewritten_sentence)
        rewritten_sentence = rewritten_sentence.encode('utf-8')
    sentence = sentence.encode('utf-8')
    
    writer.writerow({'Sentence': sentence, 'Atomic': Atomic, 'Independent': Independent, 'Declarative': Declarative, 'Absolute': Absolute, 'AIDA': AIDA, 'Rewritten_Sentence': rewritten_sentence})