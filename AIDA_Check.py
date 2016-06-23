# Import required libraries

import nltk, re, csv
from stat_parser import Parser, display_tree
parser = Parser()
from nltk.tree import Tree

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
    searchObj = re.search( r'(overall|in sum|therefore|thus|together|in conclusion|taken together|collectively|altogether|taken collectively|to conclude|conclusively|all together|all things considered|everything considered|as a result|consequently|conclusion)*.*(the|these|this|the present)*(study|results|findings|research|report|data|observation|experiment|publication|analysis|data set|dataset|we|it is)+.*(highlight|constitute|suggest|indicate|demonstrate|show|reveal|provide|illustrate|describe|conclude|support|establish|propose|advocate|determine|confirm|argue|impl|display|offer|underline|allow)+', sentence_lower, re.I)
    if searchObj != None:
        return False
    elif absolute_check.search(sentence_lower):
        return False
    elif re.search( r'is a(.){0,20}(candidate|contender|contestant)+', sentence) != None:
        return False
    elif "MD" in tags:
        return False
    else:
        return True

def make_absolute(sentence, tokenized, tagged):
    predictions = ["is predicted to", "is foreseen to", "is envisioned to"]
    searchObj = re.search( r'(overall|in sum|therefore|thus|together|in conclusion|taken together|collectively|altogether|taken collectively|to conclude|conclusively|all together|all things considered|everything considered|as a result|consequently|conclusion)*.*(the|these|this|the present)*(study|results|findings|research|report|data|observation|experiment|publication|analysis|data set|dataset|we|it is)+.*(hypothesis|highlight|constitute|suggest|indicate|demonstrate|show|reveal|provide|illustrate|describe|conclude|support|establish|propose|advocate|determine|confirm|argue|impl|display|offer|underline|allow|provide increased support for|found)+((.){0,10}(that))+', sentence, re.I)
    if searchObj != None:
        sentence = sentence.replace((searchObj.group() + " "), "")
    for prediction in predictions:
        if prediction in sentence:
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
    if "  " in sentence:
        sentence = sentence.replace("  ", " ")
    return sentence

def final_check(sentence):
    searchObj = re.search( r'(\d)*(\.)*( )*(Discussion|Results|Conclusions|Conclusion)+', sentence)
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

# The sentence that we're talking about is given here and some basic NLP tools do their work

sentence = "Topiramate is effective in the prophylactic treatment of migraine."
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
        print "The sentence is atomic."
        Atomic = True
    else:
        print "The sentence is not atomic."
        Atomic = False
    if check_if_independent(sentence):
        print "The sentence is independent."
        Independent = True
    else:
        print "The sentence is not independent."
        Independent = False
    if check_if_declarative(sentence, tags):
        print "The sentence is declarative."
        Declarative = True
    else:
        print "The sentence is not declarative."
        Declarative = False
    if check_if_absolute(sentence, sentence_lower, tags):
        print "The sentence is absolute."
        Absolute = True
    else:
        print "The sentence is not absolute."
        Absolute = False
    return Atomic, Independent, Declarative, Absolute

print "Sentence to check for AIDA compliancy: \n"
print sentence
print "\nResults: \n"

AIDA = perform_AIDA_check()
Atomic = AIDA[0]
Independent = AIDA[1]
Declarative = AIDA[2]
Absolute = AIDA[3]

# If it complies with all the rules, the sentence is printed
# Otherwise, the sentence will be rewritten

if Atomic == True and Independent == True and Declarative == True and Absolute == True:
    print "\nThe sentence complies with the AIDA rules."
else:
    print "\nThe sentence is now processed to comply with the AIDA rules..."
    if Atomic == False:
        sentence = make_atomic(sentence)
        Atomic = True
    if Independent == False:
        sentence = make_independent(sentence)
        Independent = True
    if Declarative == False:
        sentence = make_declarative(sentence, tags)
        Declarative = True
    if Absolute == False:
        sentence = make_absolute(sentence, tokenized, tagged)
        Absolute = True
    sentence = final_check(sentence)
    if Atomic == True and Independent == True and Declarative == True and Absolute == True:
        print "\nThe final version of the sentence is:\n"
        print sentence
