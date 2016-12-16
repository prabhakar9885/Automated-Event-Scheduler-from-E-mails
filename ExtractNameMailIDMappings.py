import pickle as p

# mails = p.load( open("MailDataenron_mail_20150507.dump", "rb") )

# print "Extracting mail Ids..."
# mailIds = set()
# for mail in mails:
# 	emails = [ mail['From'] ]
# 	if 'To' in mail and len(mail['To'])!=0:
# 		emails += mail['To']
# 	if 'Cc' in mail and len(mail['Cc'])!=0:
# 		emails += mail['Cc']
# 	if 'Bcc' in mail and len(mail['Bcc'])!=0:
# 		emails += mail['Bcc']
# 	for email in emails:
# 		mailIds.add( email.strip() )
# p.dump( mailIds, open("mailIds.dump", "wb+") )

mailIds = p.load( open("mailIds.dump", "rb") )

print "Creating the mapping: Name -> MailId..."
nameToMailIdMapping = {}
for email in mailIds:
	try:
		indx = email.index("@")
		name = email[:indx]
		for item in name.replace("-", " ").replace("_", " ").replace(".", " ").split():
			item = item.replace("'","").replace('"',"").lower()
			if item not in nameToMailIdMapping:
				nameToMailIdMapping[ item ] =  [email]
			else:
				nameToMailIdMapping[ item ] += [email]
	except:
		pass

print "Dumping the mapping... nameToMailIdMapping.dump"
p.dump( nameToMailIdMapping, open("nameToMailIdMapping.dump", "wb+") )
print "Done"