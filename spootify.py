import cred 
import requests
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from moodfinder import find_mood


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
    tempo, speechiness, loudness, instrumentalness, acousticness, valence, danceability, energy, liveness= 0, 0, 0, 0, 0, 0, 0, 0, 0
    #keeping track of individual song moods
    x=0
    song_moods= []
    for ids in track_ids:
        link= "https://api.spotify.com/v1/audio-features/"+ids
        song_feature= spotify.get(link)
        song_feature = song_feature.json()
        #print(song_feature)
        tempo+= song_feature["tempo"]
        speechiness+= song_feature["speechiness"]
        loudness+= song_feature["loudness"]
        instrumentalness+= song_feature["instrumentalness"]
        acousticness+= song_feature["acousticness"]
        valence+= song_feature["valence"]
        danceability+= song_feature["danceability"]
        energy+= song_feature["energy"]
        liveness+= song_feature["liveness"]
        song_moods.append([tracks_names[x], find_mood([song_feature["tempo"], song_feature["speechiness"],
                                                      song_feature["loudness"], song_feature["instrumentalness"],
                                                      song_feature["acousticness"], song_feature["valence"],
                                                      song_feature["danceability"], song_feature["energy"],
                                                      song_feature["liveness"]])])
        x+=1

    #finding averages    
    tempo= tempo/ len(track_ids)
    speechiness= speechiness/ len(track_ids)
    loudness= loudness/ len(track_ids)
    instrumentalness= instrumentalness/ len(track_ids)
    acousticness= acousticness/ len(track_ids)
    valence= valence/ len(track_ids)
    danceability= danceability/ len(track_ids)
    energy= energy/ len(track_ids)
    liveness= liveness/ len(track_ids)
    stats= [tempo, speechiness, loudness, instrumentalness, acousticness, valence, danceability, energy, liveness]
    print(stats)
    #print("valence: ", valence, "\ndanceability: ", danceability, "\nenergy: ", energy, "\nliveness: ", liveness)
    return stats, tracks_names, song_moods
    
    
def main():
    
    stats, tracks_names, song_moods= authorization() 
    print("\nBased on your 20 most recently-played songs, we found that you are most likely feeling",find_mood(stats),".")
    val= input("\nWould you like to see more information about your songs? <yes/no> ")
    if val=="yes":
        for i in song_moods:
            print(i[0], ': ', i[1])
    elif val=="no":
        print("thank you for trying out my web application!")
    else:
        print("only valid inputs are 'yes' or 'no'")

main()