import re


def compose(x, lof):
    res = x
    for func in lof:
        res = func(res)
    return res


def remove_rt(x):
    return re.sub('RT @\w +: ', "", x)


def remove_tags(x):
    return re.sub("(@\w+)", "", x)


def remove_single_chars(x):
    return re.sub(" ([0-9A-Za-z \t]) ", " ", x)


def remove_links(x):
    return re.sub("(\w+:\/\/\S+)", "", x)


def remove_controls(x):
    return re.sub("(\\\\x\w{2})|(\\\\\w)", "", x)


def remove_punctuation(x):
    return re.sub("[^\w\d\s]", "", x)


def remove_whitespace(x):
    return re.sub("[^\w\d]+", " ", x)


def clean_tweet(tweet_text):
    rm_all = compose(tweet_text, [remove_rt, remove_tags, remove_single_chars, remove_links, remove_controls, remove_punctuation, remove_whitespace])
    lower = rm_all.lower()
    return lower
