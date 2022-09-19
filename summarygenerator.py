# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:06:57 2021

@author: Souparno
"""

import spacy
import pandas as pd
import re
from sentrank import SentenceRank
from daysstandard import standardizeddays
from collections import Counter
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



df=pd.DataFrame(columns=['PMCID','Title','Methodology Summarized'])
def SummarizerText(data1,sentences_required):
    global df
    data=data1

    for i in range(len(data)):
        ID=data['PMCID'][i]
        title=data['Title'][i]
        text=data['Methodology'][i]
        text=cleanhtml(text)
        text=remove_special_chars(text)
        text=standardizeddays(text)
        finalstr=SentenceRank(text,3)
       # print('data summarized ',i)
        try:
            df=df.append({'PMCID':ID,'Title':title,'Methodology Summarized':finalstr},ignore_index=True)
        except:
            pass
        
    temptext=''   
    for text in df['Methodology Summarized']:
        temptext+=text
        
    doc=nlp(temptext)
    sentences=[]
    repeatedsentences=[]
    for sent in doc.sents:
       # print(sent)
        if sent.text in sentences:
            repeatedsentences.append(sent.text)
        if sent.text not in sentences:
            sentences.append(sent.text)
    repeatsents=''
    count=dict(Counter(repeatedsentences))
    try:
        maxval=max(count.values())    
        for key,value in count.items():
            if maxval== value and maxval!=1:
                repeatsents+=key
    except:
        pass
    
    finaltext=repeatsents +''.join(sentences)
    MethodologyIMP=SentenceRank(finaltext,sentences_required)

    return MethodologyIMP
    
    
    