from HTMLParser import HTMLParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
import pickle as p
import numpy as np
import nltk

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

categories = ['No','Yes']



def buildDateClassifier():

	mailThread = p.load( open("mailThreadenron_mail_20150507.dump", "rb") )

	print "Preparing the train data..."
	train = []
	label = []
	dateTimeTrain = open("./DateAndTime.txt", "r" ).readlines()
	for item in dateTimeTrain:
		try:
			key, val = item.split("=")
			train += [key.strip()]
			label += [int(val.strip())]
		except:
			print len(label)

	label = np.array(label)

	# Tokenizing text 
	# ===============
	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(train)
	X_train_counts.shape

	# From occurrences to frequencies
	# ===============================
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	X_train_tfidf.shape

	# Training an SVM classifier
	print "Training the SVM..."
	clf = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, label )

	return clf, count_vect, tfidf_transformer



if __name__ == '__main__':

	clf, count_vect, tfidf_transformer = buildDateClassifier()

	# Testing
	print "Testing the model..."
	while True:
		print "Enter the Date and Time:"
		str = raw_input();
		docs_new = [str]
		X_new_counts = count_vect.transform(docs_new)
		X_new_tfidf = tfidf_transformer.transform(X_new_counts)

		predicted = clf.predict(X_new_tfidf)
		print predicted[0]
		for i in xrange(1,6):
			for ngram in nltk.ngrams( str.split(), i ):
				docs_new = [" ".join(ngram) ]
				X_new_counts = count_vect.transform(docs_new)
				X_new_tfidf = tfidf_transformer.transform(X_new_counts)
				predicted = clf.predict(X_new_tfidf)
				print docs_new, predicted