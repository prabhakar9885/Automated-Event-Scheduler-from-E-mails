from HTMLParser import HTMLParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
import pickle as p
import numpy as np

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


categories = ['No','Yes','reschedule']
mailThread = p.load(open("mailThreadenron_mail_20150507.dump", "rb") )

print "Preparing the train data..."

keys = mailThread.keys()[:200]
targets = [0]*200
indexOfSchedulingMails = [1, 2, 8, 21, 29, 30, 37, 38, 55, 59, 61, 63, 68, 69, 74, 82, 92, 110 ,113 ,124 ,131 ,139, 161 ,171 ,194 ,195 ]
indexOfReSchedulingMails = [105, 147]
for i in indexOfSchedulingMails:
	targets[i] = 1
for i in indexOfReSchedulingMails:
	targets[i] = 2

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

# Augmenting the schdeuling mails
schdeulingMails = [ \
		'Lets meet at 2 am', \
		'Lets meet in the afternoon',\
		'scheduled a meeting for tomorrow',\
		'we will meet tomorrow',\
		'we are meeting tomorrow',\
		'we will meet today',\
		'we are meeting today',\
		'would like to meet and speak to you on the 15th of September',\
		'The monthly meeting will be on Monday, 12th December 2011',\
		'The meetings will be on Monday'
		]
for m in schdeulingMails:
	allBodyMerged += [m]
	targets += [1]


# Augmenting the Reschdeuling mails
reschdeulingMailsSamples = [\
		 'rescheduled the meeting for tomorrow'
		 'we have tentatively rescheduled the meeting for August 20.'
		 'we will postpone the meet',\
		 'we will postpone the meeting',\
		 'we will reschedule the meet',\
		 'we will reschedule the meeting',\
		 'We regret to inform you the August 8 meeting has been postponed.',\
		 'I\'m afraid I have to request to reschedule our meeting of June 15.',\
		 'This is to inform you that the board meeting that was scheduled to happen on the 12th of September has been postponed to the 15th of September due to some official reasons.  We are sorry for the inconvenience caused and would like to meet and speak with you on the 15th of September.',\
		 'I deeply regret that I will be unable to keep our appointment scheduled at 12: 00 noon on Wednesday, 5th March 2014. Due to some urgent circumstances in my office, I have to travel to Singapore, hence my inability to attend the aforementioned meeting.I will return on 12th March 2014 and as soon as I return, I will call your office to reschedule our meeting. Probably we can meet the next day after my return and will call your office in this regard. Once again, I apologise my inability to attend the meeting.',\
		 'Please consider my humble request for postponing my appointment date and be kind enough to permit me to join on a future date and oblige.',\
		 'This is to inform you that our meeting for Tuesday has to be postponed.',\
		 'This email is to let you all know that our scheduled meeting for this afternoon has been postponed.',
		 'could you please reschedule the meeting for tomorrow',
		 'The monthly meeting that was to take place on Monday, 12th December 2011 has been postponed because of an urgent visit that I will be making on the project site on that day during the morning hours.'
		]
for m in reschdeulingMailsSamples:
	allBodyMerged += [m]
	targets += [2]


targets = np.array(targets)

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
print "Training the SVM..."
clf = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, targets )


# Testing
print "Testing the model..."
print "Enter the mail content:"
while True:
	str = raw_input();
	docs_new = [str]
	X_new_counts = count_vect.transform(docs_new)
	X_new_tfidf = tfidf_transformer.transform(X_new_counts)

	predicted = clf.predict(X_new_tfidf)
	print categories[predicted]