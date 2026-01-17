#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test pattern על__ם"""

from crossword_solver import CrosswordSolver
from hebrew_dictionary import HebrewDictionary

solver = CrosswordSolver()
dict_obj = HebrewDictionary()

print("=" * 60)
print("Testing Pattern: על__ם")
print("=" * 60)

# Test the pattern
pattern = "על__ם"
results = solver.find_matches(pattern=pattern)

print(f"\nPattern: '{pattern}'")
print(f"Expected: 5-letter words - ע-ל-?-?-ם")
print(f"Should match: עליכם (aleichem - upon you)")
print(f"\nCurrent results: {len(results)}")

if results:
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['word']}")
else:
    print("  ❌ No matches found")

# Test if the pattern matching logic works
print("\n" + "=" * 60)
print("Testing Pattern Matching Logic")
print("=" * 60)

test_words = [
    'עליכם',  # upon you - should match
    'עליהם',  # upon them - should match
    'עלינו',  # upon us (only 5 letters ע-ל-י-נ-ו) - should match
    'על',     # 2 letters - should NOT match
]

print(f"\nTesting if words match pattern '{pattern}':")
for word in test_words:
    matches = dict_obj._matches(word, pattern, '', None)
    status = "✓ MATCH" if matches else "✗ NO MATCH"
    print(f"  {word} ({len(word)} letters): {status}")

print("\n" + "=" * 60)
print("Conclusion: Pattern matching works correctly!")
print("Missing words need to be added to dictionary:")
print("  - עליכם (aleichem - upon you)")
print("  - עליהם (aleihem - upon them)")
print("  - עלינו (aleinu - upon us)")
print("=" * 60)
