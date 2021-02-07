import re

class Tokenizer:

    def __init__(self) -> None:
        # numbers
        num = r'\b[0-9\.]+\b'
        # punctuation
        punct = r'[\u0021-\u002f\u003a-\u0040\u005b-\u0060\u007b-\u007e\u00a1-\u00bf\u00d7\u00f7\u2013-\u204a]'
        # general words
        word = r'(?:[a-zA-Z\U0001d5d4-\U0001d607]+)|(?:[a-zA-Z\U0001d5d4-\U0001d607-]+)'
        # contractions
        contract = r'n?\'[a-zA-Z]+'
        # abbriviations
        abbriv = r'[A-Z]\.[A-Z]\.([A-Z]\.)?'
        # elipses
        elipses = r'[\.]{3,}'


        # set of tokens
        token_set = [
            contract,
            abbriv, 
            word,
            num,
            elipses,
            punct
            ]

        # compile search pattern including spaces
        self.token_pattern = re.compile(r'\s+|('+r'|'.join(token_set)+r')', re.UNICODE)

    def tokenize(self,text:str) -> list:
        tokens = [i for i in self.token_pattern.split(text.lower()) if i]

        return tokens


    @staticmethod
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
