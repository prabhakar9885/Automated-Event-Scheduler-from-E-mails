import Mail_Classifier
import Date_Classifier
import nltk


mclf, mcount_vect, mtfidf_transformer = Mail_Classifier.buildMailClassifier()
dclf, dcount_vect, dtfidf_transformer = Date_Classifier.buildDateClassifier()


def getDateTime( mailBody ):
	ngrams = [ nltk.bigrams( mailBody.split() ), nltk.trigrams( mailBody.split() ) ]
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
		if len(item.split())==2:
			bigrams += [item]
		else:
			trigrams += [item]
	res = "";
	print bigrams
	print trigrams
	try:
		if len(trigrams) != 0:
			res += trigrams[0];
			for i in xrange( 1, len(trigrams) ):
				tmp = trigrams[i].split()
				if res.split()[-2] == tmp[0]:
					if res.split()[-1] == tmp[1]:
						res += " " + tmp[2]
					else:
						res += " " + " ".join(tmp[1:])
				else:
					if res.split()[-1] == tmp[0]:
						res += " " + " ".join(tmp[1:])
					else:
						res += " " + " ".join(tmp)
		else:
			for item in target:
				item = item.split()
				print item
				res += item[0] + " "
			for item in target[-1].split()[1:]:
				res += item + " "
	except:
		res = "DateTime can't be extracted."
	return res


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