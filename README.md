# Spotify Mood Analyzer

The Spotify Mood Analyzer is a Python program that analyzes your 20 most recently played songs on Spotify to determine your current mood. It uses the Spotify API to fetch data about the songs you've listened to and the RandomForestClassifier from the sklearn library to make predictions based on the audio features of these songs. The program also allows you to see the mood associated with each individual song.

## Installation

To run this program, you'll need to have Python installed on your computer along with the following libraries:

- requests
- requests_oauthlib
- pandas
- numpy
- matplotlib
- sklearn

You can install these packages using pip by running the following command:
```bash
pip install requests requests_oauthlib pandas numpy matplotlib sklearn
```
Additionally, you will need to download and save the data_moods.csv file in the same directory as the program.

## Usage
First, you'll need to create a file named cred.py in the same directory as the program. In this file, add the following lines, replacing the placeholders with your Spotify app credentials and the appropriate redirect URL:

```bash
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URL = "your_redirect_url"
```
Run the program using Python:
```bash
python spotify_mood_analyzer.py
```

Follow the instructions in the terminal. You'll be prompted to authorize the program to access your Spotify account. After authorization, the program will analyze your recently played songs and display your current mood.

If you want to see more information about your songs, type "yes" when prompted.

## How it works
The program uses the Spotify API to fetch information about your 20 most recently played songs. It then calculates the average values for various audio features such as tempo, speechiness, loudness, instrumentalness, acousticness, valence, danceability, energy, and liveness. Using these features, the RandomForestClassifier predicts your mood based on a pre-trained dataset (data_moods.csv).

The classifier has an accuracy of around 82%, which means that it can accurately predict the mood associated with a song in 82% of cases.
