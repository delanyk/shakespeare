from utils.tokenizer import Tokenizer
from models.language_models import NGramModel
from time import sleep


class ShakespeareSpeak:
    def __init__(self) -> None:
        self.trained = False



    def build_model(self):
        try:
            n = int(input('\nInput the gram size you would like: \n'))
            if n < 1:
                print("\nPlease enter a positive integer")
                sleep(1)
                self.build_model()
            self.trained = False
            sleep(1)
            return NGramModel(n)
        except:
            print("\nPlease enter a positive integer")
            sleep(1)
            self.build_model()

    @staticmethod
    def load_text():
        try:
            source = input('Please Enter the file name of text for training:\n')
            with open(source, 'r') as f:
                text = f.read()
            return [Tokenizer.tokenize(seq) for seq in text.split('\n')]
        except:
            print("Invalid file name")

    @staticmethod
    def load_perplexity():
        try:
            source = input(
                'Enter the file name of text for perplexity evaluation:\n')
            with open(source, 'r') as f:
                text = f.read()
            return [sent for sent in text.split('\n') if sent]
        except:
            print("Invalid file name")

    @staticmethod
    def untrained():
        print('\nSelection cannot be completed.\nModel is not trained.')
        print('\nPlease train model before making this selection.')
        sleep(2)

    def run(self):
        print("Thank you for choosing\nKing's n-gram Lanaguage Model\n")
        sleep(1)
        ans = input("Would you like to create an n-gram model?: (Y|n)\n")
        if ans == '':
            pass
        elif ans[0].lower() != 'y':
            sleep(1)
            print('Okay, goodbye\n')
            sleep(1)
            exit()
        sleep(1)
        lm = self.build_model()
        print('\nCompleted.')
        sleep(1)

        while True:
            sleep(1)
            print('\nOptions:')
            print('\t1. Build new n-gram model')
            print('\t2. Load and train model')
            print('\t3. Genereate text')
            print('\t4. Print texts to file')
            print('\t5. Show model statistics')
            print('\t6. Test Perplexity of text')
            print('\t7. Exit')

            try:
                res = int(input('\nPlease enter the number of your selection:\n'))
                assert (res >= 1 and res <= 8), sleep(1)
                sleep(1)
                print('\nokay\n')
            except:
                print('\nInvalid Selection\nPlease select an available option\n')
                res = 0
                sleep(1)

            if res == 1:

                lm = self.build_model()
                sleep(1)
                print('\nCompleted.\nNew models will need to be trained.')
                sleep(1)

            elif res == 2:
                data = self.load_text()
                if not data:
                    print('Invalid training data')
                    sleep(1)

                else:
                    lm.train(data)
                    trained = True
                    print('\nCompleted.\nModel is trained.')
                    sleep(1)

            elif res == 3:
                if not self.trained:
                    self.untrained()
                else:
                    try:
                        n = int(input('Enter the number of texts to be generate:\n'))

                        for i in range(n):
                            print('Text {}:'.format(i+1))
                            print(Tokenizer.detokenize(lm.generate()))
                            print('\n')
                            sleep(1)
                    except:
                        print('Invalid input\n')
                        sleep(1)

            elif res == 4:
                if not self.trained:
                    self.untrained()
                else:
                    try:
                        filename = input('Enter a file name:\n')
                        n = int(input('\nEnter the number of texts to be saved:\n'))

                        if n > 1:
                            lm.write(filename, n)
                            print('\nCompleted')
                            print('{} texts written to {}.\n'.format(str(n), filename))

                        elif n == 1:
                            lm.write(filename, n)
                            print('\nCompleted.')
                            print('{} text written to {}.\n'.format(str(n), filename))

                        else:
                            print('Invalid Input\n')
                            sleep(1)

                    except:
                        print('Invalid Input\n')
                        sleep(1)

            elif res == 5:
                if not self.trained:
                    self.untrained()
                else:
                    lm.stats()
                    sleep(3)

            elif res == 6:
                if not self.trained:
                    self.untrained()
                else:
                    try:
                        total = []
                        perp_sents = self.load_perplexity()
                        print('File loaded.\n')

                        ans = input(
                            'Would you like to see all or the average? (all|avg)\n')
                        if ans.lower() == 'all':
                            for n, sent in enumerate(perp_sents):
                                p = lm.perplexity(sent)
                                total.append(p)
                                print('Sentence {}:\n'.format(str(n+1)), sent)
                                print('Perplexity:', round(p, 4), '\n')
                                sleep(1)

                        elif ans.lower() == 'avg':
                            for sent in perp_sents:
                                total.append(lm.perplexity(sent))
                            print('\nAverage Perplexity:', round(
                                sum(total)/len(total), 4), '\n')
                            sleep(1)

                    except:
                        print('Invalid Input')
                        sleep(1)

            elif res == 7:
                sleep(1)
                print('Bye Bye\n')
                exit()
