from string import punctuation


def no_punc(s):
    return ''.join(c for c in s if c not in punctuation)
