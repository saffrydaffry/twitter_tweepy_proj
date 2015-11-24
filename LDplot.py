__author__ = 'Safyre'

import pymongo
import matplotlib.pyplot as plt
'''
create a plot of lexical diversities for part 2.2
'''

print " Open MongoDB connection to db_lexus2\n"
try:
    conn=pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
    print "Connection failed : %s" % e


lex_db = conn['db_lexus2']
lex_coll = lex_db.posts

records = lex_coll.find()

users_list = []
LD = []
for record in records:
    users_list.append(record['user'])
    LD.append(record['LD'])


index = range(0,len(LD))
print index
print LD

bar_width = [0.35]

plt.bar(index, LD, bar_width)
#plt.xticks(index + bar_width,('JmSports1', 'JayDB176', 'PetsNCritters', 'taylortodd784',
#                              'iamRichCole', 'jeikki09', 'allie_runyan', 'Mjmerritt23J', 'bunzonbunz',
#                              'iQ_Freedom', '3Q_Freedom','CREATEdigmanpub', 'Lindi_82072','demetrejaw48',
#                              'tH3_GmAn', 'NE2016_NE', 'AnsaarMohamed', 'GS_Warriors1', 'Carole_Delisl', 'Finished1' ))
plt.xticks(index+bar_width, users_list, rotation = 'vertical')
plt.xlabel('Users')
plt.ylabel('Lexical Diversity')
plt.title('Lexical Diversity of unique users in db_restT (500 tweets)')
plt.show()
print "Finished1"
#plt.plot(Cs, y)
#plt.xlabel('Lexical Diversities')
#plt.ylabel('Lexical Diversities')
#plt.title('Lexical Diversities per 30 top retweeted user')