import argparse
import os
import re

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
        for word, count in sorted(word_count.items(), key=lambda x: (x[1], x[0])):
            file_count.write(f"{count}, {word}\n")
        file_count.write("--------------------\n")
        file_count.write(f"{len(word_count)} Words\n")


def insert_word(word_count, word, count):
    if word in word_count:
        word_count[word] += count
    else:
        word_count[word] = count


def process_words(word_count):
    for word, count in sorted(word_count.items()):
        if word.count("'") > 1:
            del word_count[word]
        elif word.count("'") == 1:
            insert_word(word_count, word.split("'")[0], count)
            del word_count[word]
        elif re.search(r"[^a-z]", word):
            del word_count[word]


def calculate_total_word_count(word_count):
    return sum(word_count.values())


def main():
    parser = argparse.ArgumentParser(description="Process word list from a file.")
    parser.add_argument('input_file', type=str, help="Input file containing count, word pairs.")
    parser.add_argument('output_file_alpha', type=str, help="Output file to save the word list sorted alphabetically.")
    parser.add_argument('output_file_count', type=str, help="Output file to save the word list sorted by count and alphabetically if tied.")

    args = parser.parse_args()

    input_file = args.input_file
    output_file_alpha = args.output_file_alpha
    output_file_count = args.output_file_count

    if os.path.exists(input_file):
        word_count = load_words(input_file)
    else:
        print(f"Input file '{input_file}' does not exist.")
        return

    process_words(word_count)

    total_word_count = calculate_total_word_count(word_count)

    save_words(output_file_alpha, output_file_count, word_count)
    print(f"\nChanges saved to {output_file_alpha} (alphabetical) and {output_file_count} (by count)!")
    print(f"Total: {total_word_count} Words")


if __name__ == "__main__":
    main()
