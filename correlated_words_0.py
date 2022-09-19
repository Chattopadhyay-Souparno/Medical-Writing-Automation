# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:09:55 2021

@author: Souparno
"""


import pandas as pd
import string
import spacy
import re
from collections import Counter 
nlp = spacy.load("en_core_web_lg")

# data=pd.read_csv('methodology smallpox vaccine data.csv')
#text=data['Methodology'][5]

def remove_special_chars(x):
    x=re.sub(r'\[.*\]','',x) 
    x = re.sub(r"<[^>]*>","",x)      # removes html tags
    x=re.sub(r'\([^)]*\)', '', x)    # removes parentheses '()'
    x = ' '.join(x.split())
    x = re.findall('[A-Z][^A-Z]*', x) # splits any joint words
    x=''.join(x)
    return x
index=0
# data['keywords']=''

def keywordExtraction(filename,search_query):
    data=pd.read_csv(filename)
    data['keywords']=''
    global index
    for text in data['Methodology']:
        
        new=remove_special_chars(text)
        new=new.lower()
        doc=nlp(new)
        
        
        words=[]
        for token in doc:
            if not token.is_stop:
                if token.text not in string.punctuation:
                        words.append(token.lemma_)
                      
        wordfreq =Counter(words)
        mostcommon=wordfreq.most_common(15)   # 15 most freq. words
        removewords=[]
        for i in mostcommon:
            if i[1]>10:
                removewords.append(i[0])
        
        words=list(set(words)-set(removewords))
        doc = ' '.join(words)
        doc=nlp(doc)
        
        correlated_words={}
        
        for token1 in doc:
            correlated_words[token1.text]=[]
            for token2 in doc:
                if token2.text not in correlated_words.keys():
                    if token1.similarity(token2) > 0.5 and token1!=token2:
                        correlated_words[token1.text].append(token2.text)
              
        filtered = {k: v for k, v in correlated_words.items() if v }
        correlated_words.clear()
        correlated_words.update(filtered)
                
        ##### added later ######
        #keydoc=nlp(' '.join(list(correlated_words.keys())))
        keyword=nlp(search_query)
        finalkeys=[]
        for token in list(correlated_words.keys()):
            totalsim=0
            for token2 in keyword:
                sim=nlp(token).similarity(token2)
                totalsim=totalsim+sim
            
            avgsim=totalsim/len(keyword)
            finalkeys.append((token,avgsim))
            finalkeys.sort(reverse=True,key = lambda x: x[1])  
        
        final=[]
        for i in finalkeys:
            if i[1]>0.5:
                #print(i)
                final.append(i[0])
        
        
        
        
        
        unwanted = set(correlated_words.keys()) - set(final)
        
        for unwanted_key in unwanted: del correlated_words[unwanted_key]
        
        values=list(correlated_words.values())+list(correlated_words.values())
        
        finalkeywords=[]
        for i in values:
            for j in i:
                finalkeywords.append(j)
                
        finalkeywords=set(finalkeywords)
        print('index :',index)
        print(finalkeywords)
        
        data['keywords'][index]=' '.join(finalkeywords)
        index=index+1
        
    #data.to_csv('keywords.csv')
    return data