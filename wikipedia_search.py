import requests
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class WikipediaSearch:
    def __init__(self):
        self.base_url = "https://he.wikipedia.org/w/api.php"
        self.session = requests.Session()
        # Add proper User-Agent header as required by Wikipedia API
        self.session.headers.update({
            'User-Agent': 'HebrewCrosswordSolver/1.0 (https://github.com/ranmic/Test; Educational Project)',
            'Accept': 'application/json'
        })

    def search(self, term: str) -> Optional[Dict]:
        """
        Search Wikipedia for a specific term.

        Args:
            term: The search term (Hebrew word)

        Returns:
            Dictionary with word info or None if not found
        """
        try:
            # Search for the term
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': term,
                'srlimit': 1,
                'utf8': 1
            }

            response = self.session.get(self.base_url, params=search_params, timeout=5)
            response.raise_for_status()
            data = response.json()

            if not data.get('query', {}).get('search'):
                return None

            # Get the first result
            result = data['query']['search'][0]
            page_id = result['pageid']
            title = result['title']

            # Get page extract
            extract_params = {
                'action': 'query',
                'format': 'json',
                'prop': 'extracts',
                'pageids': page_id,
                'exintro': 1,
                'explaintext': 1,
                'utf8': 1
            }

            extract_response = self.session.get(self.base_url, params=extract_params, timeout=5)
            extract_response.raise_for_status()
            extract_data = extract_response.json()

            pages = extract_data.get('query', {}).get('pages', {})
            if str(page_id) in pages:
                extract = pages[str(page_id)].get('extract', '')
                # Get first 200 characters
                description = extract[:200] + '...' if len(extract) > 200 else extract
            else:
                description = result.get('snippet', '')

            return {
                'word': title,
                'description': description,
                'url': f"https://he.wikipedia.org/wiki/{title.replace(' ', '_')}"
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching Wikipedia: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in Wikipedia search: {e}")
            return None

    def search_pattern(self, pattern: str, length: Optional[int] = None) -> List[Dict]:
        """
        Search Wikipedia for words matching a pattern.

        Args:
            pattern: Search pattern
            length: Word length filter

        Returns:
            List of matching words with descriptions
        """
        try:
            # Remove underscores from pattern for search
            search_term = pattern.replace('_', '')

            if not search_term:
                logger.info("Wikipedia pattern search: Empty search term after removing underscores")
                return []

            logger.info(f"Wikipedia searching for pattern '{pattern}' (search term: '{search_term}', length: {length})")

            results = []
            seen_words = set()

            # STRATEGY 1: Search Wiktionary for comprehensive Hebrew word list
            logger.info("Strategy 1: Searching Hebrew Wiktionary word lists...")
            wiktionary_words = self._search_wiktionary_allpages(search_term, length)
            logger.info(f"Wiktionary returned {len(wiktionary_words)} candidate words")
            if wiktionary_words:
                sample_wiktionary = [w['word'] for w in wiktionary_words[:10]]
                logger.info(f"Sample Wiktionary words: {sample_wiktionary}")
                # Check if היפרבולה is in the results
                wiktionary_word_list = [w['word'] for w in wiktionary_words]
                if 'היפרבולה' in wiktionary_word_list:
                    logger.info("✓ Found היפרבולה in Wiktionary results!")
                else:
                    logger.warning("✗ היפרבולה NOT in Wiktionary results")

            for word_data in wiktionary_words:
                word = word_data['word']
                if word not in seen_words:
                    results.append(word_data)
                    seen_words.add(word)

            # STRATEGY 2: Search Wikipedia articles (original method)
            logger.info("Strategy 2: Searching Wikipedia articles...")
            # Search Wikipedia - increased limit to get more results
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': search_term,
                'srlimit': 50,  # Increased from 10 to 50 for comprehensive results
                'utf8': 1
            }

            response = self.session.get(self.base_url, params=search_params, timeout=5)
            response.raise_for_status()
            data = response.json()

            search_results = data.get('query', {}).get('search', [])
            logger.info(f"Wikipedia returned {len(search_results)} article results")

            all_extracted_words = []

            for item in search_results:
                title = item['title']
                snippet = item.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')

                # Extract individual words from title (Wikipedia titles can be phrases)
                # Split on spaces and common punctuation
                import re
                words_in_title = re.findall(r'[\u0590-\u05FF]+', title)

                # Also extract from snippet for more word candidates
                words_in_snippet = re.findall(r'[\u0590-\u05FF]+', snippet)
                all_words = words_in_title + words_in_snippet

                for word in all_words:
                    # Track all extracted words for debugging
                    if word not in all_extracted_words:
                        all_extracted_words.append(word)

                    # Skip if we've already seen this word
                    if word in seen_words:
                        continue

                    # Filter by length if specified
                    if length and len(word) != length:
                        continue

                    seen_words.add(word)
                    results.append({
                        'word': word,
                        'description': f"{title}: {snippet[:150]}" + ('...' if len(snippet) > 150 else ''),
                        'url': f"https://he.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    })

            # Log word length distribution for debugging
            from collections import Counter
            word_lengths = Counter(len(w) for w in all_extracted_words[:100])  # Sample first 100
            logger.info(f"Wikipedia extracted {len(all_extracted_words)} total unique words")
            logger.info(f"Word length distribution (sample): {dict(sorted(word_lengths.items()))}")
            logger.info(f"Wikipedia pattern search found {len(results)} unique words matching length {length}")
            if results:
                logger.info(f"Sample Wikipedia results: {[r['word'] for r in results[:5]]}")
            elif all_extracted_words:
                # Show what we DID extract, even if it doesn't match length
                sample_words_by_length = {}
                for w in all_extracted_words[:30]:
                    wlen = len(w)
                    if wlen not in sample_words_by_length:
                        sample_words_by_length[wlen] = []
                    if len(sample_words_by_length[wlen]) < 3:
                        sample_words_by_length[wlen].append(w)
                logger.info(f"Sample extracted words by length: {sample_words_by_length}")

            return results

        except Exception as e:
            logger.error(f"Error in Wikipedia pattern search: {e}")
            return []

    def _search_wiktionary_allpages(self, search_term: str, length: Optional[int] = None) -> List[Dict]:
        """
        Search Hebrew Wiktionary using SEARCH API for words containing the search term.

        Args:
            search_term: Hebrew letters to search for (must be IN the word)
            length: Required word length

        Returns:
            List of word dictionaries
        """
        try:
            results = []
            seen_words = set()

            wiktionary_url = "https://he.wiktionary.org/w/api.php"

            # STRATEGY: Use Wiktionary's SEARCH API (more comprehensive than allpages)
            # Search for the letter itself to find all words containing it
            logger.info(f"Using Wiktionary SEARCH API for words containing '{search_term}'...")

            # Search Wiktionary for pages containing the search term
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': search_term,
                'srlimit': 500,  # Get up to 500 results
                'srnamespace': 0,  # Main namespace only
            }

            try:
                response = self.session.get(wiktionary_url, params=search_params, timeout=10)
                response.raise_for_status()
                data = response.json()

                search_results = data.get('query', {}).get('search', [])
                logger.info(f"Wiktionary search returned {len(search_results)} pages")

                for item in search_results:
                    word = item['title']

                    # Skip if already seen
                    if word in seen_words:
                        continue

                    # Only keep Hebrew words (filter out Latin, special chars, etc.)
                    if not any('\u0590' <= c <= '\u05FF' for c in word):
                        continue

                    # Filter by length if specified
                    if length and len(word) != length:
                        continue

                    # Check if word contains the search term
                    if search_term in word:
                        results.append({
                            'word': word,
                            'description': f'מילה מהוויקימילון העברי',
                            'url': f"https://he.wiktionary.org/wiki/{word}"
                        })
                        seen_words.add(word)

                logger.info(f"Wiktionary search found {len(results)} words containing '{search_term}' with length {length}")
                if results:
                    logger.info(f"Sample Wiktionary words from SEARCH: {[r['word'] for r in results[:10]]}")

            except Exception as e:
                logger.warning(f"Error in Wiktionary search: {e}")

            return results

        except Exception as e:
            logger.warning(f"Error searching Wiktionary: {e}")
            return []
