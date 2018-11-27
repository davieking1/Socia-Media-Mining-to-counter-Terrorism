import pandas as pd
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap

tweets_file = open('twitter.txt','r')
tweets = []
for line in tweets_file.readlines():
    try:
        tweets.append(json.loads(line))
    except Exception:
        continue


def tweets_df(tweets):
    df = pd.DataFrame()
    df['text']=map(lambda tweet:tweet['text'], tweets)
    df['location'] = map(lambda tweet:tweet['user']['location'], tweets)
    df['country_code'] = map(lambda tweet:tweet['place']['country_code']
                                  if tweet['place'] != None else '', tweets)
    df['long']=map(lambda tweet:tweet['coordinates']['coordinates'][0]
                      if tweet['coordinates'] != None else 'NaN', tweets)
    df['latt']=map(lambda tweet:tweet['coordinates']['coordinates'][1]
                      if tweet['coordinates'] != None else 'NaN', tweets)
    return df
df = tweets_df(tweets)



m = Basemap(projection='merc', lat_0=50, lon_0=-100,
                resolution='l', area_thresh=500.0,
                llcrnrlon=-140, llcrnrlat=-55,
                urcrnrlon=160, urcrnrlat=70)
#draw elements on the map
m.drawcountries()
m.drawcoastlines(antialiased=False,
                 linewidth=0.005)
m.drawstates(color='b')
m.fillcontinents(lake_color='aqua')
m.drawmapboundary(color='aqua')
#add coordinates to the map
longs = list(df.loc[(df.long != 'NaN')].long)
latts = list(df.loc[(df.latt != 'NaN')].latt)
x, y = m(longs,latts)
m.plot(x, y, 'ro', markersize=6, alpha=0.5)
plt.show()

