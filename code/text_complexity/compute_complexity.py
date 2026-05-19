import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import SyllableTokenizer

import warnings

# Ignore warnings related to non-english characters in the sonority hierarchy
warnings.filterwarnings(
    "ignore",
    message=".*sonority_hierarchy.*",
    category=UserWarning,
    module="nltk.tokenize.sonority_sequencing"
)

nltk.download('punkt_tab')


# only keep words, ignore punctuation
tokenizer = RegexpTokenizer(r'\w+')

# splits words into syllables
syllable_tokenizer = SyllableTokenizer()

def split_into_sentences(cleaned_up_text: str) -> list[str]:
    return nltk.sent_tokenize(cleaned_up_text)

def split_into_words(sentence: str) -> list[str]:
    return tokenizer.tokenize(sentence)

def split_into_syllables(word: str) -> list[str]:
    return syllable_tokenizer.tokenize(word)

def is_complex_word(syllables: list[str]) -> bool:
    return len(syllables) >= 3

# Calculate the complexity of a given text using the gunning fog index
def calculate_complexity_gunning_fog(number_of_sentences: int, number_of_words: int, number_of_complex_words: int) -> float:

    if number_of_sentences == 0 or number_of_words == 0:
        return -1.0  # Return -1 to indicate undefined complexity due to zero sentences or words

    # gunning fog index
    complexity = 0.4 * ((number_of_words / number_of_sentences) + (100 * (number_of_complex_words / number_of_words)))

    return complexity


def complexity_dictionary(text: str) -> dict:
    sentences = split_into_sentences(text)
    words = split_into_words(text)
    syllables = [split_into_syllables(word) for word in words]
    complex_words = [word for word in syllables if is_complex_word(word)]

    sentence_count = len(sentences)
    word_count = len(words)
    syllable_count = sum(len(syllable) for syllable in syllables)
    complex_word_count = len(complex_words)

    complexity = calculate_complexity_gunning_fog(sentence_count, word_count, complex_word_count)

    return {
        "sentence_count": sentence_count,
        "word_count": word_count,\
        "syllable_count": syllable_count,
        "complex_words_count": complex_word_count,
        "readability_index": complexity
    }