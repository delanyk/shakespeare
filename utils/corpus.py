def tokenize(text):
    from nltk import word_tokenize
    tokens = word_tokenize(text.lower())

    return tokens


def detokenize(tokens):

    # markers for punction and contractions
    punct = ['!', '.', "'", '?', ',', ':', ';']
    short = ["'twas", "'tis", "'t", "'twixt"]

    # creates a modified token list
    toks = []
    for n, i in enumerate(tokens):
        # Remove None values from construction
        if i == None:
            continue

        # capitalizes first word
        elif not toks or i == 'i':
            toks.append(i.capitalize())

        # Attach punction and contractions to previous tokens
        elif i[0] in punct and tokens[n-1] not in punct \
                and i not in short and len(i) <= 3:
            toks[-1] = toks[-1]+i

        # Capitlizes tokens after ending punctuation
        elif tokens[n-1] in '?.!\n':
            if tokens[n-1] == '\n':
                toks[-1] = toks[-1]+i.capitalize()
            else:
                toks.append(i.capitalize())
        else:
            toks.append(i)

    return ' '.join([i for i in toks if i])
