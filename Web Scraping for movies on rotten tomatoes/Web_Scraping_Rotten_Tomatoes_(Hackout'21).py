# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 12:07:51 2021

@author: vyaso
"""

#setting up the environment
# load packages
import requests
from bs4 import BeautifulSoup

#definig the URL of site i.e., url of rotten tomatoes 
url = "https://editorial.rottentomatoes.com/guide/140-essential-action-movies-to-watch-now/2/"

# request to webpage
response = requests.get(url)
response.status_code

# HTML response from webpage
html = response.content

# HTML to Beautifulsoup conversion
soup = BeautifulSoup(html, 'html.parser')

# HTML to a file
with open('Rotten_tomatoes_HTML.html', 'wb') as file:
    file.write(soup.prettify('utf-8'))

# HTML to a BeatifulSoup object
soup = BeautifulSoup(html, 'lxml')

# HTML to a file
with open('Rotten_tomatoes_lxml.html', 'wb') as file:
    file.write(soup.prettify('utf-8'))

# Finding all div tags to extract the information
divs = soup.find_all("div", {"class": "col-sm-18 col-full-xs countdown-item-content"})
divs

#heading
divs[0].find("h2")

H = [div.find("h2") for div in divs]
H

# Inspecting the text inside the headings
[heading.text for heading in H]
H[0]

# Title
# Checking all heading links
[heading.find('a') for heading in H]

# Extracting the movie titles
moviename = [heading.find('a').string for heading in H]
moviename

# Year
# Filtering only the spans containing the year
[heading.find("span", class_ = 'start-year') for heading in H]

# Extracting the year string from webpage
year = [heading.find("span", class_ = 'start-year').string for heading in H]
year

year[0]

# Removing the brackets
year = [year.strip('()') for year in year]
year

# Converting all the strings to integers
year = [int(year) for year in year]
year

#Score
# Filtering only the spans containing the score
[heading.find("span", class_ = 'tMeterScore') for heading in H]

# Extracting the score string
score = [heading.find("span", class_ = 'tMeterScore').string for heading in H]
score

score = [s.strip('%') for s in score]
score

# Converting each score to an integer
score = [int(s) for s in score]
score

# Critics Consensus"""

divs
cc = [div.find("div", {"class": "info critics-consensus"}) for div in divs]
cc

# Inspecting the text inside these tags
[con.text for con in cc]

# inspect element
cc[0]

#  .contents to obtain a list of the tag
cc[0].contents

# The second element of that list is the text we want
cc[0].contents[1]

#remove extra white space
cc[0].contents[1].strip()

# Processing all texts
cc_text = [con.contents[1].strip() for con in cc]
cc_text

# Extracting all director divs
D = [div.find("div", class_ = 'director') for div in divs]
D

# Inspecting a div
D[0]

# The director's name can be found as the string of a link

# Obtaining director links
[director.find("a") for director in D]

# We can use if-else to deal with the None value

final_D = [None if director.find("a") is None 
                   else director.find("a").string 
                   for director in D]
final_D

# cast
castinfo = [div.find("div", class_ = 'cast') 
             for div in divs]
castinfo

castinfo[0]

# Initialize the list of all cast memners
cast = []

# previous operations inside a for loop
for c in castinfo:
    cast_links = c.find_all('a')
    cast_names = [link.string 
                  for link in cast_links]
    
    cast.append(", ".join(cast_names)) 

cast

# Nested list comprehension

cast = [", ".join([link.string 
                   for link in c.find_all("a")]) 
        for c in castinfo]
cast
#adjusted score
adjscores = [div.find("div", {"class": "info countdown-adjusted-score"}) 
              for div in divs]
adjscores

# Inspecting an element
adjscores[0]
adjscores[0].contents[1]  

# without '%' sign and extra space
adjscores_clean = [score.contents[1].strip('% ') for score in adjscores]
adjscores_clean

# strings to numbers
final_S = [float(score) for score in adjscores_clean] # Note that this time the scores are float, not int!
final_S

# Representing the data in structured form
import pandas as pd

# Creating a Data Frame
movies = pd.DataFrame()
movies 

# Populating the dataframe
movies["Movie Title"] = moviename
movies["Year"] = year
movies["Score"] = score
movies["Adjusted Score"] = final_S 
movies["Director"] = final_D
movies["Cast"] = cast
movies["Consensus"] = cc_text

movies

pd.set_option('display.max_colwidth', -1)
movies

# Write data to excel file
movies.to_excel("movies.xlsx", index = False, header = True)

# write data to CSV file
movies.to_csv("movies.csv", index = False, header = True)

