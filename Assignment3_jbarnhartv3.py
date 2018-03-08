import pandas as pd
import json
import pickle as p

#------------------------------------- PART 1 -----------------------------------#

# ------- Step 1 ---------#

# load file 100506.json into a Python dictionary of dictionaries
with open('100506.json') as input_file:
    jsondat=json.load(input_file)

ratings_list = list()
new_dict = {}
categories = ['Author','Date','Ratings'] 

for review in jsondat['Reviews']:
    for key,value in review.iteritems(): 
        if str(key) in categories:
            new_dict[key] = value
    ratings_list.append(new_dict)
    new_dict = {}   

# len(ratings_list[0]['Ratings']

new_dictionary = {}

Ratings = ['Business service (e.g., internet access)','Check in / front desk','Cleanliness','Location','Overall','Rooms','Service','Sleep Quality','Value']

current_ratings=list()

# rating_list = ratings_list[4]['Ratings']

i=0

for review in ratings_list:
    if len(review['Ratings']) < 9:
        for key,value in review['Ratings'].iteritems(): 
            current_ratings.append(str(key))
        for ratings in Ratings:
            if ratings not in current_ratings:
                new_dictionary[ratings] = 'NaN'
        review['Ratings'].update(new_dictionary) 
        current_ratings=list()
        new_dictionary = {}

# df_reviews = pd.DataFrame(ratings_list)

# df_reviews.to_csv('review_check')

#------------- Step 2 ------------#

#df_reviews_test1 = pd.DataFrame.from_dict(ratings_list[0]['Ratings'], orient = 'index')
#df_reviews_test2 = pd.DataFrame.from_dict(ratings_list[1]['Ratings'], orient = 'index')

#df_reviews_test1 = df_reviews_test1.T # transpose the DataFrame 

#df_reviews_test2.T

# first create a DataFrame just f0r the 48 ratings

df_ratings_workhorse= pd.DataFrame() # workhorse dataframe
df_ratings= pd.DataFrame()

for rating in ratings_list:
    df_ratings_workhorse= pd.DataFrame.from_dict(rating['Ratings'], orient = 'index')
    df_ratings_workhorse = df_ratings_workhorse.T
    df_ratings = pd.concat([df_ratings,df_ratings_workhorse], axis=0) # concatenate vertically 
    df_ratings_workhorse= pd.DataFrame()
    
df_ratings = df_ratings.reset_index() # reset index to integers 0-47


# create a DataFrame just for the 48 Authors and Dates   

#df_Author_Date = pd.DataFrame()

#for review in ratings_list:
    #df_Author_workhorse = pd.DataFrame.from_dict(review['Author'], orient = 'index')
    #df_Date_workhorse = pd.DataFrame.from_dict(review['Date'], orient = 'index')
    #df_Author_workhorse = df_Author_workhorse.T
    #df_Date_workhorse = df_Date_workhorse.T
    #df_Author_Date = pd.concat([df_Author_workhorse,df_Date_workhorse], axis=0) # concatenate vertically 
    #df_Author_workhorse = pd.DataFrame()
    #df_Date_workhorse = pd.DataFrame()
    
#for review in ratings_list:
    #df_workhorse = pd.DataFrame.from_dict(review, orient = 'index')
    
# Concatenate both intermediary dataframes 

df_reviews = pd.DataFrame(ratings_list)

# drop the 'Ratings' column and horizontally concatenate with df_ratings DataFrame

del df_reviews['Ratings'] 


df_reviews = pd.concat([df_reviews,df_ratings], axis=1) # concatenate horizontally 

del df_reviews['index'] 

#------------- Step 3 ------------#

# change from unicode to float

df_reviews['Business service (e.g., internet access)'] = df_reviews['Business service (e.g., internet access)'].astype(float)  
df_reviews['Check in / front desk'] = df_reviews['Check in / front desk'].astype(float) 
df_reviews['Cleanliness'] = df_reviews['Cleanliness'].astype(float)    
df_reviews['Location'] = df_reviews['Location'].astype(float) 
df_reviews['Overall'] = df_reviews['Overall'].astype(float) 
df_reviews['Rooms'] = df_reviews['Rooms'].astype(float) 
df_reviews['Service'] = df_reviews['Service'].astype(float) 
df_reviews['Sleep Quality'] = df_reviews['Sleep Quality'].astype(float) 
df_reviews['Value'] = df_reviews['Value'].astype(float) 


#-------------Step 4 --------------#

# Create second DataFrame for comments

# Create a list of dictionaries with each Author, Content, and Date

comments_list = list()
new_dict = {}
categories = ['Author','Content','Date'] 

for review in jsondat['Reviews']:
    for key,value in review.iteritems(): 
        if str(key) in categories:
            new_dict[key] = value
    comments_list.append(new_dict)
    new_dict = {}  
    
# Create a dataframe of the comments_list

df_comments =pd.DataFrame(comments_list)

#-------------statistics for each ratings column --------------#


# If I had more time I would make this more elegant by creating a loop and save results into a DataFrame

# Business Service

df_reviews['Business service (e.g., internet access)'].mean()
df_reviews['Business service (e.g., internet access)'].min()
df_reviews['Business service (e.g., internet access)'].max()

# Check-in/Front Desk

df_reviews['Check in / front desk'].mean()
df_reviews['Check in / front desk'].min()
df_reviews['Check in / front desk'].max()

# Cleanliness

df_reviews['Cleanliness'].mean()
df_reviews['Cleanliness'].min()
df_reviews['Cleanliness'].max()

# Location

df_reviews['Location'].mean()
df_reviews['Location'].min()
df_reviews['Location'].max()

# Overall

df_reviews['Overall'].mean()
df_reviews['Overall'].min()
df_reviews['Overall'].max()

# Rooms

df_reviews['Rooms'].mean()
df_reviews['Rooms'].min()
df_reviews['Rooms'].max()

# Service

df_reviews['Service'].mean()
df_reviews['Service'].min()
df_reviews['Service'].max()

# Sleep Quality 

df_reviews['Sleep Quality'].mean()
df_reviews['Sleep Quality'].min()
df_reviews['Sleep Quality'].max()

# Value

df_reviews['Value'].mean()
df_reviews['Value'].min()
df_reviews['Value'].max()

# pickle dataftames

df_reviews.to_pickle("reviews.pkl")
df_comments.to_pickle("comments.pkl")