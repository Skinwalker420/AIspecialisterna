from nltk.tokenize import sent_tokenize
import nltk.data
import json

def tokenize(text, filename):
        filePath = "/home/tempvm/Dumps/Sentence.json"
        tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
        sentences = sent_tokenize(text)
        print(sentences)
        # Output the sentences
        with open(filePath, 'w') as json_file:
                json.dump(sentences, json_file, indent=4)
                print(f"Data successfully saved to {filePath}")
