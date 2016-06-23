# Extracting-Core-Claims
An attempt to extract single core claims from scientific articles

In this project, an attempt is made to extract single core claims from scientific articles.

The code works as follows:

First, the core sentence is extracted from a scientific article. This is done in Extract_Sentence.py
In order to do this, the english stopwords list from NLTK is changed, therefore it is added here as well

When the core sentence is extracted, AIDA comes into place to check sentences. AIDA is a concept brought to life by Kuhn et al. [1] and offers a way to structure scientific claims. It is proposed as a tool for  researchers to easily access and communicate research hypotheses, claims and opinions. The rules of an AIDA sentence are used in this approach to determine whether we are dealing with a single claim or not.

Therefore, the second step is to check whether the core sentence complies with the rules of an AIDA sentence. If it does, a single claim is extracted from the article. If it does not, an attempt is made to rewrite the sentence in order to make it comply with these rules. This is all done in AIDA_Check.py

Tthe results of my project are also provided, feel free to use them for further improvements of the algorithm!

Cheers,

Tom 
