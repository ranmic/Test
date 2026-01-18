#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test pattern ____ב___"""

from crossword_solver import CrosswordSolver
from hebrew_dictionary import HebrewDictionary

solver = CrosswordSolver()
dict_obj = HebrewDictionary()

print("=" * 60)
print("Testing Pattern: ____ב___")
print("=" * 60)

# Test the pattern
pattern = "____ב___"
results = solver.find_matches(pattern=pattern)

print(f"\nPattern: '{pattern}'")
print(f"Length: {len(pattern)} letters")
print(f"Expected: 9-letter words with 'ב' at position 5")
print(f"\nResults found: {len(results)}")

if results:
    print("\nMatching words:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['word']}")
        print(f"     Source: {result['source']}")
        if result.get('description'):
            desc = result['description'][:80] + "..." if len(result.get('description', '')) > 80 else result.get('description', '')
            print(f"     Description: {desc}")
else:
    print("  ❌ No matches found")

# Let's check what 9-letter words we have in the dictionary
print("\n" + "=" * 60)
print("All 9-letter words in dictionary:")
print("=" * 60)

all_words = sorted(dict_obj.words, key=len, reverse=True)
nine_letter_words = [w for w in all_words if len(w) == 9]

print(f"\nFound {len(nine_letter_words)} words with 9 letters:")
if nine_letter_words:
    for i, word in enumerate(nine_letter_words[:20], 1):  # Show first 20
        has_bet_at_5 = "✓ MATCHES PATTERN" if len(word) == 9 and word[4] == 'ב' else ""
        print(f"  {i}. {word} {has_bet_at_5}")
    if len(nine_letter_words) > 20:
        print(f"  ... and {len(nine_letter_words) - 20} more")
else:
    print("  (No 9-letter words in dictionary)")

# Show word length distribution
print("\n" + "=" * 60)
print("Word Length Distribution in Dictionary:")
print("=" * 60)

from collections import Counter
length_counts = Counter(len(w) for w in dict_obj.words)
for length in sorted(length_counts.keys()):
    print(f"  {length} letters: {length_counts[length]} words")

print(f"\nTotal words: {len(dict_obj.words)}")
