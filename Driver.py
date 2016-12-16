"""
How to run?
===========
python Driver.py RunOnDump	# Run on enron mail data
python Driver.py 			# Run in interactive mode
"""

import Mail_Classifier
import Date_Classifier
import nltk, re
import pickle as p
from HTMLParser import HTMLParser
import traceback, sys, timeit
from glob import iglob
from nltk.tag import StanfordNERTagger
from nltk.internals import find_jars_within_path


start = timeit.default_timer()



mclf, mcount_vect, mtfidf_transformer = Mail_Classifier.buildMailClassifier()
dclf, dcount_vect, dtfidf_transformer = Date_Classifier.buildDateClassifier()


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
	for i in xrange(len(ner)):
		return ner


def getLocation( text ):
	locations = set()
	tps = doNER( s.get_data() )
	for tp in tps:
		if tp[1]=="LOCATION":
			locations.add( (tp[0]).lower() )
	return locations


def getDateTime( mailBody ):
	ngrams = [ nltk.bigrams( mailBody.split(" ") ), nltk.trigrams( mailBody.split(" ") ) ]
	res = []
	for ngram in ngrams:
		for item in ngram:
			docs_new = [" ".join(item)]
			X_new_counts = dcount_vect.transform(docs_new)
			X_new_tfidf = dtfidf_transformer.transform(X_new_counts)
			predicted = dclf.predict(X_new_tfidf)
			if predicted==1:
				res += [ ' '.join(item) ]
	return res;


def mergedText( dateTime ):
	bigrams = []
	trigrams = []
	for item in dateTime:
		if len(item.split(" "))==2:
			bigrams += [item]
		else:
			trigrams += [item]
	res = "";
	# print bigrams
	# print trigrams
	try:
		if len(trigrams) != 0:
			res += trigrams[0];
			for i in xrange( 1, len(trigrams) ):
				tmp = trigrams[i].split(" ")
				if res.split(" ")[-2] == tmp[0]:
					if res.split(" ")[-1] == tmp[1]:
						res += " " + tmp[2]
					else:
						res += " " + " ".join(tmp[1:])
				else:
					if res.split(" ")[-1] == tmp[0]:
						res += " " + " ".join(tmp[1:])
					else:
						res += " " + " ".join(tmp)
		else:
			res += bigrams[0];
			for i in xrange( 1, len(bigrams) ):
				tmp = bigrams[i].split(" ")
				if res.split(" ")[-1] == tmp[0]:
					res += " " + tmp[1]
				else:
					res += " " + " ".join(tmp)
	except:
		res = "DateTime can't be extracted."
	return res


if len(sys.argv)==2 and sys.argv[1]=="RunOnDump":
	i = 0
	schedulingMails = []
	reSchedulingMails = []
	print "Loading the dump..."
	mails = p.load( open("MailDataenron_mail_20150507.dump", "rb") )
	# mails = p.load( open("./100Mails.dump", "rb") )
	for mail in mails:
		
		if i==100:
			break
		try:
			indx = mail['body'].index("----") if "----" in mail['body'] else -1
			s = MLStripper()
			s.feed( mail['body'].replace("\n"," ").replace("\r"," ").replace("\t"," ")[:indx] )
			docs_new = [ s.get_data() ]
			X_new_counts = mcount_vect.transform(docs_new)
			X_new_tfidf = mtfidf_transformer.transform(X_new_counts)
			predicted = mclf.predict(X_new_tfidf)[0]
			if predicted==0:
				continue;
				print "Not a Scheduling mail"
			elif predicted==1:
				print "#"*20
				print "Actual date-time: ", mail['Date']
				i += 1
				print "Scheduling mail"
				dateTime = getDateTime( docs_new[0] )
				if dateTime == "DateTime can't be extracted.":
					print "Extracted date-time: ", dateTime
				else:
					print "Extracted date-time: ", mergedText( dateTime )
				location = getLocation( docs_new[0] )
				print "Location: ", "; ".join( location)
			elif predicted==2:
				print "#"*20
				print "Actual date-time: ", mail['Date']
				i += 1
				print "Re-Scheduling mail"
				dateTime = getDateTime( docs_new[0] )			
				if dateTime == "DateTime can't be extracted.":
					print "Extracted date-time: ", dateTime
				else:
					print "Extracted date-time: ", mergedText( dateTime )
				location = getLocation( docs_new[0] )
				print "Location: ", "; ".join( location )
			print "Participants: ", "; ".join( [mail["From"]] + mail["X-To"] )
			print "Subject:\n", mail['Subject'] if 'Subject' in mail else ""
			print "Body:\n", docs_new[0]
		except Exception, err:
			print "Exception: "
			print err
			print mail["Date"];
			print mail["Subject"];
			print traceback.print_exc()

		# p.dump( schedulingMails, open("schedulingMails.dump","wb+") )
		# p.dump( reSchedulingMails, open("reSchedulingMails.dump","wb+") )
else:
	while True:
		print "\nEnter the mail content:"
		str = raw_input();
		docs_new = [str]
		X_new_counts = mcount_vect.transform(docs_new)
		X_new_tfidf = mtfidf_transformer.transform(X_new_counts)
		predicted = mclf.predict(X_new_tfidf)
		if predicted==0:
			print "Not a Scheduling mail"
		elif predicted==1:
			print "Scheduling mail"
			dateTime = getDateTime(str)
			print dateTime
			print mergedText( dateTime )
		elif predicted==2:
			print "Re-Scheduling mail"
			dateTime = getDateTime(str)
			print dateTime
			print mergedText( dateTime )

print "Runtime: ", timeit.default_timer() - start