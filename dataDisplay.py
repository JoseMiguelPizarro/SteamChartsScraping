import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt

data = pd.read_csv('gamesData.csv')

genres = data[data.genres.str.len()>2]
genresData = genres.genres.tolist()


print(genresData[0])
allGenres = []
for gd in genresData:
    genres = gd.strip("[]")
    genres = genres.split(',')
    for i in range(len(genres)):
        g = genres[i].strip(" ''")
        genres[i] = g
    allGenres.extend(genres)


plt.hist(allGenres)
plt.show()

# for gd in genresData:
#     allGenres.append(gd)
        
