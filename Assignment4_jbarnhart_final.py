# import required packages 
import numpy as np
import pandas as pd 

# read locally-stored file "2014 CY-YTD Passenger Raw Data 2-1.csv" and "A2010_14.txt" into Pandas DataFrame
# using read_csv()
passengers = pd.read_csv("Passengers.csv", na_values='\N', thousands=',')
accidents = pd.read_csv("A2010_14.txt", na_values='\N', sep ='\t') # tab delimited 

#------------------ PART 1---------------------#

# Determine the total number of passengers departing from BOS, MDW, FLL, MIA, and LAX airports. 
# Which of these airports had the largest numbers of passengers flying out it?

# group original dataframe by OriginApt and then retrieve the sum of total 
# passengers for the indicated airports

OrgApt = ('BOS','MDW','FLL','MIA','LAX') # list of interested airports
# I'm unfortunately not searching for KBOS, KMIA, or KLAX as I realized this too late 

Answer = pd.DataFrame(columns = ['Total'], index = ['BOS','MDW','FLL','MIA','LAX']) # dataframe whose index are the airports

# for all five airports, group by OriginApt, and get sum of Total for each group, save answer in dataframe 
for Apt in OrgApt:
    Answer.loc[Apt]= passengers.groupby('OriginApt').get_group(Apt).sum()['Total']
    
# Determine the total number of passengers arriving to each of these five airports. 
# Which of these airports had the largest numbers of passengers flying into it?

# The code below shows that there are no passengers arriving to there five airports
print (passengers.DestApt == 'BOS').sum()
print (passengers.DestApt == 'MDW').sum()
print (passengers.DestApt == 'FLL').sum()
print (passengers.DestApt == 'MIA').sum()
print (passengers.DestApt == 'LAx').sum()

# The code below only theoretically works if there were passengers arriving at the five airports
Answer2 = pd.DataFrame(columns = ['Total'], index = ['BOS','MDW','FLL','MIA','LAX'])

for Apt in OrgApt:
    Answer.loc[Apt]= passengers.groupby('DestApt').get_group(Apt).sum()['Total']

# For each of the five airports, break down the total number of departing passengers by carrier. 
# For each of the five airports, which carrier transported the most passengers out of the airport, i.e. 
# which was the most popular carrier flying out of that airportdf

Answer3 = pd.DataFrame(columns = ['Carrier','Total'], index = ['BOS','MDW','FLL','MIA','LAX']) # dataframe whose index are the airports

finder = 0 # helper variable that saves the maximum Total of all carriers for designated airport

for Apt in OrgApt: # create for loop that iterates through all five airports 
    df_wk = pd.DataFrame(passengers[passengers.OriginApt == Apt]) # select those rows whose OriginApt is equal to designated airport
    df_wk = df_wk.groupby('Carrier').sum()['Total'] # group by carrier and sum up Total passengers for each carrier
    Answer3.loc[Apt]['Total'] = max(df_wk) # save maximum Total passengers for each airport into dataframe
    finder = max(df_wk) # save the maximum Total passengers for each airport into variable finder 
    Answer3.loc[Apt]['Carrier'] = df_wk[df_wk == finder] # Find finder's carrier --> this does not work perfectly 

# The code above is almost perfect, except that the Carrier column does not just display the Carrier but other info too

# For each of the five airports, break down the total number of arriving passengers by carrier. 
# For each of the five airports, which carrier transported the most passengers into the airport, i.e. 
# which was the most popular carrier flying into that airport?

# The code below is the same as above only with OriginApt and DestApt switched in FOR loop 
# This code is only theoretical because, again, there are no DestApt with the designated airport codes 

Answer4 = pd.DataFrame(columns = ['Carrier','Total'], index = ['BOS','MDW','FLL','MIA','LAX']) # dataframe whose index are the airports

finder = 0 # helper variable that saves the maximum Total of all carriers for designated airport

for Apt in OrgApt:
    df_wk = pd.DataFrame(passengers[passengers.DestApt == Apt]) # select those rows whose DestApt is equal to designated airport
    df_wk = df_wk.groupby('Carrier').sum()['Total']
    Answer4.loc[Apt]['Total'] = max(df_wk)
    finder = max(df_wk)
    Answer4.loc[Apt]['Carrier'] = df_wk[df_wk == finder]
    
#------------------ PART 2---------------------#

# For each of the five airports, break down the total number of departing passengers by destination airport. 
# For each of the five airports, which was the most popular destination?

# The code below is the same as above only with DestApt and OriginApt switched in FOR loop 
# and now the grouping is done by DestApt

Answer5 = pd.DataFrame(columns = ['Destination','Total'], index = ['BOS','MDW','FLL','MIA','LAX']) # dataframe whose index are the airports

finder = 0 # helper variable that saves the maximum Total of all DestApt for designated airport

for Apt in OrgApt:
    df_wk = pd.DataFrame(passengers[passengers.OriginApt == Apt]) # select those rows whose OriginApt is equal to designated airport
    df_wk = df_wk.groupby('DestApt').sum()['Total'] # group by DestApt
    Answer5.loc[Apt]['Total'] = max(df_wk)
    finder = max(df_wk)
    Answer5.loc[Apt]['Destination'] = df_wk[df_wk == finder]
    
# For each of the five airports, break down the total number of arriving passengers by source airport. 
# For each of the five airports, which originating airport sent the most passengers into the airport?

# The code below is the same as above with OriginApt and DestApt switched out in the FOR loop 
# This code is only theoretical because, again, there are no DestApt with the designated airport codes 

Answer6 = pd.DataFrame(columns = ['Origin','Total'], index = ['BOS','MDW','FLL','MIA','LAX']) # dataframe whose index are the airports

finder = 0 # helper variable that saves the maximum Total of all DestApt for designated airport

for Apt in OrgApt:
    df_wk = pd.DataFrame(passengers[passengers.DestApt == Apt]) # select those rows whose DestApt is equal to designated airport
    df_wk = df_wk.groupby('OriginApt').sum()['Total'] # group by OriginApt
    Answer6.loc[Apt]['Total'] = max(df_wk)
    finder = max(df_wk)
    Answer6.loc[Apt]['Origin'] = df_wk[df_wk == finder]
    
# #------------------ PART 3---------------------#

# For each of these airports, determine the number of accidents or incidents that occurred 
# at them between 2010 and 2014 inclusive, according to the FAA. 

Answer7 = pd.DataFrame(columns = ['Total'], index = ['BOS','MDW','FLL','MIA','LAX']) # dataframe whose index are the airports

for Apt in OrgApt: # for each of the five airports
    Answer7.loc[Apt]= (accidents.c143.str.strip() == Apt).sum() # change value in column c143 to string, strip white spaces, and compare
    # to see if accident location matched airport code; sum up Total for each airport code 

# Determine the number of deaths that occurred in each event for each of these five airports.

df_1 = pd.DataFrame() # empty dataframe

# List of all accidents for all five airports
for Apt in OrgApt:    
    df_1 = df_1.append(accidents[accidents.c143.str.strip()==Apt]) # append each smaller dataframe found by airport to one another

# group by airport and then by event type
df_1 = df_1.groupby(['c143','c1'])

# sum up each number of fatalities by airport and event
Answer8 = df_1['c76'].sum()


#------------------ PART 4---------------------#

# Determine what the top ten (primary) causes of 2010-2014 incidents and accidents are for all events resulting in 
# deaths regardless of where they occurred. Provide descriptions (not codes) for the causes.

df_x = accidents.groupby('c78').c76.sum() # group accidents by primary cause and then by fatalities and sum-up

Answer9 = pd.DataFrame(df_x) # nake series into a dataframe

Answer9 = Answer9.sort('c76', ascending=False)[:11] # sort descending by c76 and get first 11 rows
# first row does not have a cause 

