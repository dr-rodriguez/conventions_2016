# Script to look into the sentiments

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from collections import Counter
import string
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# =======================================================
# Load up the sentiment data
filename = 'NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt'
sentiment_data = pd.read_csv(filename, delim_whitespace=True, skiprows=45, header=None, names=['word', 'affect', 'flag'])

stop_words = set(stopwords.words('english'))
stop_words.update([s for s in string.punctuation] + ['\xe2', '\x80', '\x93', '\xe2\x80\x94',
                                                     '\xe2\x80\x93', '\xe2\x80\x99', u'\u2019', u'\u2013'])

def get_sentiment(text):
    emotion_words = dict()
    emotion_map = dict()
    affects = ['positive', 'negative', 'anger', 'anticipation', 'disgust',
               'fear', 'joy', 'sadness', 'surprise', 'trust']
    for key in affects:
        emotion_words[key] = sentiment_data[(sentiment_data['affect'] == key) & (sentiment_data['flag'] == 1)]['word'].tolist()
        emotion_map[key] = list()

    # Note no stemming or it may fail to match words
    words = Counter([i.lower() for i in wordpunct_tokenize(text)
                 if i.lower() not in stop_words])
    for key in emotion_words.keys():
        x = set(emotion_words[key]).intersection(words.keys())
        emotion_map[key].append(len(x))
    sentiment = pd.DataFrame(emotion_map)
    return sentiment

# =======================================================
# Loop through DNC files
mypath = 'dnc/'
counts = dict()
full_sentiments = None
for file in [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]:
    if file.startswith('.'): continue
    print file
    with open(os.path.join(mypath,file), 'r') as f:
        data = f.read()
    s = get_sentiment(data)
    name = ' '.join([word.capitalize() for word in file[:-4].split('_')])
    s.index = [file[:-4]]
    s['Speaker'] = name
    if full_sentiments is None:
        full_sentiments = s
    else:
        full_sentiments = pd.concat([full_sentiments, s])

    words = Counter([i.lower() for i in wordpunct_tokenize(data)
                     if i.lower() not in stop_words])
    counts[file[:-4]] = len(words)

# Full set of speakers
fig = plt.figure()
ax = sns.barplot(data=full_sentiments, palette='Blues_d', estimator=sum, ci=None)
ax.set_xlabel('Emotions')
ax.set_ylabel('Word Count')
ax.set_title('Democratic National Convention')
plt.savefig('figures/dnc_full.png')

# Treat speakers individually
tidy_sentiments = pd.melt(full_sentiments, id_vars='Speaker', value_vars=full_sentiments.columns.tolist()[:-1])

fig = plt.figure()
ax = sns.barplot(data=tidy_sentiments, hue='Speaker', x='variable', y='value', palette='Paired')
ax.set_xlabel('Emotions')
ax.set_ylabel('Word Count')
ax.set_title('Democratic National Convention')
plt.savefig('figures/dnc_individual.png')

# Normalized
normalized_sentiments = full_sentiments.drop('Speaker', axis=1)
for name in counts:
    normalized_sentiments[normalized_sentiments.index == name] /= counts[name]
for name in counts:
    normalized_sentiments.loc[normalized_sentiments.index == name,'Speaker'] = ' '.join([word.capitalize() for word in name.split('_')])

tidy_sentiments = pd.melt(normalized_sentiments, id_vars='Speaker', value_vars=full_sentiments.columns.tolist()[:-1])

fig = plt.figure()
ax = sns.barplot(data=tidy_sentiments, hue='Speaker', x='variable', y='value', palette='Paired')
ax.set_xlabel('Emotions')
ax.set_ylabel('Normalized Word Count')
ax.set_title('Democratic National Convention')
plt.savefig('figures/dnc_normalized.png')

dnc = normalized_sentiments

# =======================================================
# Repeat for RNC
mypath = 'rnc/'
counts = dict()
full_sentiments = None
for file in [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]:
    if file.startswith('.'): continue
    print file
    with open(os.path.join(mypath,file), 'r') as f:
        data = f.read()
    s = get_sentiment(data)
    name = ' '.join([word.capitalize() for word in file[:-4].split('_')])
    s.index = [file[:-4]]
    s['Speaker'] = name
    if full_sentiments is None:
        full_sentiments = s
    else:
        full_sentiments = pd.concat([full_sentiments, s])

    words = Counter([i.lower() for i in wordpunct_tokenize(data)
                     if i.lower() not in stop_words])
    counts[file[:-4]] = len(words)

# Full set of speakers
fig = plt.figure()
ax = sns.barplot(data=full_sentiments, palette='Reds_d', estimator=sum, ci=None)
ax.set_xlabel('Emotions')
ax.set_ylabel('Word Count')
ax.set_title('Republican National Convention')
plt.savefig('figures/rnc_full.png')

# Treat speakers individually
tidy_sentiments = pd.melt(full_sentiments, id_vars='Speaker', value_vars=full_sentiments.columns.tolist()[:-1])

fig = plt.figure()
ax = sns.barplot(data=tidy_sentiments, hue='Speaker', x='variable', y='value', palette='Paired')
ax.set_xlabel('Emotions')
ax.set_ylabel('Word Count')
ax.set_title('Republican National Convention')
plt.savefig('figures/rnc_individual.png')

# Normalized
normalized_sentiments = full_sentiments.drop('Speaker', axis=1)
for name in counts:
    normalized_sentiments[normalized_sentiments.index == name] /= counts[name]
for name in counts:
    normalized_sentiments.loc[normalized_sentiments.index == name,'Speaker'] = ' '.join([word.capitalize() for word in name.split('_')])

tidy_sentiments = pd.melt(normalized_sentiments, id_vars='Speaker', value_vars=full_sentiments.columns.tolist()[:-1])

fig = plt.figure()
ax = sns.barplot(data=tidy_sentiments, hue='Speaker', x='variable', y='value', palette='Paired')
ax.set_xlabel('Emotions')
ax.set_ylabel('Normalized Word Count')
ax.set_title('Republican National Convention')
plt.savefig('figures/rnc_normalized.png')

rnc = normalized_sentiments

# =======================================================
# Both at once

dnc['Party'] = 'Democrat'
rnc['Party'] = 'Republican'
full_sentiments = pd.concat([dnc, rnc])
full_sentiments.drop('Speaker', axis=1, inplace=True)

tidy_sentiments = pd.melt(full_sentiments, id_vars='Party', value_vars=full_sentiments.columns.tolist()[:-1])

fig = plt.figure()
ax = sns.barplot(data=tidy_sentiments, hue='Party', x='variable', y='value', ci=None,
                 palette={'Democrat': 'blue', 'Republican': 'red'})
ax.set_xlabel('Emotions')
ax.set_ylabel('Average Normalized Word Count')
plt.savefig('figures/convention_full.png')
