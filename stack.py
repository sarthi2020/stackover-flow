from stackapi import StackAPI
import json
import pymongo

site  = StackAPI("stackoverflow")
site.max_pages = 2
site.page_size = 75

myclient = pymongo.MongoClient()

# dblist = myclient.list_database_names()

# print(dblist)
# if "database" not in dblist:
mydb = myclient["database"]

# questions = site.fetch('posts', filter='withbody')

questions = site.fetch('questions', filter='withbody')
answers = site.fetch('answers', filter='withbody')

question_drop_list = ["is_answered","view_count","answer_count","score","owner"]
answer_drop_list = ["is_accepted","score","owner"]

for data in questions["items"]:
	for item in question_drop_list:
		data.pop(item)

for data in answers["items"]:
	for item in answer_drop_list:
		data.pop(item)

myquestions = mydb["questions"]
myanswers = mydb["answers"]

# myquestions.insert_many(json.dumps(questions['items']))
# myanswers.insert_many(json.dumps(answers['items']))

print(json.dumps(questions['items'],indent=4))
print(len(questions['items']))

# id = int(input("Enter question id \n"))
# for data in answers['items']:
# 	if(int(data["question_id"])-id == 0):
# 		# print(questions['items'][0])
# 		print(json.dumps(data, indent=4))
