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


def doNER( text ):
	st = StanfordNERTagger('english.muc.7class.caseless.distsim.crf.ser.gz')
	stanford_dir = st._stanford_jar[0].rpartition('/')[0]
	stanford_jars = find_jars_within_path(stanford_dir)
	st._stanford_jar = ':'.join(stanford_jars)
	tokenizer='[, \n\r:;\'\"-<>(){}\[\]/!=]'
	words=re.split(tokenizer,text)
	ner=st.tag(words)
	return ner

print "Loading the dump..."
mails = p.load( open("MailDataenron_mail_20150507.dump", "rb") )

print "Extracting the entities"
f = open("names.txt","w+")

for m in mails:
	try:
		indx = m['body'].index("----") if "----" in m['body'] else -1
		s = MLStripper()
		s.feed( m['body'].replace("\n"," ").replace("\r"," ").replace("\t"," ")[:indx] )
		ners = doNER( s.get_data() )
		for ner in ners:
			if ner[1] == "PERSON":
				print ner[0]
	except Exception, e:
		print e
		pass

f.close()
print "Done"