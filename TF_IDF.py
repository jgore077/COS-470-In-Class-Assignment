import math
import os
import nltk
import numpy
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from regex import W
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE

nltk.download('punkt')


def read_files_to_dictionaries(directory_path):
    """
    This method will iterate on all the files in the input sub-directories and for each song calculates the term
    frequencies
    @param directory_path: directory path where all the directories of different genre are located
    @return: dictionary with song name as the key and the value as a dictionary (A). (A) is a dictionary with key
    representing the token and value being the frequency in the document. The second return type will give you genre for
    each song.
    """
    dic_song_term_frequency = {}
    dic_song_genre = {}
    for genre in os.listdir(directory_path):
        path = directory_path + genre
        for file in os.listdir(path):
            temp_dic = {}
            with open(path + "/" + file, 'r') as rfile:
                for line in rfile:
                    current_line = line.strip()
                    ############################
                    # pre-process each line if you want to and save the results in current_line
                    # YOUR CODE
                    ############################

                    token_list = word_tokenize(current_line)
                    for token in token_list:
                        # Update frequency for existing term or add a new term with frequency 1
                        temp_dic[token] = temp_dic.get(token, 0) + 1
            song_name = file.split(".")[0]
            dic_song_term_frequency[song_name] = temp_dic
            dic_song_genre[song_name] = genre
    return dic_song_term_frequency, dic_song_genre


def get_TF_values(dic_song_term_frequency):
    """
    This method takes in token frequency per song as the input and returns TF per token/song
    @param dic_song_term_frequency: song name as key and dictionary A as value. In A, keys are the tokens with their
    frequencies as the values
    @return: Dictionary with song names as keys, and TF-Values as values. These values are also a dictionary of token as
    the keys and their TFs as values
    """
    dic_tf_per_song = {}
    for song in dic_song_term_frequency:
        dic_tf_per_song[song]={}
        for word in dic_song_term_frequency[song].keys():
            dic_tf_per_song[song][word]= math.log10(dic_song_term_frequency[song][word]+1)

    return dic_tf_per_song


def get_IDF_values(dic_song_term_frequency):
    """
    This method calculates the IDF values for each token
    @param dic_song_term_frequency: song name as key and dictionary A as value. In A, keys are the tokens with their
    frequencies as the values
    @return: Dictionary with tokens as the keys and IDF values as values
    """
    dic_idf_values = {}
    num_songs = len(dic_song_term_frequency.keys())
   
    for song in dic_song_term_frequency:
        # Sorting terms
        # dic_song_term_frequency[song] ={key: value for key, value in sorted(dic_song_term_frequency[song].items())}
        for term in dic_song_term_frequency[song].keys():
            if dic_idf_values.get(term)==None:
                dic_idf_values[term]=1
                continue
            dic_idf_values[term]+=1
        

    for term in dic_idf_values:
        dic_idf_values[term]= math.log10(num_songs/dic_idf_values[term])
    return dic_idf_values


def song_to_vector(dic_tf_per_song, dic_idf):
    """
    This method will extract vector representation (based on TF-IDF) for each song
    @param dic_tf_per_song: TF dictionary with song name as key and dictionary of (token:TF) as value
    @param dic_idf: IDF dictionary with token as key and its IDF as value
    @return: dictionary of (song name, vector)
    """
    song_to_vec = {}
    for song, tf_dict in dic_tf_per_song.items():
        song_vector = numpy.zeros(len(dic_idf))

        for token, tf in tf_dict.items():
            if token in dic_idf: 
                tf_idf = tf * dic_idf[token]
        
                index = list(dic_idf.keys()).index(token)
                song_vector[index] = tf_idf
        
        song_to_vec[song] = song_vector
    return song_to_vec


def cosine_sim(numpy_vec1, numpy_vec2):
    """
    Using sklearn library, this method calculates the cosine similarity between two numpy vectors
    @param numpy_vec1: vector 1
    @param numpy_vec2: vector 2
    @return: cosine similarity
    """

    return cosine_similarity(numpy_vec1, numpy_vec2)


def test_cosine(dic_song_vectors):
    print(cosine_sim(dic_song_vectors["Till I Collapse"].reshape(1, -1), dic_song_vectors["Rap God"].reshape(1, -1)))
    print(
        cosine_sim(dic_song_vectors["Till I Collapse"].reshape(1, -1), dic_song_vectors["Billie Jean"].reshape(1, -1)))


def test_tsne_plot(dic_song_vectors, dic_song_genre):
    lst_song_names = []
    lst_data = []
    colors = []
    tsne = TSNE(n_components=2)
    for song in list(dic_song_vectors.keys()):
        lst_song_names.append(song)
        lst_data.append(dic_song_vectors[song])
        color = get_color(dic_song_genre[song])
        colors.append(color)
    data = numpy.array(lst_data)
    vectors = tsne.fit_transform(data)
    ax = plt.axes()
    ax.set_facecolor("black")
    for i in range(len(vectors)):
        plt.scatter(vectors[i][0], vectors[i][1], color=colors[i])

    # Adding song names; this can make the plot messy; you can choose a fewer songs and uncomment this code
    # for i, txt in enumerate(lst_song_names):
    #     plt.annotate(txt, (vectors[i][0], vectors[i][1]))
    plt.show()


def get_color(genre):
    """
    Assigns a color to each genre
    @param genre: song genre
    @return: genre's color
    """
    if genre == "Blues":
        color = 'blue'
    elif genre == "Country":
        color = 'red'
    elif genre == "Metal":
        color = 'gray'
    elif genre == "Pop":
        color = 'yellow'
    elif genre == "Rap":
        color = 'green'
    elif genre == "Rock":
        color = 'purple'
    return color


def main():
    # Path to the root Lyrics files
    path_to_root_dir = r"./Lyrics"
    dic_song_dic_term_count, dic_song_genre = read_files_to_dictionaries(path_to_root_dir + "/")
    dic_song_dic_term_frequency = get_TF_values(dic_song_dic_term_count)
    print(dic_song_dic_term_frequency)
    dic_term_idfs = get_IDF_values(dic_song_dic_term_count)
    dic_song_vectors = song_to_vector(dic_song_dic_term_frequency, dic_term_idfs)



    test_cosine(dic_song_vectors)
    # test_tsne_plot(dic_song_vectors, dic_song_genre)


if __name__ == '__main__':
    main()
