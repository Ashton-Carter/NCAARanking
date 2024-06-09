import itertools
import numpy as np
import pandas as pd
import numpy as np
from sklearn import preprocessing
import streamlit as st
from sklearn import svm
from sklearn.model_selection import train_test_split

#Training File
df = pd.read_csv('initdata.csv')

#Creating Win Index from Wins Over Bubble
df['windex'] = np.where(df.WAB > 7, 'True', 'False')

#Formating Training Data
df1 = df.loc[df['POSTSEASON'].str.contains('F4|S16|E8', na=False)]
df1.groupby(['windex'])['POSTSEASON'].value_counts(normalize=True)
df1['windex'].replace(to_replace=['False','True'], value=[0,1],inplace=True)
X = df1[['G', 'W', 'ADJOE', 'ADJDE', 'BARTHAG', 'EFG_O', 'EFG_D',
       'TOR', 'TORD', 'ORB', 'DRB', 'FTR', 'FTRD', '2P_O', '2P_D', '3P_O',
       '3P_D', 'ADJ_T', 'WAB', 'SEED', 'windex']]
y = df1['POSTSEASON'].values

#Standardizing Data
X= preprocessing.StandardScaler().fit(X).transform(X)

#Creating Train and Test Splits
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=4)

#Fitting data
finalSVM = svm.SVC(kernel = 'poly').fit(X_train, y_train)

#Creating Dictionary to Convert Output into Proper Format
rankings={
    '[\'E8\']':'Elite 8',
    '[\'F4\']':'Final 4',
    '[\'S16\']':'Sweet 16',
    '[\'R32\']':'Round of 32',
    '[\'R64\']':'Round of 64',
    '[\'R68\']':'Round of 68'
}


#File Uploader
st.title("NCAA Team Rankings Prediction")
st.write("Upload your CSV file with team data to get the predicted rankings.")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

#Checking if File is Uploaded
if uploaded_file is not None:

    #Formating Entry Data
    input_df = pd.read_csv(uploaded_file,on_bad_lines='skip')
    input_df['windex'] = np.where(input_df.WAB > 7, 'True', 'False')
    input_df['windex'].replace(to_replace=['False','True'], value=[0,1],inplace=True)
    names = input_df['TEAM']
    input_df.drop('TEAM', axis = 1, inplace=True)
    input_df= preprocessing.StandardScaler().fit(input_df).transform(input_df)

    #Creating Prediction and Formating with Dictionary
    final_rankings = finalSVM.predict(input_df)
    final_rankings = [rankings[str([pred])] for pred in final_rankings]
    results_df = pd.DataFrame({
        'Team' : names,
        'Ranking' : final_rankings
    })

    #Displaying Results
    st.title("NCAA Team Rankings")
    st.dataframe(results_df)

