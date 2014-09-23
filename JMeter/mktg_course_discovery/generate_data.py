#!/usr/bin/env python
"""
Generate data for the marketing load test.

* Randomize URLs / search terms.
* Generate "autocomplete" search terms, using partial search terms.
* Introduce typographical errors into the search terms.

"""
import math
import random


URLS = [
    ("input/primary_urls.csv", "test/primary_urls.csv"),
    ("input/secondary_urls.csv", "test/secondary_urls.csv"),
]

AUTOCOMPLETE = [
    ("input/school_search.csv", "test/school_autocomplete.csv"),
    ("input/subject_search.csv", "test/subject_autocomplete.csv"),
    ("input/course_search.csv", "test/course_autocomplete.csv"),
]

SEARCH_OUTPUT = "test/all_queries.csv"

TYPO_LETTERS = ['a', 'b', 'c', 'g', 'h', 'k']

NUM_COPIES = 50
TYPO_RATE = 0.2


def randomize(input_list, output_filename):
    # Clear the file
    with open(output_filename, 'w') as output_file:
        output_file.write('')

    for output_num in range(NUM_COPIES):
        random.shuffle(input_list)
        with open(output_filename, 'a') as output_file:
            output_file.write('\n'.join(input_list))

            if output_num < (NUM_COPIES - 1):
                output_file.write('\n')


def partial_terms(terms):
    partial_terms = []
    for term in terms:
        if term:
            for idx in range(1, len(term) + 1):
                partial_terms.append(term[0:idx])
    return partial_terms


def add_typos(terms):
    num_typos = int(math.ceil(TYPO_RATE * len(terms)))
    typo_terms = random.sample(terms, num_typos)

    all_terms = terms[:]
    for term in typo_terms:
        insert_idx = random.randint(0, len(term))
        all_terms.append(term[0:insert_idx] + random.choice(TYPO_LETTERS) + term[insert_idx:])

    return all_terms


def load_csv(file_handle):
    return file_handle.read().split('\n')[:-1]


def main():
    # Randomize the URLs
    for (input_filename, output_filename) in URLS:
        with open(input_filename) as urls_file:
            randomize(load_csv(urls_file), output_filename)

    # Randomize search terms (autocomplete)
    all_terms = []
    for (input_filename, output_filename) in AUTOCOMPLETE:
        with open(input_filename) as search_file:
            terms = add_typos(load_csv(search_file))
            all_terms.extend(terms)
            randomize(partial_terms(terms), output_filename)

    # Main search includes everything
    randomize(all_terms, SEARCH_OUTPUT)


if __name__ == "__main__":
    main()
