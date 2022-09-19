










from transformers import GPT2Model,GPT2Tokenizer,GPT2Config,BertModel,BertTokenizer,BertConfig
from summarizer import Summarizer,TransformerSummarizer


custom_config = GPT2Config.from_pretrained('gpt2/models',local_files_only=True)
custom_config.output_hidden_states = True
custom_tokenizer = GPT2Tokenizer.from_pretrained('gpt2/models',local_files_only=True)
custom_model = GPT2Model.from_pretrained('gpt2/models', config=custom_config)

model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
result = model(data, min_length=30, max_length=1000)
summary = "".join(result)



data='We assessed postoperative discomfort based on information captured by visual analogue scales .We included outcome data up to three months after randomisation for all outcomes except ureteral stricture formation; for this outcome, we also considered longer‐term data when available.'

data.encode('utf-8')
import requests
import json

url = "https://rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com/rewrite"

#payload = "{\r\n    \"language\": \"en\",\r\n    \"strength\": 3,\r\n    \"text\": data\r\n}"
payload = "{\r\"language\": \"en\",\r\"strength\": 3,\r\"text\": \""+data+"\"\r}"

headers = {
    'content-type': "application/json",
    'x-rapidapi-key': "2d8926693fmsh664f75bf9fe13e7p1d82a0jsne01e5012ea3e",
    'x-rapidapi-host': "rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com"
    }

response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)


resp_text = response.text
dictionary=json.loads(resp_text)
print(response.text)

