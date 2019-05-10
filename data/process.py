#!/usr/bin/python
import math

#Example line of data:
#49,1,17,Att. 7.10,Atticus,Cicero,Mention,-1

#This function makes sure every day or month is two characters.
#E.g. '02' instead of '2'.
def c(m):
    return m if len(m) == 2 else '0' + m

#Create a dictionary mapping the year to an empty list for storing
#the cleaned data points
years = {str(k): list() for k in range(1947, 1956)}

#Open the csv fild and read in every line
with open('raw_data.csv', 'r') as f:
    lines = f.readlines()[1:]
    for l in lines:
        s = l.split(',')
        year = '19' + s[0] if s[0] else None
        month = c(s[1]) if s[1] else None
        day = c(s[2]) if s[2] else "01"
        letter = s[3]
        to = s[4]
        fro = s[5]
        sentiment = float(s[7]) if s[7] else None

        #Make sure all of the necessary fields are present. If they are, add the data point
        #to the year's corresponding list.
        if year != None and month != None and sentiment != None:
            years[year].append(('Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral', year + '-' + month + '-' + day, letter + ' (To: ' + to + '; From: ' + fro + ')'))

#Sort each list so that the graphs will show up Positive,
#then Neutral, then Negative
a = {'Positive': 0, 'Neutral': 1, 'Negative': 2}
for k in years:
    years[k] = sorted(years[k], key=lambda k: a[k[0]])

#Open and read the beginning and ending file templates
beg = ""
end = ""
with open('beg.html', 'r') as b:
    beg = b.read()
with open('end.html', 'r') as e:
    end = e.read()

#This function takes a datapoint and writes the javascript line that
#adds it to the graph
def createLine(p):
    return "[ '" + p[0] + "', null, '" + p[2] + "', new Date('" + p[1] + "'), new Date((new Date('" + p[1] + "')).getTime() + 1400*60000) ]"

#For each list of datapoints, create an HTML page with all of the data inserted
for k in years:
    if len(years[k]) == 0:
        continue
    with open(k[2:] + '.html', 'w') as f:
        f.write(beg)
        f.write("dataTable.addRows([\n")

        year = years[k]
        
        f.write(createLine(year[0]))
        for i in range(1,len(year)):
            p = year[i]
            f.write(',\n' + createLine(p))
        f.write("]);\n")
        f.write(end)


    
    
