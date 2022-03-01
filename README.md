# Group23Needle

## Files

writeup_group23.pdf - our full report.

noimages_group23.pdf - our full report without images.

DataAnalysis.ipynb - The data analysis part.

get_data.py - functions to get data from riot-games api and to
process this data to Objects that match our needs.

data_types.py - two classes (Objects types that we use as our data types)
that represents the data as we need.

similarity_tools.py - the functions we used to find similarities
between two different games (timelines).

test_bronze_teams.pkl - the bronze teams data (Team objects).

grand_teams.pkl - the grandmaster teams data (Team objects).

## About

Project for course 'Needle in a Data Haystack' (67978).

In Chess, when you learn the game it is very common to learn
from the greats. It is very common to take some state of the
game and study a pro move and take it as your own (Like: 
"Albin countergambit", "Amar opening", etc.). We decided 
take that intuition and see if it transferable. **We decided
to take the game "League of Legends"** and using algorithms 
from the course to see if a low-level player, 
using strategies from an experienced one, has a 
better chance of winning the game (SPOILER ALERT: 
We succeeded). We wanted to take this from a recommendation
point of view, we tried to build a recommendation system 
for a low-level beginner, taking into account his own
choices in the game.

## Data

We used the public riot-games api to get the data.
We used timelines of variety of games and we processed this data
to match our needs and the algorithms we used.

To see the data gathering process, please inspect the functions
in get_data.py file.

Note - to request new data, create a riot-games developer user and
generate new key (don't forget to paste the new key instead of the current key
at the top of the file)



You can download the data here (the processed data file are
'test_bronze_teams.pkl' and 'grand_teams.pkl'): https://drive.google.
com/drive/folders/13v0RDy0Am6guIRwnPi45idVX-z5sNZBG?
usp=sharing

## Algorithms

To find similarities between two different games (timelines) 
we used two similarity methods - Jaccard and Cosine similarities.

Check functions under 'similarity_tools.py' files for further
information of how we used the similarity algorithm.

## Data Analysis (The Juicy Conclusions!)

The data analysis and graphs are under DataAnalysis.ipynb, check it for further information!
