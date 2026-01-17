#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test online dictionary integration"""

from crossword_solver import CrosswordSolver
from online_dictionary import OnlineDictionary

print("=" * 60)
print("Testing Online Dictionary Integration")
print("=" * 60)

# Test pattern א_ג_ת with online dictionary
solver = CrosswordSolver()
online_dict = OnlineDictionary()

print("\n1. Testing Pattern: א_ג_ת")
print("-" * 60)
results = solver.find_matches(pattern="א_ג_ת")
print(f"Found {len(results)} matches:")
for i, result in enumerate(results, 1):
    print(f"\n  {i}. {result['word']}")
    print(f"     Source: {result['source']}")
    if result.get('description'):
        desc = result['description'][:100] + "..." if len(result.get('description', '')) > 100 else result.get('description', '')
        print(f"     Description: {desc}")
    if result.get('wiki_url'):
        print(f"     Wikipedia: {result['wiki_url']}")
    if result.get('wiktionary_url'):
        print(f"     Wiktionary: {result['wiktionary_url']}")

print("\n" + "=" * 60)
print("2. Testing Individual Word: אוגדת")
print("-" * 60)
word = "אוגדת"
online_result = online_dict.search_all_sources(word)
if online_result:
    print(f"✓ Found in {online_result['source']}")
    print(f"  URL: {online_result.get('url')}")
    if online_result.get('definition'):
        print(f"  Definition: {online_result['definition'][:150]}...")
else:
    print(f"✗ Not found in online dictionaries")
    print(f"  (This is OK - the word might not be in Wiktionary)")

print("\n" + "=" * 60)
print("3. Testing Common Word: שלום")
print("-" * 60)
word = "שלום"
online_result = online_dict.search_all_sources(word)
if online_result:
    print(f"✓ Found in {online_result['source']}")
    print(f"  URL: {online_result.get('url')}")
    if online_result.get('definition'):
        print(f"  Definition: {online_result['definition'][:150]}...")
else:
    print(f"✗ Not found in online dictionaries")

print("\n" + "=" * 60)
print("4. Testing Word Verification")
print("-" * 60)
test_words = ['שלום', 'אוגדת', 'ישראל', 'notarealword123']
for word in test_words:
    exists = online_dict.verify_word(word)
    status = "✓ EXISTS" if exists else "✗ NOT FOUND"
    print(f"  {word}: {status}")

print("\n" + "=" * 60)
print("Testing Complete!")
print("=" * 60)
print("\nNOTE: Online dictionary searches require internet access.")
print("If you see errors above, it's likely due to network restrictions.")
print("When deployed, the app will have full access to online dictionaries.")
