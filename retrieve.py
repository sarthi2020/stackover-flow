import json
import pymongo
import xmltodict
import pprint 
import pandas as pd
import xml.etree.ElementTree as ET
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import time
import tracemalloc

tracemalloc.start()

# conn = mysql.connector.connect(user='root', 
#                                password='', 
#                                host='localhost', 
#                                database='database')

#For printing 

start_time = time.time()

pp = pprint.PrettyPrinter(indent=4)

#To get xml data and convert it to json
with open("/Users/ishaan/Desktop/stackExchange/devops.stackexchange.com/Posts.xml") as postsxml:
	data_dict = xmltodict.parse(postsxml.read())

postsxml.close()

#dump data to json data 
json_data = json.dumps(data_dict,indent=4)

#load json data
data = json.loads(json_data)

#printing json data
pp.pprint(data["posts"]["row"][0])
print("Total posts  " + str(len(data["posts"]["row"])))

unique_attributes = ['@OwnerDisplayName', '@ClosedDate', '@ContentLicense',
 '@Tags', '@Id', '@LastActivityDate', '@LastEditorUserId', '@ViewCount', 
 '@FavoriteCount', '@CommentCount', '@LastEditorDisplayName', '@AnswerCount', 
 '@LastEditDate', '@CommunityOwnedDate', '@AcceptedAnswerId', '@OwnerUserId', 
'@PostTypeId', '@Title', '@ParentId', '@CreationDate', '@Score', '@Body']

# lst = list(data["posts"]["row"][0].keys())
# print(lst)
# count_list = []

# for index,value in enumerate(data["posts"]["row"]):
# 	a = list(value.keys())
# 	count_list.append(len(a))  #for count of unique attributes
# 	lst.extend(a)  # to get a list of unique attributes
# 	b = lst
# 	if(a!=b):
# 		count += 1
# 		# print(index)
# print(count)

#printing unique attributes
# print(set(lst))

# get count of unique attributes in a json data
# sns.countplot(y=count_list)
# plt.show()

questions = {"data" : []}
answers = {"data" : []}
other = {"data" : []}

def preprocessing(data):
	for index,item in enumerate(data):
		if(item['@PostTypeId']=='1'):
			questions["data"].append(item)
		elif(item['@PostTypeId']=='2'):
			answers["data"].append(item)
		else:
			other["data"].append(item)


preprocessing(data["posts"]["row"])
print("Questions  " + str(len(questions["data"])))
print("Answers  " + str(len(answers["data"])))
print("Other  " + str(len(other["data"])))

print("\nTIME TAKEN= ", "{:.2f} seconds\n".format(time.time()-start_time))

final_questions = {"data":[]}
final_answers = {"data":[]}

question_keys = ['@Id','@Tags','@ContentLicense','@AnswerCount','@AcceptedAnswerId',
'@ViewCount','@Title','@CreationDate','@Body','@OwnerUserId','@LastActivityDate']

answer_keys = ['@Id','@ParentId','@ContentLicense','@CreationDate','@Body','@OwnerUserId','@LastActivityDate']

def questions_preprocessing(data):
	count_of_code_snippets = 0
	for index, item in enumerate(data):
		soup = BeautifulSoup(item["@Body"], "html.parser")
		# print("<>=================================<>")
		if(soup.pre != None):
			temp = {}
			for key in question_keys:
				if(key in item.keys()):
					temp[key] = item[key]
				else:
					temp[key] = ""
			temp['@Code'] = [tag for tag in soup.find_all('pre')]
			
			final_questions["data"].append(temp)
		
			count_of_code_snippets+=len(temp['@Code'])
	
	return count_of_code_snippets

def answers_preprocessing(data):
	count_of_code_snippets = 0
	for index, item in enumerate(data):
		soup = BeautifulSoup(item["@Body"], "html.parser")
		# print("<>=================================<>")
		if(soup.pre != None):
			temp = {}
			for key in answer_keys:
				if(key in item.keys()):
					temp[key] = item[key]
				else:
					temp[key] = ""
			temp['@Code'] = [tag for tag in soup.find_all('pre')]
			
			final_answers["data"].append(temp)
		
			count_of_code_snippets+=len(temp['@Code'])
	
	return count_of_code_snippets

c1 = questions_preprocessing(questions["data"])
print("code snippets in questions")
print(c1)


c2 = answers_preprocessing(answers["data"])
print("code snippets in answers")
print(c2)

print("Total Number of questions with code snippets", len(final_questions["data"]))
print("Total Number of answers with code snippets", len(final_answers["data"]))
print("\nTIME TAKEN= ", "{:.2f} seconds\n".format(time.time()-start_time))

pp.pprint(final_questions["data"][1])
pp.pprint(final_answers["data"][1])

# trying to convert json data to pandas
df = pd.json_normalize(data["posts"]["row"])
print(df.sample(3))

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
tracemalloc.stop()
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

