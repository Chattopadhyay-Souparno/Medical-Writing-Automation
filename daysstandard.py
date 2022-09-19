# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:05:55 2021

@author: Souparno
"""


import spacy
import re
nlp = spacy.load("en_core_web_lg")

def standardizeddays(t):
    doc = nlp(t) 
    for ent in doc.ents:
        #print(ent.text)
        if ent.label_=='TIME':
            #print(ent.text)
            temptext=ent.text
            #print(temptext)
            #### Hours --> Days ####
            hours=re.findall('\d+-*\s*hour',ent.text,re.IGNORECASE)
            if len(hours)!=0:
               # print(weeks)
                temp = re.findall(r'\d+', str(hours)) 
                days=int(temp[0])/24
                if int(days)>0:
                    newstr=str(days)+' day'
                else:
                    newstr=str(days)+' days'
                #ent.text.replace(weeks[0],newstr)
                t=t.replace(temptext,ent.text.replace(hours[0],newstr))

        if ent.label_=='DATE':
            temptext=ent.text
            #### Week --> Days ####
            weeks=re.findall('\d+-*\s*week',ent.text,re.IGNORECASE)
            if len(weeks)!=0:
               # print(weeks)
                temp = re.findall(r'\d+', str(weeks)) 
                days=int(temp[0])*7
                if int(days)>7:
                    newstr=str(days)+' day'
                else:
                    newstr=str(days)+' days'
                #ent.text.replace(weeks[0],newstr)
                t=t.replace(temptext,ent.text.replace(weeks[0],newstr))
            
            #### Month --> Days ####
            months=re.findall('\d+-*\s*month',ent.text,re.IGNORECASE)
            if len(months)!=0:
                #print(months)
                temp = re.findall(r'\d+', str(months)) 
                days=int(temp[0])*30
                if int(days)>30:
                    newstr=str(days)+' day'
                else:
                    newstr=str(days)+' days'
                #ent.text.replace(weeks[0],newstr)
                t=t.replace(temptext,ent.text.replace(months[0],newstr))
            
            #### Year --> Days ####
            years=re.findall('\d+-*\s*year',ent.text,re.IGNORECASE)
            if len(years)!=0:
                #print(months)
                temp = re.findall(r'\d+', str(years)) 
                days=int(temp[0])*365
                if int(days)>365:
                    newstr=str(days)+' day'
                else:
                    newstr=str(days)+' days'
                #ent.text.replace(weeks[0],newstr)
                t=t.replace(temptext,ent.text.replace(years[0],newstr))
    return t  


