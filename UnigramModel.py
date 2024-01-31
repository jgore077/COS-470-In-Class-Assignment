import os
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words=set(stopwords.words('english'))

# might be useful?
from collections import Counter


def read_files_in_directory(directory_path):
    # key: tokens value: their frequency in all songs belonging to a genre
    dic_term_frequency = {}

    for file in os.listdir(directory_path):
        with open(directory_path+'/'+file, 'r') as rfile:
            for line in rfile:
                current_line = line.strip()
                # pre-process each line if you want to and save the results in current_line
                # YOUR CODE

                tokens = [word.lower() for word in word_tokenize(current_line) if not word.lower() in stop_words and len(word)>1]

                # process the tokens and update your dictionary
                # YOUR CODE
                for token in tokens:
                    if token not in dic_term_frequency:
                        dic_term_frequency[token] = 1
                    else:
                        dic_term_frequency[token] += 1

    return dic_term_frequency


def freq_to_prob(dic_term_frequency):
    dic_term_prob = {}
    # YOUR CODE
    # Convert the frequencies to probabilities

    return dic_term_prob


def calculate_probability(dic_term_prob, input_text):
    prob = 0.0

    return prob


def main():
    worddict=read_files_in_directory('Blues')
    print(worddict)
    return

main()