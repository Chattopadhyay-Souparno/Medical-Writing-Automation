# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 10:41:50 2021

@author: Souparno
"""


from Bio import Entrez
from bs4 import BeautifulSoup 
import re
import requests
import pandas as pd
from selenium import webdriver
from pytrials.client import ClinicalTrials

ct = ClinicalTrials()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
#driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)

driver = webdriver.Chrome(r'D://NLG_TCS_project//selected_scripts//chromedriver',chrome_options=options) 


#### removing the html tags ####
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')    
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext   


#### generating article ID ####
def search(query,no_of_articles):
    Entrez.email = ''
    handle = Entrez.esearch(db='pmc',
                            sort='relevance',
                            retmax=no_of_articles,
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


#### dataframe creation ####
df=pd.DataFrame(columns=['PMCID','Title','Methodology','Inclusion Criteria','Exclusion Criteria'])

#### taking user input for keywords #####
# search_query=input('enter the relevant key words: ')
# no_articles_fetched=input('enter the no. of articles to be fetched: ')


def Methodology(search_query,no_articles_fetched):
    global df
    search_query='methodology '+ search_query
    
    
    #### getting the article ids #####
    results = search(search_query,no_articles_fetched)
    id_list = results['IdList']
    #print('ids :',id_list)
    print('PMCIDs of the articles searched: ',*id_list)
    meth_ids=[]
    #### extracting the abstract
    for idno in id_list:
        print('____________________')
        print('PMCDID: ',idno)
        #### url for all articles is the same only the article id at the end changes #####
        url='https://www.ncbi.nlm.nih.gov/pmc/articles/PMC'+str(idno)+'/'
        try:
            driver.get(url)
            page_source = driver.page_source
    
            #r = requests.get(url) 
            soup = BeautifulSoup(page_source,'html5lib') 
            print('article fetched')
            ### initializing  an empty abstract string ####
            text=''
            
            #### extracting the title of the article
            title=cleanhtml(str(soup.find('h1', class_='content-title')))
            
            
            #### extracting the method section which is under abstract part ####
            #### in the html - h3 header is used for the same               ####
            h3methods = soup.select('h3:contains("Methods") ~ :not(h3:contains("Methods") ~ h3)')
            for i in h3methods:
                #print(type(i))
                text=text+cleanhtml(str(i))+'\n'
            #    print(text)
                #print('\n')
            
            #### extracting method section ####
            #### in the html - h2 header is used for the same               ####
            h2methods = soup.select('h2:contains("Methods") ~ div:not(h2:contains("Methods") ~ h2 ~ div)')
            for i in h2methods:
                #print(type(i))
                text=text+cleanhtml(str(i))+'\n'
             #   print(text)
                #print('\n')
                
            h2methods = soup.select('h2:contains("Materials and Methods") ~ div:not(h2:contains("Materials and Methods") ~ h2 ~ div)')
            for i in h2methods:
                #print(type(i))
                text=text+cleanhtml(str(i))+'\n'
             #   print(text)
                #print('\n')
    
            h2methods = soup.select('h2:contains("METHODS") ~ div:not(h2:contains("METHODS") ~ h2 ~ div)')
            for i in h2methods:
                #print(type(i))
                text=text+cleanhtml(str(i))+'\n'
             #   print(text)
                #print('\n')
    
            #### if the article fetched doesnot have method section         ####
            #### text string will not be appended                           ####
            #### if text= empty print no methodology present                ####
            if text=='':
                print(str(idno) +' no methodology present')
                
                
            
            if text!='':
                finalinc=''
                finalexc=''
                    
                nctid=re.findall(r'NCT[0-9]{8}',text)
                if len(nctid)!=0:
                    print('NCTID present')
                    nctid=list(set(nctid))
                    for i in nctid:
                        nctdict=ct.get_full_studies(search_expr=i)
                        eligibility=nctdict['FullStudiesResponse']['FullStudies'][0]['Study']['ProtocolSection']\
                        ['EligibilityModule']['EligibilityCriteria']
                        
                        eligibility=eligibility.split('Exclusion')
                          
                        #eligibility=eligibility.splitlines()
                        inccriteria=eligibility[0].splitlines()
                        inccriteria=inccriteria[2:]
                        inccriteria=','.join(inccriteria)
                        
                        finalinc=finalinc + i +'\n' + inccriteria +'\n'
                        
                        exccriteria=eligibility[1].splitlines()
                        exccriteria=exccriteria[2:]
                        exccriteria=','.join(exccriteria)
                        
                        finalexc=finalexc + i+'\n' +exccriteria +'\n'             
                else:
                    print('No NCTID present')
                
                
            #### if text is not empty then only append the data to the      ####
            #### dataframe                                                  ####
            if text!='':
                meth_ids.append(idno)
                df=df.append({'PMCID' : idno , 'Title' : title ,'Methodology': text,'Inclusion Criteria':finalinc,'Exclusion Criteria':finalexc}, ignore_index=True)
                print(str(idno) +' methodology found')
            
        except:
            print('too long to open the page')
            
    #### save the data frame into csv #####
    file_name=search_query+' data.csv'
#    df.to_csv(file_name, encoding='utf-8-sig')
    return file_name,df,meth_ids

