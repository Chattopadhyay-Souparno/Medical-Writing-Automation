# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 11:47:11 2021

@author: Souparno
"""
import torch
#from transformers import AutoTokenizer, AutoModelWithLMHead
from transformers import T5Tokenizer, T5ForConditionalGeneration



from methodology_bs4 import *
#from correlated_words_0 import *
from summarygenerator import *

# tokenizer = AutoTokenizer.from_pretrained('t5-base',local_files_only=True)      ##local_files = False if downloading the model from hugging face
# model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True,local_files_only=True)   ##local_files = False if downloading the model from hugging face

tokenizer = T5Tokenizer.from_pretrained('t5-base',local_files_only=True)
model = T5ForConditionalGeneration.from_pretrained('t5-base', return_dict=True,local_files_only=True)



search_query=input('enter the relevant key words: ')
no_articles_fetched=input('enter the no. of articles to be fetched: ')


filename,df,meth_ids=Methodology(search_query,no_articles_fetched)
methodologysummary=Summarizer(filename,5)


inputs = tokenizer.encode("summarize: " + methodologysummary,
                          return_tensors='pt',
                          max_length=2048,
                          truncation=True)



summary_ids = model.generate(inputs, max_length=200, min_length=30, length_penalty=10.,num_return_sequences=10,early_stopping=False, num_beams=10)

summary = tokenizer.decode(summary_ids[0])

print(summary)

#data=pd.read_csv(filename)


#keywordframe=keywordExtraction(filename,search_query)

# name=search_query+' data+keywords.csv'
# keywordframe=keywordframe[['PMCID', 'Title', 'Methodology', 'keywords','Inclusion Criteria','Exclusion Criteria']]
# keywordframe.to_csv(name)

