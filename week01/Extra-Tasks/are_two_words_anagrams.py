"""

Are two words anagrams?

For anagrams, check here - https://en.wikipedia.org/wiki/Anagram

For example, listen and silent are anagrams.

The program should read two words from the standard input and output:

ANAGRAMS if the words are anagrams of each other
NOT ANAGRAMS if the two words are not anagrams of each other
Consider lowering the case of the two words since the case does not matter. SILENT and listen are also anagrams.

Examples

Input:
TOP_CODER COTO_PRODE
Output:
NOT ANAGRAMS

Input:
kilata cvetelina_yaneva
Output:
NOT ANAGRAMS
Also, should not make songs together.

Input:
BRADE BEARD
Output:
ANAGRAMS

"""
word_1, word_2 = input().lower().split()
print("ANAGRAMS") if set(word_1) == set(word_2) else print("NOT ANAGRAMS")