import nltk
import sys
import os
from nltk.tokenize import word_tokenize
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dict_filename_content = {}
    for filename in os.listdir(directory):
        file = open(os.path.join(directory, filename), "r")
        content = file.read()
        dict_filename_content[filename] = content
    
    return dict_filename_content

    
def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenized_words = nltk.word_tokenize(document.lower())
    stop_words = set(nltk.corpus.stopwords.words("english"))
    punctuation = set(string.punctuation)  

    # Filter out all words that are stopwords or punctuation marks
    words = [
        word for word in tokenized_words 
        if word not in punctuation
        and word not in stop_words
    ]

    return words 


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_idf = {}
    frequencies = {}
    nb_documents = len(documents.keys())

    # Populating the frequencies dict for each word
    for document in documents.keys():
        for word in documents[document]:
            if word not in frequencies:
                frequencies[word] = 1
            else:
                frequencies[word] += 1
            
    for word in frequencies.keys():
        idf = math.log(nb_documents / frequencies[word])
        word_idf[word] = idf
    
    return word_idf
            

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranks_files = {}

    for file, words in files.items():
        # Calculate the tf-idf score for the query terms present in the file
        tfidf = sum(words.count(word) * idfs[word] for word in query if word in words)

        # Skip files with a tf-idf score of 0
        if tfidf == 0:
            continue

        ranks_files[file] = tfidf

    # Sort the files by their tf-idf score in ascending order
    sorted_files = sorted(ranks_files.items(), key=lambda x: x[1])

    # Return the top n files with the highest tf-idf score
    return [file[0] for file in sorted_files[:n]]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks_sentence = {}

    for sentence, words in sentences.items():
        # The get() method returns 0 if the word is not found in idfs, preventing KeyError
        idf = sum(idfs.get(word, 0) for word in query if word in words)

        # Calculate the number of query words that match words in the current sentence
        num_match = sum(1 for word in query if word in words)

        query_density = num_match / len(words)

        ranks_sentence[sentence] = {'idf': idf, 'query_density': query_density}

    # Sort sentences by their IDF and query density in descending order
    sorted_sentence_idfs = sorted(ranks_sentence.items(), key=lambda x: (x[1]['idf'], x[1]['query_density']), reverse=True)

    # Return top n sentences with highest IDF and query density
    return [sentence[0] for sentence in sorted_sentence_idfs[:n]]


if __name__ == "__main__":
    main()
