

import cred 
import requests
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import json
import numpy as np
import matplotlib.pyplot as plt


#app credentials
client_id = cred.CLIENT_ID
client_secret = cred.CLIENT_SECRET
redirect_uri = cred.REDIRECT_URL

def authorization():
    authorization_base_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"
    scope = ["user-read-email","playlist-read-collaborative", "user-read-recently-played" ]


    spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

    # Redirect user to Spotify for authorization
    authorization_url, state = spotify.authorization_url(authorization_base_url)

    print('Please go here and authorize: ', authorization_url)

    # Get the authorization verifier code from the callback url
    redirect_response = input('\n\nPaste the full redirect URL here: ')

    auth = HTTPBasicAuth(client_id, client_secret)

    # Fetch the access token
    token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)

    #fetch recently played
    x = spotify.get('https://api.spotify.com/v1/me/player/recently-played')

    
    #getting ids from recently played
    x = x.json()
    tracks =x['items']
    track_ids= []
    tracks_names= []
    for item in tracks:
        track_ids.append(item['track']['id'])
        tracks_names.append(item['track']['name'])


    #getting features from track id and adding
    valence, danceability, energy, liveness= 0, 0, 0, 0
    for ids in track_ids:
        link= "https://api.spotify.com/v1/audio-features/"+ids
        song_feature= spotify.get(link)
        song_feature = song_feature.json()
        valence+= song_feature["valence"]
        danceability+= song_feature["danceability"]
        energy+= song_feature["energy"]
        liveness+= song_feature["liveness"]

    #finding averages    
    valence= valence/ len(track_ids)
    danceability= danceability/ len(track_ids)
    energy= energy/ len(track_ids)
    liveness= liveness/ len(track_ids)
    stats= [valence, danceability, energy, liveness]
    
    return stats, tracks_names
    #print("valence: ", valence, "\ndanceability: ", danceability, "\nenergy: ", energy, "\nliveness: ", liveness)   

def mood_finder(stats):
    if (stats[0]>0.5) & (stats[2]>0.5):
        return "happy"
    elif (stats[0]<0.334) & (stats[2]>0.333) & (stats[1]>0.333) & (stats[3]<0.666):
        return "angsty"
    else:
        return "sad"
    
def plot_stats(stats):     
    #plotting using matplotlib
    categories= ['Valence', 'Danceability','Energy','Liveness']
    categories = [*categories, categories[0]]
    stats = [*stats, stats[0]]
    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(stats))
    plt.figure(figsize=(8, 8))
    plt.subplot(polar=True)
    plt.plot(label_loc, stats)
    plt.title('Recently-Played Song Features', size=15)
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
    plt.legend()
    plt.show()

def main():
    
    stats, tracks_names= authorization() 
    print("\nBased on your 20 most recently-played songs, we found that you are most likely feeling",mood_finder(stats),".")
    val= input("\nWould you like to see your song features' averages? <yes/no> ")
    if val=="yes":
        #print("songs: ")
        #for i in tracks_names:
        #    print(i, end= ', ')
        plot_stats(stats)
    elif val=="no":
        print("thank you for trying out my web application!")
    else:
        print("only valid inputs are 'yes' or 'no'")


main()
