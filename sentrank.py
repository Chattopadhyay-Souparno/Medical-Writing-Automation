# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 09:59:07 2021

@author: Souparno
"""


import spacy
import pytextrank
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
nlp = spacy.load('en_core_web_lg')
nlp.add_pipe("textrank", last=True)




def SentenceRank(text,no_of_sentences):
    doc = nlp(text)
    
    # examine the top-ranked phrases in the document
    sentences=[]
    for p in doc.sents:
        if not p.text.isspace():
            sentences.append(p.text)
        
    v=np.zeros((300,1))  
    for p in doc.sents:
        #print(p)
        if not p.text.isspace():
            v=np.append(v,p.vector.reshape(-1,1),axis=1)
        #print(1)    
        
    v=v[:,1:]
    
    
    sim_mat = np.zeros([len(sentences), len(sentences)])
    
    for i in range(len(sentences)):
      for j in range(len(sentences)):
        if i != j:
          sim_mat[i][j] = cosine_similarity(v[:,i].reshape(1,300), v[:,j].reshape(1,300))[0,0]
          
          
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
    
    
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    
    finalstr=''
    for i in range(no_of_sentences):
        try:
            finalstr+=''+ranked_sentences[i][1]
        except:
            pass
    #print(finalstr)
    return finalstr