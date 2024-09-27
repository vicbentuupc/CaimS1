import argparse
import os
import re
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('omw-1.4')  # For additional language support (optional)
nltk.download('punkt')     # To use word tokenization if needed

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def load_words(filename):
    word_count = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if re.match(r'^\d+, [a-zA-Z]+$', line):
                count, word = line.split(', ')
                word = word.lower()
                count = int(count)
                if word in word_count:
                    word_count[word] += count
                else:
                    word_count[word] = count
    return word_count


def save_words(output_filename_alpha, output_filename_count, word_count):
    with open(output_filename_alpha, 'w') as file_alpha:
        for word in sorted(word_count.keys()):
            file_alpha.write(f"{word_count[word]}, {word}\n")
        file_alpha.write("--------------------\n")
        file_alpha.write(f"{len(word_count)} Words\n")
    
    with open(output_filename_count, 'w') as file_count:
        for word, count in sorted(word_count.items(), key=lambda x: (-x[1], x[0])):
            file_count.write(f"{count}, {word}\n")
        file_count.write("--------------------\n")
        file_count.write(f"{len(word_count)} Words\n")


def insert_word(word_count, word, count):
    if word in word_count:
        word_count[word] += count
    else:
        word_count[word] = count


def process_words(word_count, stem_word_count, lemm_word_count):
    for word, count in sorted(word_count.items()):
        initial_word = word
        if word.count("'") > 1:
            del word_count[word]
            del stem_word_count[word]
            del lemm_word_count[word]
        elif word.count("'") == 1:
            word = word.split("'")[0]
            del word_count[word]
            insert_word(word_count, word, count)

        if re.search(r"[^a-z]", word):
            del word_count[word]
        
        lemm_word, stem_word = lemmatizer.lemmatize(word), stemmer.stem(word) 
        if lemm_word != initial_word:
            insert_word(lemm_word_count, lemm_word, count)
            del lemm_word_count[initial_word]
        if stem_word != initial_word:
            insert_word(stem_word_count, stem_word, count)
            del stem_word_count[initial_word]


def calculate_total_word_count(word_count):
    return sum(word_count.values())


def main():
    parser = argparse.ArgumentParser(description="Process word list from a file.")
    parser.add_argument('input_file', type=str, help="Input file containing count, word pairs.")
    parser.add_argument('output_dir', type=str, help="Output file to save the word list sorted alphabetically.")
    parser.add_argument('name', type=str, default="output", help="Name of the output files.")

    args = parser.parse_args()

    input_file = args.input_file
    output_dir = args.output_dir
    name = args.name

    if os.path.exists(input_file):
        normal_word_count = load_words(input_file)
    else:
        print(f"Input file '{input_file}' does not exist.")
        return

    lemming_word_count = normal_word_count.copy()
    stemming_word_count = normal_word_count.copy()
    process_words(normal_word_count, stemming_word_count, lemming_word_count)

    save_words(os.path.join(output_dir, f"alpha_normal_preprocessed_{name}.txt"), os.path.join(output_dir, f"count_normal_preprocessed_{name}.txt"), normal_word_count)
    save_words(os.path.join(output_dir, f"alpha_stemming_preprocessed_{name}.txt"), os.path.join(output_dir, f"count_stemming_preprocessed_{name}.txt"), stemming_word_count)
    save_words(os.path.join(output_dir, f"alpha_lemming_preprocessed_{name}.txt"), os.path.join(output_dir, f"count_lemming_preprocessed_{name}.txt"), lemming_word_count)

    print(f"Total words in normal dictionary: {calculate_total_word_count(normal_word_count)}")
    print(f"Total words in stemming dictionary: {calculate_total_word_count(stemming_word_count)}")
    print(f"Total words in lemming dictionary: {calculate_total_word_count(lemming_word_count)}")



if __name__ == "__main__":
    main()
