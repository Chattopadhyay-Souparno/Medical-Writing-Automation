# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 10:49:58 2021

@author: Souparno
"""

from gensim.summarization import keywords
import spacy
import re
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
nlp = spacy.load("en_core_web_lg")

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')    
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext 

def remove_special_chars(x):
    x=re.sub(r'\[.*\]','',x) 
    x = re.sub(r"<[^>]*>","",x)      # removes html tags
    x=re.sub(r'\([^)]*\)', '', x)    # removes parentheses '()'
    x = ' '.join(x.split())
    x = re.findall('[A-Z][^A-Z]*', x) # splits any joint words
    x=''.join(x)
    return x



def keywords_gen(df,search_query):
    
    keyw=[]
    for text in df['Methodology']:
       # print(text)
        new=remove_special_chars(text)
        new=new.lower()
        new=cleanhtml(new)
        
        
        keyw.extend(keywords(text).split('\n'))
    
    
    
    keyw=list(set(keyw))
    
    keyword=nlp(search_query)
    finalkeys=[]
    for token in keyw:
        totalsim=0
        for token2 in keyword:
            sim=nlp(token).similarity(token2)
            totalsim=totalsim+sim
        
        avgsim=totalsim/len(keyword)
        finalkeys.append((token,avgsim))
        finalkeys.sort(reverse=True,key = lambda x: x[1])  
    
    medicalkeyw=[]
    for i in finalkeys:
        if i[1]>0.35:
            #print(i)
            medicalkeyw.append(i[0])
    return keyw,medicalkeyw
