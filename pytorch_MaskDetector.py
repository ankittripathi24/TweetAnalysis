import streamlit as st
import pandas as pd
import tweepy
import pickle
import re
import string
import joblib

import matplotlib.pyplot as plt
from ntscraper import Nitter

# Set the title of the web app
st.title('Sentiment Analysis Web App')

# test Tweet: https://twitter.com/SingaporeAir
# test tweet: flyPAL

#  side bar heading
st.sidebar.title('TWEET SENTIMENT ANALYSIS')

# Load the CSV data
@st.cache  # This makes the function run only once and stores the result in cache for performance
def load_data():
    data = pd.read_csv('data.csv')
    return data

import snscrape.modules.twitter as sntwitter

def get_tweets_Nitter(username):
    # Create an empty list to store the tweets
    tweets = []
    scrapper = Nitter(log_level=1, skip_instance_check=False)

    tweets = scrapper.get_tweets(username, mode="user", number=5)
    print(tweets)
    tweets = []
    # Use snscrape to get the latest 5 tweets from the specified username
    for  tweet in scrapper.get_tweets(username, mode="user", number=5):
        print(tweet)
        tweets.append(tweet)

    
    # # Use snscrape to get the latest 5 tweets from the specified username
    # for i, tweet in enumerate(sntwitter.TwitterUserScraper(username).get_items()):
    #     if i > 4:
    #         break
    #     tweets.append(tweet.content)

    return tweets

# Function to get tweets from a user using Tweepy
def get_tweets_tweepy(username):
    # You need to replace these with your own Twitter credentials
    consumer_key = "fHqIiab3J4rAJKzVubhpGK8AU"
    consumer_secret = "ODxRPijjNOE3m1vqzgvic6nkZ7qLybvLANe3AedAJSbSSzM2Gg"
    access_token = "1704834563942547456-j8Dah9rK0ZYRZtYlNtewDSAdcDQJXG"
    access_token_secret = "M3VnaGaQTqk9qeIxLhGJIiJY8dTEVlkLHw4pkVEl6S5eV"
    consumer_key = "uize6mhxDylCBBtTNODIO2IQC"
    consumer_secret = "H1XyjFLjEi71leFTxxWeUIhaXWKP27ZeRDrXD2jeyDzM4BJdUH"
 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = api.get_user(screen_name=username, count=5)

    return tweets

def predict_tweets(tweets):
    for tweet in tweets:
        # Preprocess the tweet
        preprocessed_tweet = preProcessTweet(tweet.full_text)
        
        # Convert the preprocessed tweet into TF-IDF features
        tfidf_features = tfidf_vectorizer.transform([preprocessed_tweet])
        
        # Make a prediction for the tweet
        prediction = loaded_model.predict(tfidf_features)
        
        # Add the original tweet, preprocessed tweet, and predicted sentiment to the results list
        predictions.append({'Original Tweet': tweet.full_text, 'Predicted Sentiment': prediction[0]})
    
    # Convert the results list to a DataFrame
    predictions_df = pd.DataFrame(predictions)
    
    # Convert the DataFrame to an HTML table with colored rows
    table_html = predictions_df.style.apply(lambda row: ['background: lightgreen' if row['Predicted Sentiment'] == 'positive' else 'background: lightcoral' for _ in row], axis=1).render()
    
    # Display the HTML table
    st.markdown(table_html, unsafe_allow_html=True)

# Function to preprocess the tweet
def preProcessTweet(tweet):
    # Convert the tweet to lowercase
    tweet = tweet.lower()
    # Remove URLs
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    # Remove user @ references and '#' from tweet
    spec_chars = ["!",'"',"#","%","&","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–"]
    for sc in spec_chars:
        tweet = tweet.replace(sc, '')
    # Remove punctuations
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    
    return tweet
    

# Load the vectorizer and the model

with open('final_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

model = joblib.load("model.pkl")
tfidf_vectorizer = joblib.load("vectorizer.pkl")

# Create a checkbox for the 'I am only interested in seeing stats' option
if st.sidebar.checkbox('I am only interested in seeing stats'):
    option = 'DISPLAY STATISTICS'
else:
    # Create a sidebar with options
    option = st.sidebar.radio(
        'How would you like to enter the tweet?',
        ('ENTER TWEET', 'UPLOAD TWEET CSV', 'GET TWEETS FROM SCRAPPER')
    )


if option == 'ENTER TWEET':
    # data = load_data()
    # st.write(data)
    
    tweet_text = st.text_input('Enter a tweet for sentiment analysis')
    if st.button('Predict'):
        # Preprocess the input text (clean, tokenize, etc.)
        preprocessed_tweet = preProcessTweet(tweet_text)
        
        # Convert the preprocessed tweet text into TF-IDF features
        tfidf_features = tfidf_vectorizer.transform([preprocessed_tweet])
        
        # Make predictions using the loaded model
        prediction = loaded_model.predict(tfidf_features)
        
        # Display the predicted sentiment
        st.write(f'Predicted Sentiment: {prediction}')
elif option == 'UPLOAD TWEET CSV':
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        if 'Tweets' in data.columns:
            st.write(data)
            if st.button('Predict all'):
                results = []
                predictions = []
                for tweet in data['Tweets']:
                    # Check if the tweet is a string
                    if isinstance(tweet, str):
                        # # Print the tweet before preprocessing it
                        # st.write(f'Original Tweet: {tweet}')
                        
                        # Preprocess the tweet
                        preprocessed_tweet = preProcessTweet(tweet)
                        
                        # Convert the preprocessed tweet into TF-IDF features
                        tfidf_features = tfidf_vectorizer.transform([preprocessed_tweet])
                        
                        # Make a prediction for the tweet
                        prediction = loaded_model.predict(tfidf_features)
                        
                        # Add the prediction to the list of predictions
                        predictions.append(prediction)
                        
                        # Add the original tweet, preprocessed tweet, and predicted sentiment to the results DataFrame
                        results.append({'Original Tweet': tweet, 'Preprocessed Tweet': preprocessed_tweet, 'Predicted Sentiment': prediction[0]})
                
                # Display the results DataFrame
                # for result in results:
                results_df = pd.DataFrame(results)
                
                # Display the results DataFrame
                st.write(results_df)
                
        
        else:
            st.write('The uploaded file does not contain a "Tweets" column.')

# elif option == 'GET TWEETS FROM SCRAPPER 1':
#     username = st.sidebar.text_input('Enter a Twitter username')
#     if username:
#         tweets = get_tweets(username)
#         for tweet in tweets:
#             st.write(tweet.full_text)

elif option == 'GET TWEETS FROM SCRAPPER':
    username = st.sidebar.text_input('Enter a Twitter username')
    if username:
        if st.sidebar.button('Predict from Tweepy'):
            tweets = get_tweets_tweepy(username)
            if tweets:
                for tweet in tweets:
                    st.write(tweet.full_text)
                if st.button('Predict'):
                    predict_tweets(tweets)
            else:
                st.write('No tweets found for this username.')
        

        elif st.sidebar.button('Predict from Nitter'):
            tweets = get_tweets_Nitter(username)
            if tweets:
                for tweet in tweets:
                    st.write(tweet)
                if st.button('Predict'):
                    predict_tweets(tweets)
            else:
                st.write('No tweets found for this username.')

# elif option == 'DISPLAY STATISTICS':
#     data = pd.read_csv('DataCleaning_SentimentCreation_df.csv')
#     # sentiment_vader
#     if 'cleaned_text_english_only' in data.columns and 'airline' in data.columns and 'tweet_created' in data.columns:
#         data['tweet_created'] = pd.to_datetime(data['tweet_created']).dt.date  # Ensure the date column only contains the date part
#         if st.button('Show Statistics'):
#             for date in data['tweet_created'].unique():
#                 daily_data = data[data['tweet_created'] == date]
#                 for airline in daily_data['airline'].unique():
#                     airline_data = daily_data[daily_data['airline'] == airline]
#                     good_tweets = sum(airline_data['sentiment_vader'] == 'positive')
#                     bad_tweets = sum(airline_data['sentiment_vader'] == 'negative')
#                     st.write(f"On {date}, airline {airline} had {good_tweets} good tweets and {bad_tweets} bad tweets.")
#     else:
#         st.write('The CSV file must contain "Tweets", "airline", and "date" columns.')

elif option == 'DISPLAY STATISTICS':
    data = pd.read_csv('DataCleaning_SentimentCreation_df.csv')
    if 'cleaned_text_english_only' in data.columns and 'airline' in data.columns and 'tweet_created' in data.columns:
        data['tweet_created'] = pd.to_datetime(data['tweet_created']).dt.date  # Ensure the date column only contains the date part
        if st.button('Show Statistics'):
            for date in data['tweet_created'].unique():
                daily_data = data[data['tweet_created'] == date]
                airlines = []
                good_tweets = []
                bad_tweets = []
                for airline in daily_data['airline'].unique():
                    airline_data = daily_data[daily_data['airline'] == airline]
                    airlines.append(airline)
                    good_tweets.append(sum(airline_data['sentiment_vader'] == 'positive'))
                    bad_tweets.append(sum(airline_data['sentiment_vader'] == 'negative'))
                
                # Create a bar chart
                fig, ax = plt.subplots()
                ax.bar(airlines, good_tweets, label='Good tweets')
                ax.bar(airlines, bad_tweets, bottom=good_tweets, label='Bad tweets')
                ax.set_xlabel('Airline')
                ax.set_ylabel('Number of tweets')
                ax.set_title(f'Tweet statistics for {date}')
                ax.legend()

                # Display the chart
                st.pyplot(fig)
    else:
        st.write('The CSV file must contain "Tweets", "airline", and "date" columns.')