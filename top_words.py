# Get the top words in Hillary Clinton and Donald Trump speeches

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.porter import PorterStemmer
from collections import Counter
import string
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import codecs  # to avoid encoding errors when reading files
import numpy as np

stop_words = set(stopwords.words('english'))
stop_words.update([s for s in string.punctuation] + ['\xe2', '\x80', '\x93', '\xe2\x80\x94',
                                                     '\xe2\x80\x93', '\xe2\x80\x99', u'\u2019', u'\u2013'])
porter = PorterStemmer()
stem = True  # activate stemming

# ==============================================
# Load Hillary Clinton speech
with codecs.open('dnc/hillary_clinton.txt', 'r', 'utf-8') as f:
    text = f.read()

if stem:
    words = Counter([porter.stem(i.lower()) for i in wordpunct_tokenize(text)
                     if i.lower() not in stop_words])
else:
    words = Counter([i.lower() for i in wordpunct_tokenize(text)
                     if i.lower() not in stop_words])

clinton = words.most_common(10)
c_words = words

# ==============================================
# Load Donal Trump speech
with codecs.open('rnc/donald_trump.txt', 'r', 'utf-8') as f:
    text = f.read()

if stem:
    words = Counter([porter.stem(i.lower()) for i in wordpunct_tokenize(text)
                     if i.lower() not in stop_words])
else:
    words = Counter([i.lower() for i in wordpunct_tokenize(text)
                     if i.lower() not in stop_words])

trump = words.most_common(10)
t_words = words

# ==============================================
# Construct DataFrame
c_keys = [s[0] for s in clinton]
t_keys = [s[0] for s in trump]

columns = np.array(list(set(c_keys) | set(t_keys)))

c_row = np.array([c_words[elem] for elem in columns])
t_row = np.array([t_words[elem] for elem in columns])

ind = np.argsort(c_row)[::-1]
c_row = c_row[ind]
t_row = t_row[ind]
columns = columns[ind]

columns = np.append(columns, 'Speaker')
c_row = np.append(c_row, 'Hillary Clinton')
t_row = np.append(t_row, 'Donald Trump')

data = pd.DataFrame([c_row, t_row], columns=columns)

# ==============================================
# Plot it

tidy_data = pd.melt(data, id_vars='Speaker', value_vars=data.columns.tolist()[:-1])
tidy_data['value'] = pd.to_numeric(tidy_data['value'])

fig = plt.figure()
ax = sns.barplot(data=tidy_data, hue='Speaker', x='variable', y='value', ci=None,
                 palette={'Hillary Clinton': 'blue', 'Donald Trump': 'red'})
ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)
ax.set_xlabel('Words')
ax.set_ylabel('Count')
plt.tight_layout()
plt.savefig('figures/top_words.png')