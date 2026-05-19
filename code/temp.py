import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import SyllableTokenizer

nltk.download('punkt_tab')


# only keep words, ignore punctuation
tokenizer = RegexpTokenizer(r'\w+')

# splits words into syllables
syllable_tokenizer = SyllableTokenizer()

def cleanup_text(text):
    return text

def split_into_sentences(cleaned_up_text):
    return nltk.sent_tokenize(cleaned_up_text)

def split_into_words(sentence):
    return tokenizer.tokenize(sentence)

def split_into_syllables(word):
    return syllable_tokenizer.tokenize(word)

# def count_syllables(word):
    # return len(split_into_syllables(word))

def is_complex_word(syllables):
    return len(syllables) >= 3

# def count_complex_words(words):
    # complex_words = [word for word in words if is_complex_word(word)]
    # return len(complex_words)

# Calculate the complexity of a given text using the gunning fog index
def calculate_complexity(number_of_sentences, number_of_words, number_of_complex_words):

    if number_of_sentences == 0 or number_of_words == 0:
        return 0

    # gunning fog index
    complexity = 0.4 * ((number_of_words / number_of_sentences) + (100 * (number_of_complex_words / number_of_words)))

    return complexity