import re
import nltk

# Download corpus of stopwords if not existing
nltk.download('stopwords')


def compose(x, lof):
    """
    Applies a list of functions to a value by composition
    :param x: original input value to the functions
    :param lof: list of functions that take a single argument and return a value
    :return: the resulting value of composing "lof" and applying that function to "x"
    """
    res = x
    for func in lof:
        res = func(res)
    return res


def remove_rt(x):
    """
    Removes any retweet markers from the text of a tweet
    :param x: The text of a tweet
    :return: "x" with retweet text removed
    """
    return re.sub('RT @\w +: ', "", x)


def remove_tags(x):
    """
    Removes any tagged usernames from the text of a tweet
    :param x: The text of a tweet
    :return: "x" with tagged usernames removed
    """
    return re.sub("(@\w+)", "", x)


def remove_single_chars(x):
    """
    Removes any single character words from the text of a tweet
    :param x: The text of a tweet
    :return: "x" with single character words removed
    """
    return re.sub(" ([0-9A-Za-z \t]) ", " ", x)


def remove_links(x):
    """
    Removes any links from the text of a tweet
    :param x: The text of a tweet
    :return: "x" with links removed
    """
    return re.sub("(\w+:\/\/\S+)", "", x)


def remove_controls(x):
    """
    Removes any control characters from the text of a tweet
    :param x: The text of a tweet
    :return: "x" with control characters removed
    """
    return re.sub("(\\\\x\w{2})|(\\\\\w)", "", x)


def remove_punctuation(x):
    """
    Removes any punctuation from the text of a tweet
    :param x: The text of a tweet
    :return: "x" with punctuation removed
    """
    return re.sub("[^\w\d\s]", "", x)


def remove_whitespace(x):
    """
    Removes any whitespace from the text of a tweet
    :param x: The text of a tweet
    :return: "x" with whitespace removed
    """
    return re.sub("[^\w\d]+", " ", x)


def clean_tweet(tweet_text):
    """
    Applies all above cleaning functions to the inputted tweet text and also sets the tweet to lowercase
    :param tweet_text: The text of a tweet
    :return: The fully cleaned tweet text
    """
    rm_all = compose(tweet_text, [remove_rt, remove_tags, remove_single_chars, remove_links, remove_controls, remove_punctuation, remove_whitespace])
    lower = rm_all.lower()
    return lower


# Download a corpus of stopwords
stopword = nltk.corpus.stopwords.words('english')
ps = nltk.PorterStemmer()


def stem_tweet(tweet_text):
    """
    Applies stemming to an inputted tweet
    :param tweet_text: The text of a tweet
    :return: The fully stemmed tweet text
    """
    # Remove numbers
    text_rc = re.sub('[0-9]+', '', tweet_text)
    # Split on whitespace
    tokens = re.split('\W+', text_rc)
    # Remove stopwords and apply stemming
    text = [ps.stem(word) for word in tokens if word not in stopword]
    return ' '.join(text)
