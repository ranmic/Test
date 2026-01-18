"""
Online Hebrew Dictionary Integration
Searches multiple online sources for Hebrew words including:
- Hebrew Wiktionary
- Morfix (Hebrew-English dictionary)
- Reverso Context
- Academy of the Hebrew Language
- GitHub Hebrew word frequency lists
"""

import requests
import logging
from typing import List, Dict, Optional
import re
import json

logger = logging.getLogger(__name__)

class OnlineDictionary:
    """Search online Hebrew dictionaries for words"""

    def __init__(self):
        self.timeout = 5  # seconds
        self.cache = {}  # Simple in-memory cache
        # Add proper User-Agent header for API requests
        self.headers = {
            'User-Agent': 'HebrewCrosswordSolver/1.0 (https://github.com/ranmic/Test; Educational Project)',
            'Accept': 'application/json',
            'Accept-Language': 'he,en'
        }
        # Load cached word frequency data if available
        self.frequency_words = set()

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

    def search_morfix(self, word: str) -> Optional[Dict]:
        """
        Search Morfix Hebrew-English dictionary

        Args:
            word: Hebrew word to search

        Returns:
            Dict with word info or None
        """
        try:
            # Morfix has a public API endpoint
            url = f"https://www.morfix.co.il/{word}"

            # Try to get JSON API response
            api_url = f"https://www.morfix.co.il/api/translate/{word}"

            response = requests.get(api_url, headers=self.headers, timeout=self.timeout)

            if response.status_code == 200:
                try:
                    data = response.json()
                    if data and 'Translation' in data:
                        translation = data.get('Translation', '')
                        return {
                            'word': word,
                            'definition': f"תרגום: {translation}",
                            'source': 'Morfix',
                            'url': url
                        }
                except:
                    pass

            return None

        except Exception as e:
            logger.debug(f"Morfix search error for '{word}': {e}")
            return None

    def search_reverso(self, word: str) -> Optional[Dict]:
        """
        Search Reverso Context for Hebrew word examples

        Args:
            word: Hebrew word to search

        Returns:
            Dict with word info or None
        """
        try:
            # Reverso Context API
            url = "https://context.reverso.net/bst-query-service"

            payload = {
                "source_text": word,
                "target_text": "",
                "source_lang": "he",
                "target_lang": "en",
                "npage": 1,
                "mode": 0
            }

            response = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                if data and 'list' in data and len(data['list']) > 0:
                    first_example = data['list'][0]
                    context = first_example.get('s_text', '')
                    translation = first_example.get('t_text', '')

                    return {
                        'word': word,
                        'definition': f"הקשר: {context[:100]}...",
                        'translation': translation,
                        'source': 'Reverso Context',
                        'url': f"https://context.reverso.net/translation/hebrew-english/{word}"
                    }

            return None

        except Exception as e:
            logger.debug(f"Reverso search error for '{word}': {e}")
            return None

    def search_academy(self, word: str) -> Optional[Dict]:
        """
        Search Academy of the Hebrew Language resources

        Args:
            word: Hebrew word to search

        Returns:
            Dict with word info or None
        """
        try:
            # Academy of the Hebrew Language has an online dictionary
            # milononline.net is their official dictionary
            url = f"https://milononline.net/search/{word}"

            # This would require HTML parsing for now
            # Placeholder for future implementation
            logger.debug(f"Academy search for '{word}' - not yet implemented")

            return None

        except Exception as e:
            logger.debug(f"Academy search error for '{word}': {e}")
            return None

    def load_github_hebrew_words(self, max_words: int = 5000) -> set:
        """
        Load Hebrew words from GitHub public repositories

        Sources common Hebrew word lists from GitHub

        Args:
            max_words: Maximum number of words to load

        Returns:
            Set of Hebrew words
        """
        words = set()

        try:
            # Popular Hebrew word list on GitHub
            # https://github.com/NLPH/NLPH_Resources
            github_urls = [
                # Hebrew word frequency list
                "https://raw.githubusercontent.com/NLPH/NLPH_Resources/master/code/wordlists/hebrew_words.txt",
                # Alternative source
                "https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt",
            ]

            for url in github_urls:
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        text = response.text
                        for line in text.split('\n'):
                            word = line.strip()
                            # Check if it's Hebrew (contains Hebrew characters)
                            if word and any('\u0590' <= c <= '\u05FF' for c in word):
                                words.add(word)
                                if len(words) >= max_words:
                                    break
                except:
                    continue

            if words:
                logger.info(f"Loaded {len(words)} Hebrew words from GitHub")

        except Exception as e:
            logger.error(f"Error loading GitHub words: {e}")

        return words

    def search_all_sources(self, word: str) -> Optional[Dict]:
        """
        Search all available online sources in priority order

        Priority order:
        1. Wiktionary (most reliable, free API)
        2. Morfix (Hebrew-English, good for translations)
        3. Reverso Context (usage examples)
        4. Academy of Hebrew Language (authoritative)

        Args:
            word: Hebrew word to search

        Returns:
            Dict with word info from first successful source
        """
        # Check cache first
        if word in self.cache:
            logger.info(f"  ✓ Cache hit for '{word}'")
            return self.cache[word]

        logger.info(f"  Searching online sources for '{word}'...")

        # Try each source in priority order
        sources = [
            ('Wiktionary', self.search_wiktionary),
            ('Morfix', self.search_morfix),
            ('Reverso', self.search_reverso),
            ('Academy', self.search_academy),
        ]

        for source_name, search_func in sources:
            try:
                logger.info(f"    Trying {source_name}...")
                result = search_func(word)
                if result:
                    logger.info(f"    ✓ Found '{word}' in {source_name}")
                    self.cache[word] = result
                    return result
                else:
                    logger.info(f"    ✗ '{word}' not found in {source_name}")
            except Exception as e:
                logger.warning(f"    ✗ Error searching {source_name} for '{word}': {e}")
                continue

        logger.info(f"  ✗ '{word}' not found in any online source")
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
