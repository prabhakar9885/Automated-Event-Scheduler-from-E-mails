from HTMLParser import HTMLParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
import pickle as p

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


categories = ['Yes', 'No']
mailThread = p.load(open("mailThreadenron_mail_20150507.dump", "rb") )

keys = mailThread.keys()[:100]
targets = [0]*100
yes = [1, 2, 8, 21, 29, 30, 37, 38, 55, 59, 61, 63, 68, 69, 74, 82, 92 ]
for i in yes:
	targets[i] = 1

allBodyMerged = []
for key in keys:
	mails = mailThread[key]
	temp = "";
	for mail in mails:
		if 'body' in mail and len(mail['body'])!=0:
			indx = mail['body'].index("----") if "----" in mail['body'] else -1
			s = MLStripper()
			s.feed( mail['body'].replace("\n","").replace("\r","").replace("\t","")[:indx] )
			temp += s.get_data() + ". "
	allBodyMerged += [ temp ]


# Tokenizing text 
# ===============
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(allBodyMerged)
X_train_counts.shape



# From occurrences to frequencies
# ===============================
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape


# Training an SVM classifier
clf = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, targets )


# Testing
# =======
docs_new = ['Meeting at 11:00 am', 'Meeting tomorrow at 12', 
			'meeting in the afternoon', 'meeting at 1:45 pm',
			'Lets meet at 2 am',
			'Lets meet in the afternoon',
			'invitation for a meeting at 3 pm',
			'God is love', 'OpenGL on the GPU is fast'
			]
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for i in xrange(len(predicted)):
	print docs_new[i], " ==> ", predicted[i]