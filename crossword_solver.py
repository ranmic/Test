import re
from typing import List, Dict, Optional
from hebrew_dictionary import HebrewDictionary
from wikipedia_search import WikipediaSearch
import logging

logger = logging.getLogger(__name__)

class CrosswordSolver:
    def __init__(self):
        self.dictionary = HebrewDictionary()
        self.wiki_search = WikipediaSearch()

    def find_matches(self, pattern: str, known_letters: str = '', length: Optional[int] = None) -> List[Dict]:
        """
        Find words that match the given pattern and constraints.

        Args:
            pattern: Pattern with _ for unknown letters (e.g., "_ש_ל_ם")
            known_letters: Letters that must be in the word
            length: Required word length

        Returns:
            List of matching words with their sources and descriptions
        """
        results = []
        seen_words = set()

        # Get pattern length if specified
        if pattern and '_' in pattern:
            pattern_length = len(pattern)
        else:
            pattern_length = length

        # Search in dictionary
        try:
            dict_results = self.dictionary.search(pattern, known_letters, pattern_length)
            for word in dict_results:
                if word not in seen_words:
                    results.append({
                        'word': word,
                        'source': 'Hebrew Dictionary',
                        'description': None,
                        'wiki_url': None
                    })
                    seen_words.add(word)
        except Exception as e:
            logger.error(f"Error searching dictionary: {e}")

        # Search in Wikipedia for additional context
        try:
            # Get top results from dictionary to check Wikipedia
            top_words = [r['word'] for r in results[:10]]
            for word in top_words:
                wiki_result = self.wiki_search.search(word)
                if wiki_result:
                    # Update the result with Wikipedia info
                    for result in results:
                        if result['word'] == word:
                            result['description'] = wiki_result.get('description')
                            result['wiki_url'] = wiki_result.get('url')
                            result['source'] = 'Dictionary + Wikipedia'
                            break

            # Also search Wikipedia directly with pattern
            if pattern and not pattern.startswith('_'):
                wiki_results = self.wiki_search.search_pattern(pattern, pattern_length)
                for wiki_word in wiki_results:
                    if wiki_word['word'] not in seen_words:
                        if self._matches_pattern(wiki_word['word'], pattern, known_letters):
                            results.append({
                                'word': wiki_word['word'],
                                'source': 'Wikipedia',
                                'description': wiki_word.get('description'),
                                'wiki_url': wiki_word.get('url')
                            })
                            seen_words.add(wiki_word['word'])

        except Exception as e:
            logger.error(f"Error searching Wikipedia: {e}")

        # Sort by source priority (Dictionary + Wikipedia first)
        results.sort(key=lambda x: (
            0 if x['source'] == 'Dictionary + Wikipedia' else
            1 if x['source'] == 'Hebrew Dictionary' else 2
        ))

        return results[:50]  # Limit to 50 results

    def _matches_pattern(self, word: str, pattern: str, known_letters: str) -> bool:
        """
        Check if a word matches the given pattern and known letters.

        Args:
            word: The word to check
            pattern: Pattern with _ for unknown letters
            known_letters: Letters that must be in the word

        Returns:
            True if the word matches, False otherwise
        """
        # Check pattern match
        if pattern:
            if len(word) != len(pattern):
                return False

            for i, p in enumerate(pattern):
                if p != '_' and p != word[i]:
                    return False

        # Check known letters
        if known_letters:
            for letter in known_letters:
                if letter not in word:
                    return False

        return True
