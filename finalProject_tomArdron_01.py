#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 10:45:29 2021

@author: tom
"""
#import modules
from statistics import mean
from datetime import datetime 
import plotly.graph_objs as go
import plotly.offline as py
import csv 
with open("produce_csv.csv") as csvFile: #open csv file for reading
    reader = csv.reader(csvFile) #read the file
    data = [row for row in reader] #set list to variable 'data'

#DATA
modData = [] #initialize new list for data
for row in data: #traverse the rows
    newRow = list() #make an empty row to receive values
    for item in row: #traverse values in old row
        if "$" in item: #test for price string and convert
            newRow.append(float(item.replace("$","")))
        elif "/" in item: # test for date and converty
            newRow.append(datetime.strptime(item, '%m/%d/%Y'))
        else: # otherwise append item unchanged (not a date or price)
            newRow.append(item)
    modData.append(newRow) #append the newRow to modData   
#LOCATIONS
locations = modData.pop(0)[2:] #remove header and slice
records = list() #create empty list for data records
for row in modData: #traverse rows
    newRow = row[:2] #first two values are common in each location
    for loc, price in zip(locations,row[2:]): #traverse locaitons and prices
        records.append(newRow + [loc, price]) #add a new data record
 
#FUNCTION FOR OUTPUT AS COLUMNS
def columnPrint(x, enum = 2, wid = 20):
    s = ''
    for n, item in enumerate(x):
        if len(s) < 3*(wid+enum+2):
            if enum:
                s += f'<{n:{enum}}> '
            s += f'{item:<20}'
        else:
            print(s)
            s = ''
            if enum:
                s += f'<{n:{enum}}> '
            s += f'{item:<20}'
    if s:
        print(s)  
        
#RECORDS
print(f'{"="*30}\n{"Analysis of Commodity Data":^30}\n{"="*30}\n') #header
print("\nSELECT PRODUCTS BY NUMBER...\n")
uniRecords = sorted(list(set([x[0] for x in records]))) #list for each unique record
columnPrint(uniRecords) # formatted output
#USER RECORDS                             
resp = input("Enter product numbers separated by spaces: ").split() #prompt user response and split
newList = [uniRecords[int(i)] for i in resp] # list of unique records changed to type int
#PRINT RECORDS    
print(f'\nSelected products: {", ".join(newList)}')

#DATES
print("\nSELECT DATE RANGE BY NUMBER...\n") #title
uniDates = sorted(list(set([x[1] for x in records]))) #list of unique dates
uniqDates = [(datetime.strftime(row,"%Y-%m-%d")) for row in uniDates] #format dates added to selected dates
columnPrint(uniqDates)
print(f'\nEarliest available date is {uniDates[0].date()}') #first available date
print(f'Latest available date is {uniDates[-1].date()}') #last available date
#USER DATES
resp2 = input("Enter start/end date numbers separated by a space: ").split() # user response and split
newList2 = [uniDates[int(i)] for i in resp2]
#PRINT DATES
print(f'Dates from: {(newList2[0].date())} to {newList2[1].date()}\n')

#DATES FOR SELECT
start = newList2[0]
end = newList2[1]

#LOCATIONS2
print("SELECT LOCATIONS BY NUMBER...\n")
uniLocations = sorted(locations)
[print(f'<{j}> {i}') for j,i in enumerate(uniLocations)] # formatting output for user to select location
#USER LOCATIONS
resp3 = input("Enter the location numbers separated by spaces: ").split() #prompt user response and split
newList3 = [uniLocations[int(i)] for i in resp3]


print(f'\nSelected locations: {", ".join(newList3)}')

#RESULTS (location and commodity)
select = list(filter(lambda x: x[0]in newList and x[2] in newList3, records)) # selected data added to new lsit
#RESULTS (location commodity and DATES)
selected = [x for x in select if x[1] >= start and x[1]<= end] # ensuring data only between selected dates

#RESULTS COUNT
selectedFilesCount = 0
for row in selected:
    selectedFilesCount += 1
print(f'{selectedFilesCount} records have been selected.')
#print selected files
print("\nRECORDS SELECTED ...\n")
for row in selected:
    print(row)
#DICTIONARIES
records_dict = {}
for row in select:
    if row[0] in records_dict:
        records_dict[row[0]].append(row[2:])
    else:
        records_dict.update({row[0]:[row[2:]]})

records_final = {}#create dictionary  with location name
for item in records_dict: #for each product
    records_final[item] = {}
    for row in records_dict[item]:
        if row [0] in records_final[item]:
            records_final[item][row[0]].append(row[1])#append price data if location keys exists
        else:
            records_final[item].update({row[0]:[row[1]]})#update dictionary with location and price data

records_average = {}  #creating dictionary
for row in records_final:
    records_average[row] = {}
    for i in records_final[row]:#each location
        records_average[row][i] = round(mean(records_final[row][i]),2) #update dicitonary with average price
#TRACES
trace = []
for item in newList3:
    yValues = []
    for avg in records_average:
        yValues.append(records_average[avg][item])
    traces = go.Bar(x = [i for i in records_average], y = yValues, name = item)
    trace.append(traces)
#LAYOUT
chart = go.Layout(barmode = 'group', title = f'Commodity Prices from {start.date()} through {end.date()}', yaxis = dict(title = 'Average Price', tickformat = '$.2f'), xaxis = dict(title = 'Product'))
#BUILD CHART
figure = go.Figure(data = trace, layout = chart)
py.plot(figure, filename = "CommodityData-GroupedBarChart.html")



