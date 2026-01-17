#!/usr/bin/env python3
"""
Test script for the Hebrew Crossword Solver
"""

from crossword_solver import CrosswordSolver
import logging

logging.basicConfig(level=logging.INFO)

def test_pattern_matching():
    """Test basic pattern matching"""
    print("\n=== Testing Pattern Matching ===\n")

    solver = CrosswordSolver()

    # Test 1: Pattern with specific letters
    print("Test 1: Pattern '_ש_ל_ם'")
    results = solver.find_matches('_ש_ל_ם')
    print(f"Found {len(results)} matches:")
    for r in results[:5]:
        print(f"  - {r['word']} (Source: {r['source']})")

    # Test 2: Length-based search
    print("\nTest 2: 5-letter words")
    results = solver.find_matches('', '', 5)
    print(f"Found {len(results)} matches:")
    for r in results[:5]:
        print(f"  - {r['word']} (Source: {r['source']})")

    # Test 3: Known letters
    print("\nTest 3: Words containing 'ש' and 'ל'")
    results = solver.find_matches('', 'של', 5)
    print(f"Found {len(results)} matches:")
    for r in results[:5]:
        print(f"  - {r['word']} (Source: {r['source']})")

    # Test 4: Specific word pattern
    print("\nTest 4: Pattern 'של__'")
    results = solver.find_matches('של__')
    print(f"Found {len(results)} matches:")
    for r in results[:5]:
        print(f"  - {r['word']} (Source: {r['source']})")

    print("\n=== All Tests Completed ===\n")

if __name__ == '__main__':
    test_pattern_matching()
