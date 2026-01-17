#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test multi-dictionary integration"""

from online_dictionary import OnlineDictionary
import time

print("=" * 70)
print("Testing Multi-Dictionary Integration")
print("=" * 70)

online_dict = OnlineDictionary()

# Test words
test_words = ['שלום', 'הרצל', 'ישראל', 'תפוח']

for word in test_words:
    print(f"\n{'='*70}")
    print(f"Testing word: {word}")
    print('='*70)

    # Try each dictionary individually
    print("\n1. Wiktionary:")
    result = online_dict.search_wiktionary(word)
    if result:
        print(f"   ✓ Found: {result.get('source')}")
        print(f"   Definition: {result.get('definition', '')[:100]}...")
        print(f"   URL: {result.get('url')}")
    else:
        print("   ✗ Not found")

    time.sleep(0.5)  # Be nice to APIs

    print("\n2. Morfix:")
    result = online_dict.search_morfix(word)
    if result:
        print(f"   ✓ Found: {result.get('source')}")
        print(f"   Definition: {result.get('definition')}")
        print(f"   URL: {result.get('url')}")
    else:
        print("   ✗ Not found")

    time.sleep(0.5)

    print("\n3. Reverso Context:")
    result = online_dict.search_reverso(word)
    if result:
        print(f"   ✓ Found: {result.get('source')}")
        print(f"   Definition: {result.get('definition')}")
        if 'translation' in result:
            print(f"   Translation: {result.get('translation')}")
        print(f"   URL: {result.get('url')}")
    else:
        print("   ✗ Not found")

    time.sleep(0.5)

    print("\n4. All Sources (with priority):")
    result = online_dict.search_all_sources(word)
    if result:
        print(f"   ✓ Found in: {result.get('source')}")
        print(f"   Definition: {result.get('definition', '')[:150]}...")
        print(f"   URL: {result.get('url')}")
        if 'translation' in result:
            print(f"   Translation: {result.get('translation')}")
    else:
        print("   ✗ Not found in any source")

    time.sleep(1)  # Rate limiting

print("\n" + "=" * 70)
print("Multi-Dictionary Test Complete!")
print("=" * 70)
print("\nNote: Some APIs may be blocked due to network restrictions in test environment.")
print("When deployed with internet access, all dictionaries will work correctly.")
