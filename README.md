# Shakespeare Speak: n-gram Language Model Project

This project is a n-gram language model that accepts a loaded text and generate new texts based on the learned texts. Text can be generated on screen or be written to a text. After texts are generated or new texts as desired, their perplexity can be measured against the model. In addition, the model supports the looking under the hood and viewing what the underlying probabilities that form the language generating method.

<br/>
<br/>

## Structure

It is structured into three folders: <i>interface</i>, <i>models</i>, and <i>utilities</i>. <i>Interface</i> contains interactive class of the program.  The <i>models</i> folder contains the language model code, and the <i>utils</i> folder contains supportive class separate from the language model.
The <i>data</i> folder contains text files for training and development.
the file <i>main.py</i> runs the whole program.
<br/>
<br/>


## Running the Code

The main program and user interface is in <i>main.py</i>. It was written to run in Python3.

```bash

python3 main.py

```
<br/>
<br/>

### Initiation

The program will ask for a desire to build a language model and for an integer to designate the size of the <i>grams</i>.

```bash
Would you like to create an n-gram model?: (Y|n)
Y

Input the gram size you would like: 
4
```

This will intiate a model with the requested gram size. The options menu appear with options to perform new tasks. 

```bash
Options:
	1. Build new n-gram model
	2. Load and train model
	3. Genereate text
	4. Print texts to file
	5. Show model statistics
	6. Test Perplexity of text
	7. Exit
```
Building a new model will delete the previous model and will need to be retrained. Loading a text will train the model to be able to generate text. Options 3 and 4 will generate texts. Option 3 will generate text in the terminal, and option 4 will print that to a file name. Option 5 will show top n-grams and vocabulary in the model. Lastly, the perplexity of a text can be calculated using option 7.

<br/>
<br/>

### Loading Data and Model Training

For the option to load and train the model, the user must provide the path to the text file for training. The model will accept raw text where [new lines] will be used to separate sequences that will be used for training. If a file could be found, the model will the train itself and report that to the user. The model will then return to the options menu.

```bash
Please Enter the file name of text for training:
train_shakespeare.txt

Completed.
Model is trained.

```

<br/>
<br/>

### Text Generation

The text generation option will call upon the generation method of the language model and print the generated text within the window before returning to the options menu. Conditional probabilities are used to produce the range of likely terms to follow the current n-gram sequence. The choice is made by random choice weighted by the probabilities. This continues until and end-of-sentence token is generated.
<br/>The pogram will request the number of text that would like to be generated. 
The newly generated texts will then be printed and counted for the user and printed slowly to give the user a moment to read what is being printed.  

```
Enter the number of texts to be generate:
2
Text 1:
Custom hath made it in him a kind of hand-in-hand comparison -- had been something too fair and too good, to make modern and familiar, things supernatural and causeless. Hence is it that can tell me who it is: may it be done?


Text 2:
Weapons! Arms! What's hecuba to him, I pray thee now, tell me that? I think you know him well enough. Dost thou think, though I do hate thee worse.

```


<br/>
<br/>

### Printing to a file.

As with the text generation option, new texts will be generated but directly printed to a file. The program will ask for the filename in which to save the texts. If the file already exists, it will directly overwrite it. It will then prompt the number of texts to print, followed by a notification that the task had been completed.

```

Enter a file name:
new_text.txt

Enter the number of texts to be saved:
5

Completed
5 texts written to new_text.txt.

```
The generated texts will be broken by [new lines], appearing as below:

```
Hapless aegeon, whom the spital-house and ulcerous sores would cast the gorge at, this embalms and spices to the april day again. Come, thou shalt have to pay for it of us. Though now we must appear bloody and cruel, as, I think cassio's an honest man in it. I thank god and my cold blood, I am, necessity commands me name myself.

Advance your standards, and upon the grief of this suddenly died. Master constable, let these men be bound, and brought to leonato's: I will description the matter to you, good cornelius, and you must needs stay a time. I never prospered since I forswore myself at primero. Well, would demonstrate them now but goers backward.
```

<br/>
<br/>

### Model Statistics

This option will display the top n-grams that appear in the model, the top (n-1)-grams in the model, and the most frequent  individual terms that occur in the model. The defualt value for this in the progam is 5, it can be adjusted within the model to display more information. These grams do not include any padding tokens or end-of-sentence tokens.

```
Top 4-grams:
	 [',', 'my', 'lord', ','] : 169
	 [',', 'my', 'lord', '.'] : 158
	 ['i', 'pray', 'you', ','] : 115
	 [',', 'sir', ',', 'i'] : 63
	 [',', 'i', 'pray', 'you'] : 61


Top 3-grams:
	 [',', 'sir', ','] : 572
	 [',', 'my', 'lord'] : 505
	 ['my', 'lord', ','] : 327
	 [',', 'i', "'ll"] : 252
	 [',', 'i', 'will'] : 239
	 
Top 5 most frequent types:
	,: 42833
	.: 18911
	the: 13473
	i: 12297
	and: 12173

```

<br/>
<br/>

### Perplexity Evaluation

The program allows you to test the perplexity of stored documents. For a generated text to be evaluated, it must first be stored in a file that the model can read. The model will ask for the path to the file that is to bread, and then it will ask if you would like to see each individual text perplexity or the average perplexity of the texts within the file. <br/>
The perplexity value is logarithmic, where the further a value is from 0, the less probable it will be generated by the model. Laplace smoothing is used within this model for terms that do not appear in the vocabulary. 

```
Enter the file name of text for perplexity evaluation:
new_text.txt
File loaded.

Would you like to see all or the average? (all|avg)
all

...
Sentence 4:
 Hapless aegeon, whom the spital-house and ulcerous sores would cast the gorge at, this embalms and spices to the april day again. Come, thou shalt have to pay for it of us. Though now we must appear bloody and cruel, as, I think cassio's an honest man in it. I thank god and my cold blood, I am, necessity commands me name myself.
Perplexity: 0.8374 

Sentence 5:
 Advance your standards, and upon the grief of this suddenly died. Master constable, let these men be bound, and brought to leonato's: I will description the matter to you, good cornelius, and you must needs stay a time. I never prospered since I forswore myself at primero. Well, would demonstrate them now but goers backward.
Perplexity: 0.6687 
```
```
Would you like to see all or the average? (all|avg)
avg

Average Perplexity: 0.7851 

```
<br/>
<br/>

## Expansion

There is a lot of pontion expansions for this model. A different method of smoothing, such as back-off smoothing might yield more variation and decrease the range of perplexity within texts evaluated by the model. An option to include a specific term in a generated text would also be interesting. 

<br/>
<br/>

## Sample Data

The sample data for this project is from a shakespear corpus.
<br/>
<br/>
<br/>
<br/>

## Authors


* **King De Lany** - *Initial work* - [DelanyK](https://github.com/DelanyK)



## Acknowledgments

*This project was from the python for natural language processing course and the University of Stuttgart. 
