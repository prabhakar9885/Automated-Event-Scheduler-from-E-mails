import os, sys, json, re, nltk
import datetime as dt
import pickle as p
from glob import iglob
from nltk.tag import StanfordNERTagger
from nltk.internals import find_jars_within_path
from HTMLParser import HTMLParser


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

print doNER( "Thanks for your note.  Agreed that execution on IMI and II (construction, debt and equity closings) are the key for the Americas.  It looks like we will have slippage for Q2; I am expecting to see European numbers later this morning and will give you a call to discuss on Friday.  We can also discuss the gearbox issues for the US as to which I am a bit more optimistic than my earlier reports.  Adam   From: Stanley Horton/ENRON@enronXgate on 06/05/2001 03:00 PM CDT To: Adam Umanoff/EWC/Enron@ENRON cc: Tod A Lindholm/ENRON@enronXgate   Subject: Update.   It sounds like the due diligence with UBS is going fairly well with no real surprise.  The news is good on Indian Mesa I and II both on the deal with AEP and the financing.  The real target is completion of the project on time.  I am concerned about slippage again on Q2 due to the Greek project slippage and German installations being behind schedule.  I am looking forward to seeing the Q2 numbers very soon.  What is the issue on the L gearbox and what is the potential impact on 01 earnings given your statement that if we do not pass the test, it will present significant problems for 01 US sales.  Let's talk by phone this week if possible." )