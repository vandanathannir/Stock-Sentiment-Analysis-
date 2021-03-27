from urllib.request import urlopen, Request 
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd 
import matplotlib.pyplot as plt 


URL = "https://finviz.com/quote.ashx?t="
listOfStocks = ['AMZN','FB', 'GOOGL', 'TSLA', 'MSFT']

news_tables = {}

for i in listOfStocks:
    url = URL + i

    req = Request(url = url, headers ={'user-agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, 'html')
    news_table = html.find(id='news-table')
    news_tables[i]=news_table

parsed_data = []

for i, news_tables in news_tables.items():
    for row in news_tables.findAll('tr'):
        title = row.a.get_text()
        date_data = row.td.text.split(' ')
        if len(date_data) ==1:
            time = date[0]
        else:
            date = date_data[0]
            time = date_data[1]
        parsed_data.append([i,date,time,title])
        
df = pd.DataFrame(parsed_data, columns = ['Stock', 'date', 'Time', 'Title'])
vader = SentimentIntensityAnalyzer()
f = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['Title'].apply(f)
df['date'] = pd.to_datetime(df.date).dt.date

plt.figure(figsize=(10,8))

mean_df = df.groupby(['Stock','date']).mean()
mean_df = mean_df.unstack()
mean_df = mean_df.xs('compound', axis = "columns").transpose()
mean_df.plot(kind ='bar' )
plt.title("Sentiment Analysis")
plt.xlabel("Date")
plt.ylabel("Compound Analysis")
plt.show()
