## Sentiment Analysis of YouTube Titles using YouTube Data API v3
This project is a sentiment analysis of the titles of the 200 most popular videos on YouTube, using the YouTube Data API v3. By analyzing the sentiment of these titles, the aim is to gain insight into the types of titles that are most successful on the platform, and to use this information to inform future title selection.

## Getting Started
To get started with this project, you will need to obtain an API key from the YouTube Data API v3, and install the necessary dependencies. Full instructions for setting up your API key and installing dependencies can be found in the setup.md file.

Once you have set up your API key and installed the necessary dependencies, you can run the sentiment_analysis.py script to collect and analyze the data. The resulting sentiment scores can be displayed in a juypter notebook.

## Understanding the Results
A binary mapping was applied to sentiment labels with positive labels having a binary label score of 1, and negative lables having a binary label of -1. The sentiment scores were calculated using a weighted voting system like this takes into account both the binary label and the confidence score for each video, giving more weight to videos with higher confidence scores. This approach can help to produce more accurate results than a simple majority vote or a binary classification based on a fixed threshold.

Further research can be conducted to analyze sentiment scores with video performance, providing additional insights into the types of titles that are most successful on the platform.
