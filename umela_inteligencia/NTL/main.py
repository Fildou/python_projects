import nltk
import requests
import matplotlib.pyplot as plt
import pandas as pd

from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS


def getHTMLdoc(url):
    response = requests.get(url)
    return response.text


def sentiment_count(sentimentList):
    positive = 0
    negative = 0
    neutral = 0

    for sentiment in sentimentList:
        if sentiment['compound'] > 0:
            positive += 1
        elif sentiment['compound'] < 0:
            negative += 1
        elif sentiment['compound'] == 0:
            neutral += 1

    return positive, negative, neutral


def common_words(wordFreq):
    most_frequent = wordFreq.most_common(30)
    print('30 Most frequent words:')
    for freq in most_frequent:
        print(freq[0] + ' -> ' + str(freq[1]), end=', ')


def longest_words(tokenized_review):
    long = sorted(tokenized_review, key=len, reverse=True)
    long = long[:30]
    print('\n30 Longest words:')
    for l in long:
        print(l, ' -> ' + str(len(l)), end=', ')


def wordcloud_sentiment(positive, negative, neutral):

    df = pd.DataFrame({'word': ['positive', 'negative', 'neutral'],
                       'count': [positive, negative, neutral]})
    data = df.set_index('word').to_dict()['count']
    wc = WordCloud(width=800, height=400, max_words=200).generate_from_frequencies(data)
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def wordcloud_common(wordFreq):
    most_frequent = wordFreq.most_common(30)
    word_list = []
    count_list = []
    for freq in most_frequent:
        word_list.append(freq[0])
        count_list.append(freq[1])
    df = pd.DataFrame({'word': word_list,
                       'count': count_list})
    data = df.set_index('word').to_dict()['count']
    wc = WordCloud(width=800, height=400, max_words=200).generate_from_frequencies(data)
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def wordcloud_longest(tokenized_review):
    long = sorted(tokenized_review, key=len, reverse=True)
    long = long[:30]
    word_list = []
    count_list = []
    for l in long:
        word_list.append(l)
        count_list.append(len(l))
    df = pd.DataFrame({'word': word_list,
                       'count': count_list})
    data = df.set_index('word').to_dict()['count']
    wc = WordCloud(width=800, height=400, max_words=200).generate_from_frequencies(data)
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()


print('\n\n\nFIRST MOVIE \n ------------------------')
review = ''
reviewList = []
sentimentList = []
count = 0

url = "https://www.rottentomatoes.com/m/spider_man_no_way_home/reviews"
html_doc = getHTMLdoc(url)
soup = BeautifulSoup(html_doc, "html.parser")
hit = soup.find_all('div', {'class': 'the_review'})
print(hit)

for h in hit:
    review += h.text
    reviewList += [h.text]
    count += 1

tokenized_review = nltk.word_tokenize(review)

for rl in reviewList:
    intensity = SentimentIntensityAnalyzer()
    polarity = intensity.polarity_scores(rl)
    sentimentList += [polarity]

print('URL = ', url)
print('# Reviews = ', count)
positive, negative, neutral = sentiment_count(sentimentList)
print('Sentiments:\nPositive: {0}, Negative: {1}, Neutral: {2}'.format(
    positive, negative, neutral))
wordFreq = nltk.FreqDist(tr.lower() for tr in tokenized_review)
common_words(wordFreq)
longest_words(tokenized_review)
wordcloud_sentiment(positive, negative, neutral)
wordcloud_common(wordFreq)
wordcloud_longest(tokenized_review)

######################## second movie
print('\n\n\n SECOND MOVIE \n ------------------------')
review = ''
reviewList = []
sentimentList = []
count = 0

url = "https://www.rottentomatoes.com/m/deep_water_2022/reviews"
html_doc = getHTMLdoc(url)
soup = BeautifulSoup(html_doc, "html.parser")
hit = soup.find_all('div', {'class': 'the_review'})

for h in hit:
    review += h.text
    reviewList += [h.text]
    count += 1

tokenized_review = nltk.word_tokenize(review)

for rl in reviewList:
    intensity = SentimentIntensityAnalyzer()
    polarity = intensity.polarity_scores(rl)
    sentimentList += [polarity]

print('URL = ', url)
print('# Reviews = ', count)
positive, negative, neutral = sentiment_count(sentimentList)
print('Sentiments:\nPositive: {0}, Negative: {1}, Neutral: {2}'.format(
    positive, negative, neutral))
wordFreq = nltk.FreqDist(tr.lower() for tr in tokenized_review)
common_words(wordFreq)
longest_words(tokenized_review)
wordcloud_sentiment(positive, negative, neutral)
wordcloud_common(wordFreq)
wordcloud_longest(tokenized_review)

################## third movie
print('\n\n\n THIRD MOVIE \n ------------------------')
review = ''
reviewList = []
sentimentList = []
count = 0

url = "https://www.rottentomatoes.com/m/windfall_2022/reviews"
html_doc = getHTMLdoc(url)
soup = BeautifulSoup(html_doc, "html.parser")
hit = soup.find_all('div', {'class': 'the_review'})

for h in hit:
    review += h.text
    reviewList += [h.text]
    count += 1

tokenized_review = nltk.word_tokenize(review)

for rl in reviewList:
    intensity = SentimentIntensityAnalyzer()
    polarity = intensity.polarity_scores(rl)
    sentimentList += [polarity]

print('URL = ', url)
print('# Reviews = ', count)
positive, negative, neutral = sentiment_count(sentimentList)
print('Sentiments:\nPositive: {0}, Negative: {1}, Neutral: {2}'.format(
    positive, negative, neutral))
wordFreq = nltk.FreqDist(tr.lower() for tr in tokenized_review)
common_words(wordFreq)
longest_words(tokenized_review)
wordcloud_sentiment(positive, negative, neutral)
wordcloud_common(wordFreq)
wordcloud_longest(tokenized_review)
