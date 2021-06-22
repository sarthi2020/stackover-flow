import requests 
from bs4 import BeautifulSoup
import json

site = requests.get("https://stackoverflow.com/questions")

soup = BeautifulSoup(site.text, "html.parser")

questions_list = {
	"questions":[]
}

questions = soup.select(".question-summary")

for que in questions:
	q = que.select_one('.question-hyperlink').getText()
	vote_count = que.select_one('.vote-count-post').getText()
	questions_list["questions"].append(
		{"questions":q,"vote_count":vote_count})

json_data = json.dumps(questions_list)

print(json_data)