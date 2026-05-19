
from code.text_complexity.compute_complexity import calculate_complexity_gunning_fog, is_complex_word, split_into_sentences, split_into_syllables, split_into_words


# example_string = "I think it should be fixed on either UTC standard or UTC+1 year around, with the current zone offsets.\n\nMoving timescales add a lot of complexity to the implementation of timekeeping systems and have [dubious value]( \n\nI think seasonal shifting time made sense in the pre-electric past, when timekeeping was more flexible and artificial light was inefficient and often dangerous. \n\nNow we have machines that work easily with simple timekeeping rules, and it's more beneficial to spend a small amount on energy for lighting, and save the larger cost of engineering things to work with the complex timekeeping rules, as well as saving the irritation to humans.\n\nLighting has gotten much more efficient over time; we can squeeze out a lot more photons per unit of energy from a 2012 CFL or LED than a candle could in 1780, or a lightbulb could in 1950. \n\nThere's a lot of room for improvement in how we use lights as well; as lighting control gets more intelligent, there will be a lot of savings from not illuminating inactive spaces constantly.\n\ntl;dr: Shifting seasonal time is no longer worth it."
example_string = "Theres an entire small town under the lake by my house. I'll try and get up there soon to take pictures. the lake should be pretty empty right now. Usually is at the end of summer and before rainy season. It's actually pretty close to Shaver lake. Lake Kaweah in CA. I don't remember the story well but they either made the lake or made it bigger and the town had to be moved. didnt take down the buildings and once in a while you can see them sticking up a bit out of the water. I think the area use to just be a river. a decent part of the Central Valley use to be a lake because of all of the rivers flowing in. Shaver might be from this too. blocking off the rivers to dry up the valley. Not sure though. \n this is what it use to be. Tulare Lake. Biggest lake on the west side of the Mississippi river. Now the valley is dried up but has some of the best soil for crops in the world. \n\nTL;DR: I'll try and get some similar shots from lake Kaweah next time I'm up there because there is an entire small town under the lake. "

sentences = split_into_sentences(example_string)
words = split_into_words(example_string)
syllables = [split_into_syllables(word) for word in words]

whole_syllables = ["".join(inner) for inner in syllables]

# words = [split_into_words(sentence) for sentence in sentences]
# syllables = [split_into_syllables(word) for sentence in words for word in sentence]
complex_words = [word for word in syllables if is_complex_word(word)]
complex_whole_words = ["".join(inner) for inner in complex_words]

complex_word_count = len(complex_words)
sentence_count = len(sentences)
word_count = len(words)
syllable_count = sum(len(syllable) for syllable in syllables)

debug_syllable_count = 0

for syllable in syllables:
    debug_syllable_count += len(syllable)

print("len syllables:", len(syllables))
print("Debug syllable count:", debug_syllable_count)

complexity = calculate_complexity_gunning_fog(sentence_count, word_count, complex_word_count)

print("Sentences:", sentences)
print("Words:", words)
# print("Syllables:", syllables)
print("Whole Syllables:", whole_syllables)
print("Complex Words:", complex_whole_words)
print("Number of Complex Words:", complex_word_count)
print("------------------------------")
print("Number of Sentences:", sentence_count, "Number of Words:", word_count, "Number of Complex Words:", complex_word_count, "Number of Syllables:", syllable_count)
print("Complexity (Gunning Fog Index):", complexity)