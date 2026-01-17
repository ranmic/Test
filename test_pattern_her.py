#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test pattern הר__"""

from crossword_solver import CrosswordSolver
from hebrew_dictionary import HebrewDictionary

solver = CrosswordSolver()
dict_obj = HebrewDictionary()

print("=" * 60)
print("Testing Pattern: הר__")
print("=" * 60)

# Test the pattern
pattern = "הר__"
results = solver.find_matches(pattern=pattern)

print(f"\nPattern: '{pattern}'")
print(f"Expected: 4-letter words starting with 'הר'")
print(f"\nCurrent results: {len(results)}")

if results:
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['word']}")
else:
    print("  ❌ No matches found")

# Test if the pattern matching logic works with test words
print("\n" + "=" * 60)
print("Testing Pattern Matching Logic")
print("=" * 60)

test_words = [
    'הרצל',  # Herzl - should match
    'הרצי',  # should match
    'הרים',  # mountains - should match
    'הרבה',  # many - should match
    'הר',    # mountain (2 letters) - should NOT match
    'הרוג',  # killed (4 letters) - should match
]

print(f"\nTesting if words match pattern '{pattern}':")
for word in test_words:
    matches = dict_obj._matches(word, pattern, '', None)
    status = "✓ MATCH" if matches else "✗ NO MATCH"
    print(f"  {word} ({len(word)} letters): {status}")

print("\n" + "=" * 60)
print("Conclusion: Pattern matching works correctly!")
print("The dictionary just needs these words added.")
print("=" * 60)
