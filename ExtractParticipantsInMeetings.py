import pickle as p, re
from nltk.tag import StanfordNERTagger
from nltk.internals import find_jars_within_path
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

schedulingMails = p.load( open("100Mails.dump", "rb") )
mapping = p.load( open("nameToMailIdMapping.dump", "rb") )
names = set()
f = open("names.txt")
for name in f:
	if len(name.strip())>=3:
		names.add(name.lower())

for mail in schedulingMails:
	participants = set()
	indx = m['body'].index("----") if "----" in m['body'] else -1
	s = MLStripper()
	m['body'] = m['body'].replace("\n"," ").replace("\r"," ").replace("\t"," ")[:indx]
	s.feed( m['body'] )
	for word in s.get_data().split():
		word = word.lower()
		if word in names and word not in participants and word in mapping:
			participants.add( mapping[word] )
	print "Participants: ",  "; ".join(participants)
	print m['body']