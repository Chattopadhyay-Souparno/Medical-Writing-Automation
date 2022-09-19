
requirements.txt file is available

methodology_bs4.py = Script to fetch the PMCIDs using Bio Python Package.
				  Using the PMCIDs , medical articles are webscrapped using 
				  selenium and beautiful_soup
				  
	#change the directory of chrome_driver as per your directory
	

sent_rank.py = script of implementation of Pytextrank as per our usecase

summarygenerator.py = google T5 + sent_rank(text rank algorithm) to generate Extractive 
					  Summarization
					  
keywordsgenerator.py =Gensim model to generate keywords and cosine similarity using spacy 
					  english large model to generate  Medical keywords
					  
daysstnadard.py = standardizes all the time and days quantities into days

main_file.py = to run the entire script without streamlit GUI

app_1.py = Streamlit GUI

	CLI command from the directory :
	streamlit run app_1.py runserver
	
	Transformer models on line 43,44 and 57,58 if not available locally 
	set local_files_only=False
	
	line 101 articles to be fetched from Pubmed is set to 5,
	uncomment line 100 to allow user to decide how many articles to be searched
	
	line 82, change the document save directory and uncomment 128 and 159 lines


correlated_words_0.py and gpt2method.py are not in use