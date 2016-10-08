"""
	Usage: python PreprocessData.py <Path to the parent directory of enron_mail_20150507>
"""


import os, sys, json, re
import datetime as dt
import pickle as p
from glob import iglob


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


	def buildGraph(self):
		pass


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



if __name__ == "__main__":

	mailData = MailData()

	print "Parsing files..."

	for path in iglob( sys.argv[1] + '/enron_mail_20150507/*/*/*/*'):
		if os.path.isfile( path ):
			mailData.addFile( pathToMailFile = path )

	# print mailData.printMailData()

	print "Pickling the mails..."
	p.dump( mailData.mails, open("MailData.dump", "wb+") )

	print "Done."
