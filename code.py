import spacy
import csv
import sys
import requests
from bs4 import BeautifulSoup
from cleanco import prepare_terms, basename

nlp = spacy.load('en_core_web_sm') # Used for named entity recognition


def get_security_and_securities(text):
	'''
		This fuction returns security and securities from the given text.
	'''

	doc = nlp(text)
	security=None
	securities=[]
	for ent in doc.ents: 
		if ent.label_=='ORG':
			if security is None:
				security = ent.text   #Rule 1
			securities.append(ent.text)
	return security,securities	


def get_ticker_symbol(security,securities):
	''' 
		This function will return ticker symbol for security and securities. Since the training examples does not have them, this function
		scrapes ticker symbole from marketywatch website. 
	'''

	sec = basename(security, terms, prefix=False, middle=False, suffix=True).lower() #This is to remove thins like Inc., Ltd. fromt he comapny name 
	
	if sec == 'google':
		## I have hardcoded it here because Google is being reffered by its parent company Alphabet, yet a lot of people still use google.
		security = 'GOOG'
	else:
		page = requests.get('https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup='+str(sec)+'&Country=all&Type=All')
		soup = BeautifulSoup(page.content, 'html.parser')
		results = soup.find_all('div', class_='results') ## All the results are there in results div
		if len(results) > 0:
			security=results[0].text.strip().replace('\n',' ').split()[3]

	remove=[]
	for i in range(len(securities)):
		sec = basename(securities[i], terms, prefix=False, middle=False, suffix=True).lower()#This is to remove thins like Inc., Ltd. fromt he comapny name
		if sec == 'google':   
			## I have hardcoded it here because Google is being reffered by its parent company Alphabet, yet a lot of people still use google.
			securities[i]='GOOG'
			continue
		
		page = requests.get('https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup='+str(sec)+'&Country=all&Type=All')
		soup = BeautifulSoup(page.content, 'html.parser')
		results = soup.find_all('div', class_='results')
		if len(results) > 0 and any(sec in s.lower() for s in results[0].text.strip().replace('\n',' ').split()): #Second condition check if the company's name is what we want it to be.
			securities[i]=results[0].text.strip().replace('\n',' ').split()[3]
		else:
			remove.append(i)

	correct_securities=[] #Remove companies whose ticker symbol were wrong.
	j=0
	for i in range(len(securities)):
		if i not in remove:
			correct_securities.append(securities[i])

	return security,correct_securities

def apply_rule_2_and_3(security,securities):
	'''
		This function applies rule 2 and rule 3 as per the pdf given.
	'''

	temp=list(set(securities))
	if temp==securities:      
		security=securities[0]    #Rule 2 - all the companies occur only once, so we take first occuring company is set a security
	else:	
		security = max(set(securities), key = securities.count)     #Rule 3 - Most frequent occurin company is set a security
		securities=temp  # Since all the comapnies need to come only once

	return security,securities

def generate_output_file(input_file_name):
	''' 
		This function generates output file if it is given an input file with structure similar to the one provided for this task.
		The file will generate a new file naed output.csv and will add two columns, security and securities to it. If they are not present
		then the column would be empty.
	'''
	
	with open('output.csv','w',newline='') as output_file:
		with open(str(input_file_name),'r') as input_file: 
			lines = csv.reader(input_file)
			writer = csv.writer(output_file)
			counter=0
			
			for line in lines:
				if counter==0:
				## Header File
					line.append('SECURITY')
					line.append('SECURITIES')
					writer.writerow(line)
					counter=1
					continue

				title = line[1]
				if counter>3:
					break
				counter+=1
			    	
				security,securities=get_security_and_securities(title)
				if len(line)== 9:
					## This is call when article of the news is available.
					article = line[8]
					_,temp = get_security_and_securities(article)
					securities = securities + temp
					

				if security is None and len(securities)>0:
					## For rule 2 & 3
					security,securities = apply_rule_2_and_3(security,securities)
		      
				if security is not None:
					security,securities = get_ticker_symbol(security,securities)
					securities=str(securities)
					security=str(security)
					line.append(security)
					line.append(securities)
				
				writer.writerow(line)


if __name__ == "__main__":
	mode = int(sys.argv[1])
	terms = prepare_terms()
	try:
		if mode==0:
			input_file = sys.argv[2]
			print("Running for file: "+str(input_file))
			generate_output_file(input_file)
		elif mode==1:
			title = sys.argv[2]
			security,securities = get_security_and_securities(title)
			if len(sys.argv) > 3:
				article = sys.argv[3]
				_,temp = get_security_and_securities(article)
				securities = securities + temp

			if security is None and len(securities)>0:
				## For rule 2 & 3
				security,securities = apply_rule_2_and_3(security,securities)

			if security is not None:	
				security,securities = get_ticker_symbol(security,securities)

			securities=list(set(securities))	
			print('security: '+str(security))
			print('securities: '+str(securities))

	except Exception as e:
		print("Encountered following error: "+str(e))

