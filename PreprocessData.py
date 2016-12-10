"""
	Usage: python PreprocessData.py <Path to the parent directory of enron_mail_20150507>
"""


import os, sys, json, re
import datetime as dt
import pickle as p
from glob import iglob
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)



class MailData(object):
	"""docstring for MailData"""
	def __init__(self):
		self.mails = []
		self.regexLst = {}
		self.regexLst['dateTime'] = r"[A-Z][a-z][a-z], ([0-9]+) ([A-Z][a-z][a-z]) ([0-9]+) ([0-9]+):([0-9]+):([0-9]+)";
		self.regexLst['From'] = r"([A-Za-z0-9\.@]+)(, ([A-Za-z0-9\.@]+)+)";
		self.regexLst['To'] = r"([A-Za-z0-9\.@]+)(, ([A-Za-z0-9\.@]+)+)";


	def addFile(self, pathToMailFile):
		self.pathToMailFile = pathToMailFile
		self.parseFile();


	def convertTo( self, str, target ):
		month = {}
		month["Jan"], month["Feb"], month["Mar"], month["Apr"], month["May"], month["Jun"] = \
			range(1, 7)
		month["Jul"], month["Aug"], month["Sep"], month["Oct"], month["Nov"], month["Dec"] = \
			range(7, 13)

		if target=="datetime":
			m = re.match( self.regexLst['dateTime'], str.strip() )
			if m is None:
				return "Date format mismatch.\n"
			return dt.datetime( int(m.group(3)), month[m.group(2)], int(m.group(1)), int(m.group(4)), int(m.group(5)), int(m.group(6)) )
			

	def parseFile(self):
		d = {}
		prevKey = ""
		with open(self.pathToMailFile) as f:
			metaDataEnded = False
			for line in f:
				if metaDataEnded:
					if 'body' in d:
						d['body'] += line.replace("\n\r", " ")
					else:
						d['body'] =  line.replace("\n\r", " ")
					continue
				if re.match("^[A-Za-z\-]*: ", line):
					indxOfDelimit = line.index(":")
					key, Val = line[:indxOfDelimit].strip(), line[indxOfDelimit+1:].strip()
					prevKey = key
					if key=="Date":
						d[key] = self.convertTo( str=Val, target="datetime" )
					elif key=="X-FileName":
						d[key] = Val
						metaDataEnded = True
					else:
						d[key] = Val
				else:
					d[prevKey] += line.strip();
		self.mails += [ self.fixDataFormat(d) ];


	def printMailData(self):
		for m in self.mails:
			print "-*"*20
			for key in m:
				sys.stdout.write( key + " : " )
				print str(m[key])

	def fixDataFormat(self, mail):
		if 'To'in mail:
			mail['To'] = [ x.strip() for x in mail['To'].split(',') ]
		if 'Cc'in mail:
			mail['Cc'] = [ x.strip() for x in mail['Cc'].split(',') ]
		if 'Bcc'in mail:
			mail['Bcc'] = [ x.strip() for x in mail['Bcc'].split(',') ]

		if 'X-To'in mail:
			mail['X-To'] = [ x.strip() for x in mail['X-To'].split(',') ]
		if 'X-cc'in mail:
			mail['X-cc'] = [ x.strip() for x in mail['X-cc'].split(',') ]
		if 'X-bcc'in mail:
			mail['X-bcc'] = [ x.strip() for x in mail['X-bcc'].split(',') ]

		return mail

	def filterMail( self, mails ):
		keywords=["to meet","meeting with","meeting on","meet at","meeting at","scheduled a meet","schedule a meet","arrange a meet","tommorow at","attend a meet","attend the meet","meetings on","to a meet","meeting will be","i have a meet","tommorrow's meet","tomorrow at","this sunday","this monday","this tuesday","this wednesday","this thursday","this friday","this saturday","let's meet","request for a meeting","holding a business meet","book a meet","come by around","presence is requested","monday at","tuesday at","wednesday at","thursday at","friday at","saturday at","sunday at"];
		keyword_frequency={}
		for i in keywords:
			keyword_frequency[i]=0
		print "Number of mails to process ", len(mails)
		f=open("output1.txt","wb")
		filteredMails = []
		for i in xrange(len(mails)):
			if 'body' not in mails[i]:
				continue;
			mail = mails[i]['body'] 
			for j in keywords:
				if j in mail:
					f.write(j+" : ")
					f.write(mail)
					f.write("\n")
					filteredMails += [ mails[i] ];
					keyword_frequency[j]+=1
					break
		print "Number of filtered mails ", len(filteredMails)
		for i in keyword_frequency:
			if keyword_frequency[i] > 0:
				print i,keyword_frequency[i]
		f.close()
		return filteredMails

		def OrganizeMailsIntoThreads( filteredMails, mails ):
			filteredSubjects = set();
			for mail in filteredMails:
				subj = mail["Subject"].strip().lower()
				filteredSubjects.add(subj)
			mailsTemp = {};
			for mail in mails:
				if mail['Subject'] in filteredSubjects or \
					"re: "+mail['Subject'] in filteredSubjects:
					if mail['Subject'] in mailsTemp:
						mailsTemp[mail['Subject']] += [ mail ];
					else:
						mailsTemp[mail['Subject']] = [ mail ];
			mailsTemp.pop('')
			return mailsTemp






if __name__ == "__main__":

	mailData = MailData()

	if len(sys.argv) == 1:
		print "Parsing files..."

		for path in iglob( sys.argv[1] + '/enron_mail_20150507/*/*/*/*'):
			if os.path.isfile( path ):
				mailData.addFile( pathToMailFile = path )

		print "Pickling the mails..."
		print "====================="
		p.dump( mailData.mails, open("MailData.dump", "wb+") )
		print "Done."

		print "Filtering the Scheduling mails..."
		print "================================="
		filteredMails = filterMail(mails)
		print "Done."

		print "Organizing the mailing threads..."
		print "================================="
		mailThread = OrganizeMailsIntoThreads( filteredMails, mails )
		p.dump( mailThread, open("mailThread.dump", "wb+") )
		print "Subjects of Scheduling mails"
		print mailThread.keys()
		print "Done."
	else:
		filteredMails = p.load(open("MailData.dump", "rb") )
		mailThread = p.load(open("mailThread.dump", "rb") )
		print "Subjects of Scheduling mails"
		print mailThread.keys()


	print "Mail Threads with Sub: follow up"
	for m in mailThread['follow up']:
		print "#"*20 
		indx = m['body'].index("----") if "----" in m['body'] else -1
		s = MLStripper()
		tmp = s.feed( m['body'].replace("\n","").replace("\r","").replace("\t","")[:indx] )
		print s.get_data()