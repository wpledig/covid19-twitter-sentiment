import json
from collections import defaultdict
import pandas as pd
import datetime

"""
Calculates the number of tweets per day and stores in a CSV
"""

daily_counts = defaultdict(int)          #create a dictionary to store the value of the number of tweets that are made each day

dataset = "../data-collection/data/complete_en_US"    #define a variable for the dataset 
num_counted = 0                         #initialize the number of daily tweets counted to 0

with open(dataset) as inputfile:       
    lines = inputfile.readlines()       #create a list with each line in our dataset as an entry in that list
    print("filesize: ", len(lines))    
    for line in lines:                  #iterate through the list containing each line in our dataset
        jline = json.loads(line)        #converts the string of the Java Script Object Notation as its parameters into a dictionary containing that information
        # print(json.dumps(jline, indent=4))

        # print(jline["created_at"])
        cur_date = datetime.datetime.strptime(jline["created_at"], '%a %b %d %H:%M:%S %z %Y') #check the current date for each line in our dataset
        daily_counts[cur_date.date()] += 1    #increase the value of the number of tweets corresponding to the current date by 1 in the dictionary 

        num_counted += 1                    #increase the number of the daily tweet count value by 1 
        if num_counted % 1000 == 0:
            print("Counted ", num_counted)  #if the number of daily tweets counted modulo 1000 is equivalent to 0 then print the daily value as "Counted"

df = pd.DataFrame.from_dict(daily_counts, orient='index').reset_index()
df.columns = ['day', 'count']
print(df)                                   #print the day and the corresponsing count to that day based on the values stored in the dictionary, daily_counts
df.to_csv("days_by_counts.csv", index=False)

