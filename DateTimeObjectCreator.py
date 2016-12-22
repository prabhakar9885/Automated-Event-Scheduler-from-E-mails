import sys, re, nltk, dateparser, datetime
import Date_Classifier


clf, count_vect, tfidf_transformer = Date_Classifier.buildDateClassifier()

f = open( sys.argv[1] )

for line in f:
	if line.startswith("Actual date-time:"):
		skip = len("Actual date-time:")
		line = line[skip:].strip()
		gp = re.match( r"([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+):([0-9]+)", line )
		if gp is None:
			continue;
		yy, mont, day, hh, mm, ss = [int(i) if i is not None else -1 for i in gp.groups()]  
		mailDT = datetime.datetime(yy,mont,day,hh,mm,ss)

	if line.startswith("Extracted date-time:  DateTime can't be extracted."):
		continue
	if not line.startswith("Extracted date-time:"):
	 	continue;

	skip = len("Extracted date-time:")
	line = line[skip:].strip()
	line = line.lower().strip()
	line = line.replace("from"," ")
	
	print "Mail Date: ", mailDT
	print "Extracted Date-I:  ", line

	for i in xrange(8,0,-1):
		dt = None
		res = set()
		for ngram in nltk.ngrams( line.split(), i ):
			docs_new = [" ".join(ngram) ]
			X_new_counts = count_vect.transform(docs_new)
			X_new_tfidf = tfidf_transformer.transform(X_new_counts)
			predicted = clf.predict(X_new_tfidf)
			if predicted==1:
				dt = dateparser.parse( docs_new[0], settings={'RELATIVE_BASE': mailDT, 'PREFER_DATES_FROM': 'future'} )
				if dt is not None and dt.year>=mailDT.year:
					print docs_new[0]
					print "Extracted Date-II: ", docs_new
					print "Object: ", dt
					break;
		if dt is not None:
			break
	print "#" * 25