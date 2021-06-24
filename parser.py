import json
# import pymongo
# import xmltodict
import pprint 
# import pandas as pd
import xml.etree.ElementTree as ET
# import mysql.connector
# import seaborn as sns
# import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import time
import xml.parsers.expat
import tracemalloc

tracemalloc.start()

xml_file = '/Users/ishaan/Desktop/stackExchange/devops.stackexchange.com/Posts.xml'
BATCH_SIZE = 1000

questions = {"data" : []}
answers = {"data" : []}
other = {"data" : []}

# final_questions = {"data":[]}
# final_answers = {"data":[]}

start_time = time.time()

pp = pprint.PrettyPrinter(indent=4)

unique_attributes = ['OwnerDisplayName', 'ClosedDate', 'ContentLicense',
 'Tags', 'Id', 'LastActivityDate', 'LastEditorUserId', 'ViewCount', 
 'FavoriteCount', 'CommentCount', 'LastEditorDisplayName', 'AnswerCount', 
 'LastEditDate', 'CommunityOwnedDate', 'AcceptedAnswerId', 'OwnerUserId', 
'PostTypeId', 'Title', 'ParentId', 'CreationDate', 'Score', 'Body']

question_keys = ['Id','Tags','ContentLicense','AnswerCount','AcceptedAnswerId',
'ViewCount','Title','CreationDate','Body','OwnerUserId','LastActivityDate']

answer_keys = ['Id','ParentId','ContentLicense','CreationDate','Body','OwnerUserId','LastActivityDate']



def preprocessing(item):
	if(item['PostTypeId']=='1'):
		questions['data'].append(item)
	elif(item['PostTypeId']=='2'):
		answers['data'].append(item)
	else:
		other['data'].append(item)

def questions_preprocessing(data):
	count_of_code_snippets = 0
	final_questions = {"data":[]}

	for index, item in enumerate(data):
		soup = BeautifulSoup(item["Body"], "html.parser")
		# print("<>=================================<>")
		if(soup.pre != None):
			temp = {}
			for key in question_keys:
				if(key in item.keys()):
					temp[key] = item[key]
				else:
					temp[key] = ""
			temp['Code'] = [tag for tag in soup.find_all('pre')]
			
			final_questions["data"].append(temp)
		
			count_of_code_snippets+=len(temp['Code'])
	
	return (final_questions,count_of_code_snippets)

def answers_preprocessing(data):
	count_of_code_snippets = 0
	final_answers = {"data":[]}

	for index, item in enumerate(data):
		soup = BeautifulSoup(item["Body"], "html.parser")
		# print("<>=================================<>")
		if(soup.pre != None):
			temp = {}
			for key in answer_keys:
				if(key in item.keys()):
					temp[key] = item[key]
				else:
					temp[key] = ""
			temp['Code'] = [tag for tag in soup.find_all('pre')]
			
			final_answers["data"].append(temp)
		
			count_of_code_snippets+=len(temp['Code'])
	
	return (final_answers,count_of_code_snippets)

# tree = ET.parse('/Users/ishaan/Desktop/stackExchange/devops.stackexchange.com/Posts.xml')
# root = tree.getroot()
# print(root.tag)
# print(root.attrib)
# for index,item in enumerate(root):
# 	if(index < 5):
# 		print(item.attrib)
# print(len(root))	

total_count = 0
question_code_snippets = 0
answer_code_snippets = 0

questions_count = 0
answers_count = 0
other_count = 0

final_questions_count = 0
final_answers_count = 0

for event, elem in ET.iterparse(xml_file, events=('start','end')):
	if(elem.tag == "row"):
		dict = elem.attrib
		# print(total_count)
		# print(BATCH_SIZE)
		# print(total_count%BATCH_SIZE)
		if(event == 'start'):
			preprocessing(dict)
		elif(event == 'end'):
			total_count += 1
			elem.clear()
		
	if((total_count%BATCH_SIZE == 0 and total_count > 0) or elem.tag == "posts"):
		print(total_count)

		(final_questions,qc) = questions_preprocessing(questions["data"])
		(final_answers, ac) = answers_preprocessing(answers["data"])
		
		question_code_snippets+=qc
		answer_code_snippets+=ac
		
		questions_count+=len(questions["data"])
		answers_count+=len(answers["data"])
		other_count+=len(other["data"])

		final_questions_count+=len(final_questions["data"])
		final_answers_count+=len(final_answers["data"])
		#SAVING FINAL QUESTIONS
		questions["data"].clear()
		answers["data"].clear()
		other["data"].clear()
			# pp.pprint(dict)
		# print("<>===============================<>")



# pp.pprint(final_questions)
# pp.pprint(final_answers)

print("code snippets in questions")
print(question_code_snippets)


print("code snippets in answers")
print(answer_code_snippets)

print("Total questions with code snippets ", final_questions_count)
print("Total answers with code snippets ", final_answers_count)

if(len(other["data"])+len(answers["data"])+len(questions["data"]) != 0):
	print(len(questions["data"]))
	print(len(answers["data"]))
	print(len(other["data"]))

print("Total questions ",questions_count)
print("Total Answers ",answers_count)
print("Other ",other_count)
print("{:,}".format(total_count))

print("\nTIME TAKEN= ", "{:.2f} seconds\n".format(time.time()-start_time))

pp.pprint(final_questions["data"][0])
pp.pprint(final_answers["data"][0])

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
tracemalloc.stop()

# #printing json data
# pp.pprint(data["posts"]["row"][0])
# print("Total posts  " + str(len(data["posts"]["row"])))


# preprocessing(data["posts"]["row"])
# print("Questions  " + str(len(questions["data"])))
# print("Answers  " + str(len(answers["data"])))
# print("Other  " + str(len(other["data"])))









# #dump data to json data 
# json_data = json.dumps(data_dict,indent=4)

# #load json data
# data = json.loads(json_data)

# # trying to convert json data to pandas
# df = pd.json_normalize(data["posts"]["row"])
# print(df.sample(3))
# df = pd.read_json(data)


#trying to do the same
# def intr_docs(xml_doc):
# 	attr = xml_doc.attrib

# 	for xml in xml_doc.iter('document'):
# 		doc_dict = attr.copy()
# 		doc_dic.update(xml.attrib)
# 		doc_dict['data'] = xml.text

# 		yield doc_dict

# tree = ET.parse('/Users/ishaan/Desktop/stackExchange/devops.stackexchange.com/Posts.xml')
# root = tree.getroot()
# print(root)
# print(len(root))	
# doc_df = pd.DataFrame(list(intr_docs(root)))

# print(doc_df)

