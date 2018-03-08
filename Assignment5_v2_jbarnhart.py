from pymongo import MongoClient  # work with MongoDB 
import pandas as pd  # DataFrame object work
from datetime import datetime  # textdate manipulation
from pandas.io.json import json_normalize # to use json_normalize()
import collections as c # another Python container datatype that contains Counter() 

import sys; # system-specific parameters 
reload(sys);
sys.setdefaultencoding("utf8") # changes default ASCII to the UTF-8 encoding 
sys.getdefaultencoding()
# Python runtime uses it whenever it has to decode a string buffer to unicode 

print('First connect to the Northwestern VPNn')

# prompt for user's NetID and password
my_netid = raw_input('Enter your NetID: ')
my_password = raw_input('Enter your password: ') 

try:    
    client = MongoClient("129.105.208.225") # connect to the MongoDB database 
    client.enron.authenticate(my_netid, my_password,source='$external', mechanism='PLAIN') # authentication 
    print('\nConnected to MongoDB enron database\n')    
    success = True    
except:
    print('\nUnable to connect to the enron database') # unable to connect 

# if connection is successful, work with the database

#print('\nCollections in the enron database')
cols = client.enron.collection_names()

for col in cols:
    print(col)	
	
# work with documents in the messages collection 
workdocs = client.enron.messages

# inquire about the documents in messages collection
print('\nNumber of documents ', workdocs.count())
print('\nOne such document\n', workdocs.find_one())
one_dict = workdocs.find_one() # create dictionary
print('\nType of object workdocs ', type(one_dict)) 

# How many documents contain string "klay@enron.com"
# Remember to use escaped double quotes otherwise punctuation becomes delimiters 
print('How many documents contain the string klay@enron.com')
print(workdocs.find({'$text':{'$search':"\"klay@enron.com\""}}).count())

# Find documents containing all aliases
# The aliases contain Rosalee Flemming, the administrative assistant and proxy to Kenneth Lay 
Aliases = ["\"kenneth.lay@enron.com\"","\"ken_lay@enron.com\"","\"ken.lay@enron.com\"","\"kenneth_lay@enron.net\"","\"klay@enron.com\"","\"rosalee.flemming@enron.com\"", "Kenneth Lay", "Ken Lay", "Lay, Ken","Lay, Kenneth", "Rosalee Flemming", "Flemming, Rosalee"]

for alias in Aliases:
    sdocs = list(workdocs.find({'$text':{'$search': alias}}))
    
# Number of documents retrieved by text search
print('\nNumber of items in sdocs ', len(sdocs))  

# create a Pandas DataFrame
email_df = json_normalize(sdocs) 

# delete the _id column
del email_df['_id']

# remove "headers." from the column names
email_df.rename(columns={'headers.Date':'Date','headers.From':'From','headers.Message-ID':'Message-ID','headers.Subject':'Subject','headers.To':'To',
'headers.X-From':'X-From','headers.X-To':'X-To',
'headers.X-bcc':'X-bcc','headers.X-cc':'X-cc'},inplace=True)

# set missing data fields
email_df.fillna("", inplace=True)

# user-defined function to create simple date object (no time)
def convert_date_string (date_string):
    try:    
        return(datetime.strptime(str(date_string)[:16] # it returms a datetime.datetime object 
            lstrip().rstrip(), '%a, %d %b %Y'))
    except:
        return(None)
        
# apply function to convert string Date to date object
email_df['Date'] = email_df['Date'].apply(lambda d: convert_date_string(d))
    
# date of Enron bankruptcy
BANKRUPTCY = datetime.strptime(str('Sun, 2 Dec 2001'), '%a, %d %b %Y')   

#-------------Question 1------------#

#----How many messages are "To" Ken Lay?----#

Aliases2 = ["kenneth.lay@enron.com","ken_lay@enron.com","ken.lay@enron.com","kenneth_lay@enron.net","klay@enron.com","rosalee.flemming@enron.com", "Kenneth Lay", "Ken Lay", "Lay, Ken","Lay, Kenneth", "Rosalee Flemming", "Flemming, Rosalee"]

# Checking "To" column with all aliases
df_email_To = email_df.loc[email_df["To"].isin(Aliases2)]
len(df_email_To)
### 259

# Checking "X-To" column with all aliases
df_email_XTo = email_df.loc[email_df["X-To"].isin(Aliases2)]
len(df_email_XTo)
### 123

# Concatenating both dataframes and deduplicating rows to get final count
df_email_To_final = pd.concat([df_email_To, df_email_XTo], axis =0).drop_duplicates()
len(df_email_To_final)
### 259
       
#------ How many messages are "From" Ken Lay?-------#

# Checking "From" column with all aliases
df_email_From = email_df.loc[email_df["From"].isin(Aliases2)]
len(df_email_From)
### 18

# Checking "X-From" column with all aliases
df_email_XFrom = email_df.loc[email_df["X-From"].isin(Aliases2)]
len(df_email_XFrom)
### 4

# Concatenating both dataframes and deduplicating rows to get final count
df_email_From_final = pd.concat([df_email_From, df_email_XFrom], axis =0).drop_duplicates()
len(df_email_From_final)
### 18

#------- How many messages was Ken Lay cc'd on? ----------# 

# Checking "X-cc" column with all aliases
df_email_CC = email_df.loc[email_df["X-cc"].isin(Aliases2)]
len(df_email_CC)
### 0

#-------- How many messages was Ken Lay bcc'd on? -----------#

# Checking "X-bcc" column with all aliases
df_email_BCC = email_df.loc[email_df["X-bcc"].isin(Aliases2)]
len(df_email_BCC)
### 0


#-------------Question 2------------#   

# Who did Lay send the most emails to? 

# Reuse the df_email_From DataFrame

# email with "From" in Aliases2, grouped by "To", count for each group, maximum 

master_list = list()

for email in df_email_From.To:
        workhorse = str(email).split(",") # split string into a string array 
        for item in workhorse: # loop through each item in array 
            item = item.strip() # remove all whitespace at start and end of string
            item = item.translate(None, ' \r\n\t') # remove ' \r\n\t' from string 
            if item not in master_list: # if email is already not in master list
                print item
                master_list.append(item) # add it to list 
                workhorse = ""
# which item in the list is most frequent?

counter = c.Counter(master_list)

print counter.values()
# Everyone was emailed just once

# Who did he receive the most from?

# Reuse the df_email_To DataFrame

master_list = list()

for email in df_email_To.From:
        workhorse = str(email).split(",") # split string into a string array 
        for item in workhorse: # loop through each item in array 
            item = item.strip() # remove all whitespace at start and end of string
            item = item.translate(None, ' \r\n\t') # remove ' \r\n\t' from string 
            if item not in master_list: # if email is already not in master list
                print item
                master_list.append(item) # add it to list 
                workhorse = ""   
                
# which item in the list is most frequent?
counter = c.Counter(master_list)

print counter.values()
# Ken received emails from everyone just once

#-------------Question 3------------#   

# Did the volume of emails sent by Lay increase or decrease after bankruptcy was declared?

# Reuse the df_email_From DataFrame 

# Check the current type for "Date" column
for item in df_email_From.Date:
    print type(item)
    
# Check minimum possible date 
df_email_From.Date.min()
# July 10, 2000

# Check maximum possible date
df_email_From.Date.max()
# December 26, 2001
    
# create new dataframe with all rows whose Date is before the bankruptcy date     
df_before = df_email_From[df_email_From.Date < BANKRUPTCY] 

len(df_before)
# 17 emails

# create new dataframe with all rows whose Date is after the bankruptcy date   
df_after = df_email_From[df_email_From.Date > BANKRUPTCY]
len(df_after)
# 1 email

#------------Question 4------------# 

# How many of these email messages mention Arthur Andersen, Enron's accounting firm?

# Reuse the original DataFrame email_df

email_df.body.str.contains('Arthur Anderson').sum() # works only for a series 
# 2

email_df.body.str.contains("Arthur").sum() # but these may relate to a human named Arthur, thus further investigation needed 
# 49 

# check to see if changing the body of email to all lower letters will change comparison outcome
counter = 0
for email in email_df.body:
        if "arthur anderson" in str(email).lower():
            counter = counter +1
# still 2 emails

# check to see if changing the body of email to all lower letters will change comparison outcome 
counter = 0
for email in email_df.body:
        if "arthur" in str(email).lower():
            counter = counter +1                    
# yes it made a difference, 63 emails 
