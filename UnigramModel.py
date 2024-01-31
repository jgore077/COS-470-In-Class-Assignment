import os
import nltk
import math

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
    total = 0
    
    for t in dic_term_frequency.values():
        total += t
    
    for t in dic_term_frequency:
        dic_term_prob[t] = dic_term_frequency[t] / total
        

    return dic_term_prob


def calculate_probability(dic_term_prob, input_text):
    prob = 0.0

    input_tokens = [word.lower() for word in word_tokenize(input_text) if not word.lower() in stop_words and len(word)>1]

    for t in input_tokens:
        if t in dic_term_prob:
            prob += math.log(dic_term_prob[t])
    
    return prob

def main():
    input_text = "I am a very bad, bad sad man. My wife left me and I drink beer."

    genres = ["Blues", "Country", "Metal", "Pop", "Rap", "Rock"]
    genreprobdict = []

    for genre in genres:
        worddict=read_files_in_directory(genre)
        probdict=freq_to_prob(worddict)
        genreprobdict.append(probdict)


    smallestindex = 0
    smallestprob = -100000

    for i, v in enumerate(genreprobdict):
        t = calculate_probability(v, input_text)
        if t > smallestprob:
            smallestindex = i
            smallestprob = t

    print(genres[smallestindex], smallestprob)
    
    return

main()