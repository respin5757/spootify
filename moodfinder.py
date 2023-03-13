import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score



# read in the data
moods=pd.read_csv('data_moods.csv')
moods= moods[['tempo', 'speechiness', 'loudness', 'instrumentalness', 'acousticness','valence', 'danceability','energy','liveness','mood']]
# split the data into 2 for training
train1, train2 = train_test_split(moods, test_size=0.33, random_state=40)
rf = RandomForestClassifier()
X_train = train1.drop('mood', axis=1)
y_train = train1['mood']
rf.fit(X_train, y_train)

# set feature_names attribute
rf.feature_names = X_train.columns.tolist()

X_test = train2.drop('mood', axis=1)
X_test.columns = ['tempo', 'speechiness', 'loudness', 'instrumentalness', 'acousticness','valence', 'danceability','energy','liveness']
X_test = train2.drop('mood', axis=1)
y_test = train2['mood']
y_pred = rf.predict(X_test.rename(columns={'Unnamed: 0': 'id', '0': 'tempo', '1': 'speechiness', '2': 'loudness', '3': 'instrumentalness', '4': 'acousticness', '5': 'valence', '6': 'danceability', '7': 'energy', '8': 'liveness'}))

# show accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

    
def find_mood(stats):
    prediction = rf.predict([stats])[0]
    return prediction
