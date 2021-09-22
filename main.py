import tmdbsimple as tmdb
import requests

tmdb.API_KEY = 'YOUR-KEY'
tmdb.REQUESTS_SESSION = requests.Session()

import pandas as pd               # dataframe
import matplotlib.pyplot as plt   # plotting
import seaborn as sns             # plotting
import numpy as np                # cleaning data
from collections import Counter   # count words
from iso639 import languages      # convert iso639 code for language

###### ADDING INFORMATION FOR DATA ######

# open file csv
path_data= 'watched.csv'
data = pd.read_csv(path_data)

# prepare csv
data['Year'] = data['Year'].astype(int)
data = data[['Date', 'Name', 'Year']]

# function
search = tmdb.Search()
director = ""

def writeId(nameFilm, yearFilm):
  listFilm = search.movie(query='"{}"'.format(nameFilm), year = yearFilm)
  for film in search.results:
    try:
      title = film['title']
      title = title.lower()
      nameFilm = nameFilm.lower()
      if (nameFilm == title):
        id = str(film['id'])
        return id
    except:
     continue

def writeInfo(idFilm):
    try:
      global director
      # credit
      movie = tmdb.Movies(idFilm)
      response = movie.credits()
    
      # director
      for credit in movie.crew:  
        if credit["job"] == "Director":  
          director = credit['name']
        
      # actor
      crew = movie.crew
      actors = movie.cast
      actorList = []
      for act in actors:
        aktor = act['name']
        actorList.append(aktor)
        
      # info
      response = movie.info() 

      # genre
      genres = movie.genres
      genreList = []
      for gen in genres:
        genre = gen['name']
        genreList.append(genre)

      # lang
      lang = movie.original_language 

      # runtime
      runtime = movie.runtime
    
      info ={'Director':director, 'Cast':actorList, 'Genre':genreList, 'Lang':lang, 'Runtime':runtime}
      return info
    except:
      return ""

def plotHor(barname):
  for p in barname.patches:
    barname.annotate("%.0f" % p.get_width(), xy=(p.get_width(), p.get_y()+p.get_height()/2), 
                   ha = 'left', va = 'center', 
                   size=9,
                   xytext = (5, 0), 
                   textcoords = 'offset points')

def plotVer(barname):
  for p in barname.patches:
    # change .0f to .2f when plotting for the average
    barname.annotate(format(p.get_height(), '.0f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   size=9,
                   xytext = (0, 5), 
                   textcoords = 'offset points')

# data process
data['Id'] = data.apply(lambda row : writeId(row['Name'],row['Year']), axis = 1)  # fetch id
data['Info'] = data.apply(lambda row : writeInfo(row['Id']), axis = 1)            # fetch director, cast, genre, lang, runtime
data = data.dropna(axis=0, subset=['Id'])                                         # drop null value in id
dfNew = data.reset_index()                                                        # reset index
info = pd.json_normalize(dfNew['Info'])                                           # normalize column info into director, cast, genre, lang, runtime
noinfo = dfNew.drop(columns=['Info'])                                             # drop column info
df = noinfo.join(info, lsuffix='_caller', rsuffix='_other')                       # join column
df[['Cast', 'Genre']] = df[['Cast','Genre']].astype(str)                          # change type column cast and genre
df['Cast'] = df['Cast'].str.replace("\\[|\\]|\\'","")                             # remove some characters from column cast
df['Genre'] =  df['Genre'].str.replace("\\[|\\]|\\'","")                          # remove some characters from column genre
df['Lang'] = df['Lang'].str.replace("cn","zh")                                    # change mandarin code
df['Lang'] = df['Lang'].apply(lambda x: languages.get(alpha2=x).name)             # convert languange

###### OPTION ######

# if you want, you can check columns that might still have several empty values and change it manually per row
# you might found 
# convert empty values to NaN values
df = df.replace(r'^\s*$', np.NaN, regex=True)

# NaN values row
is_NaN = df.isnull()
row_has_NaN = is_NaN.any(axis=1)
rows_with_NaN = df[row_has_NaN]

# better save it for future use
df.to_csv('df.csv')

###### MERGE DATAFRAME AND RATINGS ######

# open file
path_rating= 'ratings.csv'
rating = pd.read_csv(path_rating)

# get only necessary column
rating['Year'] = rating['Year'].astype(int)
rating = rating[['Name', 'Year', 'Year]]

# merge
df = pd.merge(df, rating, how = "left").fillna(0)

###### VISUALIZATION ######

# total films, hours, directors
director = str(len(df['Director'].value_counts()))
hours = str((df['Runtime'].sum(axis = 0, skipna = True)) // 60)
film = str(len(df))

# plotting total films, hours, directors (arrange the coordinate manually)
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
fig = plt.figure(figsize=(10,5))
fig.patch.set_facecolor('#2c3440')
plt.scatter( 0 , 0.1 , s = 10000 )
plt.text(-0.07, 0.037, director, fontsize = 25, color = 'w')
plt.text(-0.17, -0.5, 'Directors', fontsize = 25, color = 'w')

plt.scatter( 0.5 , 0.1 , s = 10000 )
plt.text(0.407, 0.037, hours, fontsize = 25, color = 'w')
plt.text(0.38, -0.5, 'Hours', fontsize = 25, color = 'w')

plt.scatter( -0.5 , 0.1 , s = 10000 )
plt.text(-0.57, 0.037, film, fontsize = 25, color = 'w')
plt.text(-0.6, -0.5, 'Films', fontsize = 25, color = 'w')

plt.xlim( -0.85 , 0.85 )
plt.ylim( -0.95 , 0.95 )

plt.axis('off')
plt.show()

# Films by release date
year = df['Year'].value_counts()
plt.figure(figsize=(25,10))
baryear = sns.barplot(year.index, year.values, alpha=0.8)
plotVer(baryear)
plt.title('Films by Release Year',fontsize=16)
plt.show()

# average rating
ratings = df.groupby('Year')['Rating'].mean()
plt.figure(figsize=(25,10))
barrat = sns.barplot(ratings.index, ratings.values, alpha=0.8)
plotVer(barrat)
plt.title('Average Rating by Release Year',fontsize=16)
plt.show()
                 
# most watched directors
dir = df['Director'].value_counts()[:10]
plt.figure(figsize=(10,5))
bardir = sns.barplot(dir.values, dir.index, alpha=0.8)
plotHor(bardir)
plt.title('Most Watched Directors',fontsize=16 )
plt.show()

# most watched actors
actor = (", ".join(df["Cast"]).split(', '))
act = Counter(actor)
y = [count for tag, count in act.most_common(10)]
x = [tag for tag, count in act.most_common(10)]
plt.figure(figsize=(10,5))
baractor = sns.barplot(y, x, alpha=0.8)
plotHor(baractor)
plt.title('Most Watched Actors',fontsize=16 )
plt.show()

# most watched genres
genre = (",".join(df["Genre"]).split(','))
gr = Counter(genre)
y = [count for tag, count in gr.most_common(10)]
x = [tag for tag, count in gr.most_common(10)]
plt.figure(figsize=(10,5))
bargenre = sns.barplot(y, x, alpha=0.8)
plotHor(bargenre)
plt.title('Most Watched Genres',fontsize=16 )
plt.show()

# most watched languages
lang = df['Lang'].value_counts()[:10]
plt.figure(figsize=(10,5))
barlang = sns.barplot(lang.values, lang.index, alpha=0.8)
plotHor(barlang)
plt.title('Most Watched Languages',fontsize=16 )
plt.show()
