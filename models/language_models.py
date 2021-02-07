from utils.tokenizer import Tokenizer


class NGramModel:
    """ This is an N-gram Language model that can be
        trained, generate new text, write to a file,
        and test perplexity of texts based on the model.
    """

    def __init__(self, n=3):
        """ Initiates the language model
            requires positive integer for n
            greater than 0
        """

        from collections import defaultdict
        self._n = n
        self._ngrams = defaultdict(int)
        self._ngrams_1 = defaultdict(int)
        self._tok_types = defaultdict(int)
        self._tok_count = 0
        self._smoothing = False

    def ngrams(self, tokens, n):
        """ generates a list of tuples
            size of n
            returns a list
        """

        ngram_tokens = []
        for i in range(len(tokens)-n+1):
            ngram_tokens.append(tuple(tokens[i:i+n]))
        return ngram_tokens

    def train(self, token_sequences):
        """ Builds several dictionaries of type
            distributions within the text
            Builds: 
                n-gram dictionary
                n-1 gram dictionary
                type dictionary with counts
                token count

        """

        # handling lists of lists
        if all(isinstance(x, list) for x in token_sequences):
            for x in token_sequences:
                self.train(x)
        else:
            # building dictionary of types and token count
            toks = token_sequences.copy()
            for i in toks:
                self._tok_count += 1
                self._tok_types[i] += 1
            self._tok_types[None] = 1
            self._tok_count += 1

            # building both n-gram and n-1 gram dictionaries
            if self._n > 1:
                # Generating Padding tokens around tokens
                for i in range(self._n-1):
                    toks.insert(0, None)
                    toks.append(None)

                # generates n-1 gram dictionary
                grams_1 = self.ngrams(toks, self._n-1)
                for i in grams_1:
                    self._ngrams_1[i] += 1

                # generates n-gram dictionary
                grams = self.ngrams(toks, self._n)
                for i in grams:
                    self._ngrams[i] += 1
            else:

                # buiding dictionary for unigram models
                for i in range(self._n):
                    toks.insert(0, None)
                    toks.append(None)

                grams = self.ngrams(toks, self._n)
                for i in grams:
                    self._ngrams[i] += 1

    def p_next(self, tokens):
        """ Generates a list of probable words
            to follow the current n-gram
        """

        next_word = {}
        if self._n > 1:
            for i in self._tok_types:
                p = self._ngrams.get(tuple(tokens+[i]), 0)
                if p > 0:
                    next_word[i] = p/(self._ngrams_1[tuple(tokens)])
        else:

            # generates probabilities for unigram models
            for i in self._tok_types:
                next_word[i] = self._tok_types[i]/self._tok_count

        return next_word

    def generate(self):
        """ Generates new text from the model using
            random choice weighted by pobability distributions
            within the model
            returns a list
        """
        # building n-gram start with n-1 None values
        import numpy as np
        n = self._n-1
        string = []
        string += [None]*n

        # generating string
        while True:
            if self._n > 1:
                # creates moving window for n-gram generation
                l = len(string)
                window = string[l-n:l]
                if type(window) == str:
                    window = [window]
                next_word = self.p_next(window)
                new = np.random.choice(
                    list(next_word.keys()), 1, list(next_word.values()))[0]
            else:
                # generates uni-gram words
                next_word = self.p_next(string)
                new = np.random.choice(
                    list(next_word.keys()), 1, list(next_word.values()))[0]

            # If end of sentence None marker generated,
            # breaks and returns value
            # or adds to string and continues
            if new == None:
                break
            else:
                string.append(new)

        return string

    def write(self, filename, num=5):
        """ Writes generated texts to file
            a number of entries can be included 
            in variable 'num', default is 5
        """

        with open(filename, 'w') as f:
            for i in range(num):
                f.write(Tokenizer.detokenize(self.generate()))
                f.write('\n')

    def perplexity(self, string, smoothing=False):
        """ Calculates the perplexity of a string, 
            Applies Laplace smoothing in all cases
        """

        from math import log2

        # create a padded tokenized string
        tokens = Tokenizer.tokenize(string)
        tokens.insert(0, None)
        tokens.append(None)

        # model n-gram generation
        n_grams = self.ngrams(tokens, self._n)
        for gram in n_grams:
            if gram not in self._ngrams:
                smoothing = True

        self._smoothing = smoothing
        # produces probabilites with Laplace smoothing
        total = 0
        # Probabilties for non unigram models
        if self._n > 1:
            if smoothing:
                for i in range(len(tokens)-self._n+1):
                    # if key is not found, a default value is presented
                    total += log2(float((
                        self._ngrams.get(tuple(tokens[i:i+self._n]), 0)+1) /
                        (self._ngrams_1.get(tuple(tokens[i:i+self._n-1]), 0)
                         + len(self._ngrams_1))))

            else:
                for i in range(len(tokens)-self._n+1):
                    # if key is not found, a default value is presented
                    total += log2(self._ngrams.get(tuple(
                        tokens[i:i+self._n]))/self._ngrams_1.get(
                        tuple(tokens[i:i+self._n-1])))
        else:
            # unigram model probablities
            if smoothing:
                for i in range(len(tokens)-1):
                    total += log2(float((self._tok_types.get(tokens[i], 0)+1)/(
                        self._tok_count+len(self._ngrams))))
            else:
                for i in range(len(tokens)-1):
                    total += log2(
                        float(self._tok_types.get(tokens[i])/self._tok_count))

        # Returns perplexity
        return -1*total/len(n_grams) if total < 0 else 0

    def stats(self, n=5):
        # top ngrams
        if self._n > 1:
            print('Top {}-grams:'.format(self._n))
            grams = sorted([key for key in self._ngrams.keys(
            ) if None not in key], reverse=True, key=lambda x: self._ngrams[x])
            for k in grams[:n]:
                print('\t', [i for i in k], ':', self._ngrams[k])
            print('\n')

        # top n-1 grams
        if self._n > 2:
            print('Top {}-grams:'.format(self._n-1))
            grams = sorted([key for key in self._ngrams_1.keys()
                            if None not in key], reverse=True,
                           key=lambda x: self._ngrams_1[x])
            for k in grams[:n]:
                print('\t', [i for i in k], ':', self._ngrams_1[k])

        # top n words
        print('Top {} most frequent types:'.format(n))
        terms = sorted(
            [(val, key) for key, val in self._tok_types.items()
             if key != None], reverse=True)
        for v, k in terms[:n]:
            print('\t'+k+':', v)


if __name__ == '__main__':
    lm = NGramModel(4)
    with open('train_shakespeare.txt', 'r') as f:
        text = f.read()
    sents = [Tokenizer.tokenize(sent) for sent in text.split('\n')]
    lm.train(sents)
    print('Generate test:', Tokenizer.detokenize(lm.generate()))
    lm.stats()
    try:
        lm.write('test_file.txt', 3)
        print('Written successfully')
    except:
        print('Failed to write')
