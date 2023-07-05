import nltk
nltk.download('vader_lexicon')
import feedparser
from nltk.sentiment import SentimentIntensityAnalyzer
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    if compound_score >= 0.05:
        sentiment = 'Positivo'
    elif compound_score <= -0.05:
        sentiment = 'Negativo'
    else:
        sentiment = 'Neutro'
    
    return sentiment

feed_url = 'https://news.yahoo.com/rss/us'
feed = feedparser.parse(feed_url)

news_titles = []  # Lista para armazenar os títulos das notícias

for entry in feed.entries:
    text = entry.title
    news_titles.append(text)  # Adiciona o título à lista

# Configuração do Tkinter
root = tk.Tk()
root.title('Títulos das notícias dos EUA')

# Configuração da tabela
tree_frame = ttk.Frame(root)
tree_frame.pack(pady=10)

tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side='right', fill='y')

tree = ttk.Treeview(tree_frame, columns=['Título'], yscrollcommand=tree_scroll.set)
tree.heading('#0', text='ID')
tree.heading('Título', text='Título')

# Adiciona os títulos das notícias à tabela
for i, title in enumerate(news_titles):
    tree.insert('', 'end', text=str(i), values=(title,))

tree.pack(side='left', fill='both')
tree_scroll.config(command=tree.yview)

# Configuração do gráfico de barras
chart_frame = ttk.Frame(root)
chart_frame.pack(pady=10)

positive_count = 0
negative_count = 0
neutral_count = 0

for title in news_titles:
    sentiment = analyze_sentiment(title)
    
    if sentiment == 'Positivo':
        positive_count += 1
    elif sentiment == 'Negativo':
        negative_count += 1
    else:
        neutral_count += 1

total_count = len(news_titles)
positive_percentage = (positive_count / total_count) * 100
negative_percentage = (negative_count / total_count) * 100
neutral_percentage = (neutral_count / total_count) * 100

labels = ['Positivo', 'Negativo', 'Neutro']
percentages = [positive_percentage, negative_percentage, neutral_percentage]
colors = ['green', 'red', 'blue']

plt.figure(figsize=(6, 4))
plt.bar(labels, percentages, color=colors)
plt.xlabel('Sentimento')
plt.ylabel('Porcentagem')
plt.title('Sentimento das notícias dos EUA')

# Exibir a mensagem sobre o cenário dos EUA abaixo do gráfico
if positive_percentage > negative_percentage and positive_percentage > neutral_percentage:
    sentiment_message = 'Cenário nos EUA: Bom'
    sentiment_color = 'green'
elif negative_percentage > positive_percentage and negative_percentage > neutral_percentage:
    sentiment_message = 'Cenário nos EUA: Ruim'
    sentiment_color = 'red'
else:
    sentiment_message = 'Cenário nos EUA: Normal'
    sentiment_color = 'blue'

plt.text(1, -20, sentiment_message, fontsize=12, color=sentiment_color)

plt.show()

root.mainloop()
