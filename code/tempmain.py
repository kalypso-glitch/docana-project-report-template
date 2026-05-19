from temp import calculate_complexity, is_complex_word, split_into_sentences, split_into_syllables, split_into_words

sentences = split_into_sentences("I think it should be fixed on either UTC standard or UTC+1 year around, with the current zone offsets.\n\nMoving timescales add a lot of complexity to the implementation of timekeeping systems and have [dubious value]( \n\nI think seasonal shifting time made sense in the pre-electric past, when timekeeping was more flexible and artificial light was inefficient and often dangerous. \n\nNow we have machines that work easily with simple timekeeping rules, and it's more beneficial to spend a small amount on energy for lighting, and save the larger cost of engineering things to work with the complex timekeeping rules, as well as saving the irritation to humans.\n\nLighting has gotten much more efficient over time; we can squeeze out a lot more photons per unit of energy from a 2012 CFL or LED than a candle could in 1780, or a lightbulb could in 1950. \n\nThere's a lot of room for improvement in how we use lights as well; as lighting control gets more intelligent, there will be a lot of savings from not illuminating inactive spaces constantly.\n\ntl;dr: Shifting seasonal time is no longer worth it.")
words = [split_into_words(sentence) for sentence in sentences]
syllables = [split_into_syllables(word) for sentence in words for word in sentence]
complex_words = [word for word in syllables if is_complex_word(word)]

complex_word_count = len(complex_words)
sentence_count = len(sentences)
word_count = sum(len(sentence) for sentence in words)

complexity = calculate_complexity(sentence_count, word_count, complex_word_count)

print("Sentences:", sentences)
print("Words:", words)
print("Syllables:", syllables)
print("Complex Words:", complex_words)
print("Number of Complex Words:", complex_word_count)
print("------------------------------")
print("Number of Sentences:", sentence_count, "Number of Words:", word_count, "Number of Complex Words:", complex_word_count)
print("Complexity (Gunning Fog Index):", complexity)