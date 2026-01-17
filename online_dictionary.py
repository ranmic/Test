"""
Online Hebrew Dictionary Integration
Searches multiple online sources for Hebrew words
"""

import requests
import logging
from typing import List, Dict, Optional
import re

logger = logging.getLogger(__name__)

class OnlineDictionary:
    """Search online Hebrew dictionaries for words"""

    def __init__(self):
        self.timeout = 5  # seconds
        self.cache = {}  # Simple in-memory cache
        # Add proper User-Agent header for API requests
        self.headers = {
            'User-Agent': 'HebrewCrosswordSolver/1.0 (https://github.com/ranmic/Test; Educational Project)',
            'Accept': 'application/json'
        }

    def search_wiktionary(self, word: str) -> Optional[Dict]:
        """
        Search Hebrew Wiktionary for a word

        Args:
            word: Hebrew word to search

        Returns:
            Dict with word info or None
        """
        try:
            # Use Wiktionary API
            url = "https://he.wiktionary.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'titles': word,
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if page_id != '-1':  # Page exists
                    return {
                        'word': word,
                        'definition': page_data.get('extract', ''),
                        'source': 'Wiktionary',
                        'url': f'https://he.wiktionary.org/wiki/{word}'
                    }

            return None

        except Exception as e:
            logger.debug(f"Wiktionary search error for '{word}': {e}")
            return None

    def search_all_sources(self, word: str) -> Optional[Dict]:
        """
        Search all available online sources

        Args:
            word: Hebrew word to search

        Returns:
            Dict with word info from first successful source
        """
        # Check cache first
        if word in self.cache:
            logger.debug(f"Cache hit for '{word}'")
            return self.cache[word]

        # Try Wiktionary
        result = self.search_wiktionary(word)

        if result:
            self.cache[word] = result
            return result

        return None

    def search_pattern_in_hebrew_words(self, pattern: str, length: Optional[int] = None) -> List[str]:
        """
        Search for words matching a pattern from online sources

        This is a more advanced feature that queries online word lists

        Args:
            pattern: Pattern with _ for unknown letters
            length: Required word length

        Returns:
            List of matching Hebrew words
        """
        matches = []

        try:
            # Use Hebrew word frequency list or dictionary API
            # For now, we'll use a simple approach with common Hebrew words

            # Convert pattern to regex
            if pattern:
                regex_pattern = pattern.replace('_', '.')
                regex = re.compile(f'^{regex_pattern}$')

                # You could query an API here for Hebrew words
                # For now, this is a placeholder
                logger.debug(f"Pattern search: {pattern}")

        except Exception as e:
            logger.error(f"Error in online pattern search: {e}")

        return matches

    def get_word_frequency_list(self, limit: int = 1000) -> List[str]:
        """
        Get a list of common Hebrew words from online sources

        This could pull from:
        - Hebrew Wikipedia word frequency lists
        - Open Hebrew word databases
        - Academic resources

        Args:
            limit: Maximum number of words to return

        Returns:
            List of common Hebrew words
        """
        common_words = []

        try:
            # This is a placeholder - in production you'd query actual APIs
            # Possible sources:
            # 1. Hebrew Wikipedia dumps
            # 2. Open Hebrew word lists on GitHub
            # 3. Academic linguistic databases

            logger.info("Loading common Hebrew words from online sources...")

        except Exception as e:
            logger.error(f"Error loading word frequency list: {e}")

        return common_words

    def verify_word(self, word: str) -> bool:
        """
        Verify if a word exists in Hebrew dictionaries

        Args:
            word: Word to verify

        Returns:
            True if word exists, False otherwise
        """
        result = self.search_all_sources(word)
        return result is not None

    def get_definition(self, word: str) -> Optional[str]:
        """
        Get definition for a Hebrew word

        Args:
            word: Hebrew word

        Returns:
            Definition string or None
        """
        result = self.search_all_sources(word)
        if result:
            return result.get('definition')
        return None
