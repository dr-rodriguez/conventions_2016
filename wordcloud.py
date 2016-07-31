# Script to generate a word cloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.misc import imread
import matplotlib.pyplot as plt
import os


def make_cloud(words, image, size=10, filename='figures/cloud.png', max_words=200, horizontal=0.8):

    # Remove URLs, 'RT' text, screen names, etc
    my_stopwords = ['RT', 'amp', 'lt']
    words_no_urls = ' '.join([word for word in words.split()
                              if word not in my_stopwords])

    # Add stopwords, if needed
    stopwords = STOPWORDS.copy()
    stopwords.add("RT")
    stopwords.add('amp')
    stopwords.add('lt')

    # Load up a logo as a mask & color image
    logo = imread(image)

    # Generate colors
    image_colors = ImageColorGenerator(logo)

    # Generate plot
    wc = WordCloud(stopwords=stopwords, mask=logo, color_func=image_colors, scale=0.8,
                   max_words=max_words, background_color='white', random_state=42, prefer_horizontal=horizontal)

    wc.generate(words_no_urls)

    plt.figure(figsize=(size, size))
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(filename)

# ==============================================
# Load Hillary Clinton speech
with open('dnc/hillary_clinton.txt', 'r') as f:
    text = f.read()

make_cloud(text, 'logos/DemocraticLogo.png', filename='figures/clinton_cloud.png', max_words=200, horizontal=0.8)

# ==============================================
# Load Donald Trump speech
with open('rnc/donald_trump.txt', 'r') as f:
    text = f.read()

make_cloud(text, 'logos/RepublicanLogo.png', filename='figures/trump_cloud.png', max_words=200, horizontal=0.8)

# ==============================================
# Load all DNC speeches
mypath = 'dnc/'
text_list = list()
for file in [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]:
    if file.startswith('.'): continue
    with open(os.path.join(mypath,file), 'r') as f:
        data = f.read()
    text_list.append(data)

text = ' '.join(text_list)
make_cloud(text, 'logos/DemocraticLogo.png', filename='figures/dnc_cloud.png', max_words=200, horizontal=0.8, size=12)

# ==============================================
# Load all RNC speeches
mypath = 'rnc/'
text_list = list()
for file in [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]:
    if file.startswith('.'): continue
    with open(os.path.join(mypath,file), 'r') as f:
        data = f.read()
    text_list.append(data)

text = ' '.join(text_list)
make_cloud(text, 'logos/RepublicanLogo.png', filename='figures/rnc_cloud.png', max_words=200, horizontal=0.8, size=12)
