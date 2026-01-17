#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test specific pattern א_ג_ת"""

from crossword_solver import CrosswordSolver
from hebrew_dictionary import HebrewDictionary

# Test the pattern matching
solver = CrosswordSolver()

print("=" * 60)
print("Testing Pattern: א_ג_ת")
print("=" * 60)

# Test with the specific pattern
pattern = "א_ג_ת"
results = solver.find_matches(pattern=pattern)

print(f"\nPattern: '{pattern}'")
print(f"Pattern length: {len(pattern)} letters")
print(f"Expected: Words with 'א' at position 1, 'ג' at position 3, 'ת' at position 5")
print(f"\nResults found: {len(results)}")

if results:
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['word']}")
        print(f"   Source: {result['source']}")
        if result['description']:
            print(f"   Description: {result['description'][:100]}...")
else:
    print("\n❌ No matches found in dictionary!")
    print("\nThis is because the built-in dictionary has limited words.")
    print("Words that would match 'א_ג_ת' pattern include:")
    print("  - אגרת (letter/correspondence) - but it's only 4 letters: א-ג-ר-ת")
    print("  - We need 5-letter words with pattern: א-?-ג-?-ת")

# Let's manually check if the pattern matching logic works
print("\n" + "=" * 60)
print("Testing Pattern Matching Logic")
print("=" * 60)

# Create test words
test_words = [
    'אגרת',      # 4 letters - should NOT match (wrong length)
    'אבגדת',     # 5 letters א-ב-ג-ד-ת - should match
    'אוגדת',     # 5 letters א-ו-ג-ד-ת - should match
    'אלגבת',     # 5 letters א-ל-ג-ב-ת - should match
    'שלום',      # doesn't match pattern
]

dict_obj = HebrewDictionary()

print(f"\nTesting pattern '{pattern}' against test words:")
for word in test_words:
    matches = dict_obj._matches(word, pattern, '', None)
    status = "✓ MATCH" if matches else "✗ NO MATCH"
    print(f"  {word} ({len(word)} letters): {status}")

# Add a test word to the dictionary and verify it works
print("\n" + "=" * 60)
print("Adding Test Word to Dictionary")
print("=" * 60)

test_word = 'אבגדת'  # This matches the pattern א_ג_ת
dict_obj.add_word(test_word)
print(f"Added '{test_word}' to dictionary")

# Now test again
results = solver.find_matches(pattern=pattern)
print(f"\nResults after adding test word: {len(results)}")
if results:
    for result in results:
        print(f"  - {result['word']}")
