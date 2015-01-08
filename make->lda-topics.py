import lda, csv, string

import numpy as np

from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from awesome_print import ap
punkt = set(string.punctuation)
stopwords = set(open('stopwords.txt').read().splitlines())
#data = filter(lambda x: x != 'none',[shift['Student Comment'].lower().strip() for shift in csv.DictReader(open('comments.csv'))])
data = [line.lower() for line in open('./sinai/combined','rb').read().splitlines()]
data = [' '.join([''.join(ch for ch in word if ord(ch)<128) for word in line.split() 
		if word not in stopwords and 'file://' not in word and not any([ch in punkt for ch in word])]) for line in data]
tfx = TfidfVectorizer(data,tokenizer=word_tokenize,strip_accents='unicode',
	ngram_range=(1,3),min_df=3, use_idf=True)
tfidf = tfx.fit_transform(data)

model = lda.LDA(n_topics=10, n_iter=1000,random_state=1)
model.fit(tfidf)

topic_word = model.topic_word_
n_top_words = 10


with open('lda-topics_short.txt','wb') as outfile:
	for i,topic_dist in enumerate(topic_word):
		topic_words = np.array(data)[np.argsort(topic_dist)][:-n_top_words:-1]
		print>>outfile,'Topic {}: {}'.format(i, ' '.join(topic_words))
