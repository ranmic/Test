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

    def _pattern_to_search_query(self, pattern: str) -> tuple:
        """
        Convert a pattern to search query and regex for matching.

        Args:
            pattern: Pattern with _ for unknown letters (e.g., ____ב___)

        Returns:
            Tuple of (search_query, regex_pattern)
        """
        import re

        # Extract known letters for Wikipedia search
        known_letters = pattern.replace('_', '')

        # Convert pattern to regex for post-filtering
        # _ becomes . (any Hebrew character)
        # This ensures we only match Hebrew letters, not spaces or punctuation
        regex_pattern = ''
        for char in pattern:
            if char == '_':
                regex_pattern += '[\u0590-\u05FF]'  # Any Hebrew character
            else:
                regex_pattern += re.escape(char)  # Exact letter match

        # Build SMART search query using ALL known letters with AND logic
        # This reduces the number of results Wikipedia returns
        # Wikipedia doesn't support regex, but we can use multiple intitle: operators
        if len(known_letters) > 1:
            # Multiple letters: deduplicate and use "intitle:letter1 intitle:letter2 ..." (implicit AND)
            # Deduplicate to avoid redundant queries like "intitle:ו intitle:ו"
            unique_letters = list(dict.fromkeys(known_letters))  # Preserves order, removes duplicates
            letter_queries = [f'intitle:{letter}' for letter in unique_letters]
            search_query = ' '.join(letter_queries)
        else:
            # Single letter: just use intitle:letter
            search_query = f'intitle:{known_letters}'

        logger.info(f"Converted pattern '{pattern}' to:")
        logger.info(f"  - Known letters: '{known_letters}' → Unique: {list(dict.fromkeys(known_letters))}")
        logger.info(f"  - Search query: '{search_query}' (titles must contain ALL these letters)")
        logger.info(f"  - Regex pattern: '^{regex_pattern}$' (ensures exact position match)")

        return search_query, f'^{regex_pattern}$'

    def search_pattern(self, pattern: str, length: Optional[int] = None) -> List[Dict]:
        """
        Search Wikipedia for words matching a pattern.

        Args:
            pattern: Search pattern with _ for unknown letters (e.g., ____ב___)
            length: Word length filter

        Returns:
            List of matching words with descriptions
        """
        try:
            import re as regex_module

            # Build smart search query and regex pattern from user input
            search_query, regex_pattern = self._pattern_to_search_query(pattern)

            if not search_query:
                logger.info("Wikipedia pattern search: Empty search query after conversion")
                return []

            logger.info(f"Wikipedia searching for pattern '{pattern}'")
            logger.info(f"  Using search query: '{search_query}'")
            logger.info(f"  Using regex filter: '{regex_pattern}'")

            # Compile regex for efficient matching
            compiled_regex = regex_module.compile(regex_pattern)

            results = []
            seen_words = set()

            # STRATEGY 1: Search Wiktionary for comprehensive Hebrew word list
            logger.info("Strategy 1: Searching Hebrew Wiktionary word lists...")
            # Extract just letters for Wiktionary search
            search_term = pattern.replace('_', '')
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

            # STRATEGY 2: Search Wikipedia articles with intitle:
            logger.info("Strategy 2: Searching Wikipedia articles with intitle:...")

            # FIRST: Check if specific test words exist in Wikipedia (for debugging)
            # Common words that might be searched: היפרבולה, גוודלקנל, etc.
            test_words = ['היפרבולה', 'גוודלקנל']
            for test_word in test_words:
                # Only test words that match our pattern length and letters
                if length and len(test_word) == length and search_term in test_word:
                    test_params = {
                        'action': 'query',
                        'format': 'json',
                        'titles': test_word,
                        'prop': 'info'
                    }
                    try:
                        test_response = self.session.get(self.base_url, params=test_params, timeout=5)
                        test_data = test_response.json()
                        test_pages = test_data.get('query', {}).get('pages', {})
                        if '-1' not in test_pages:
                            logger.info(f"✓ Test: '{test_word}' EXISTS as a Wikipedia page!")
                            # Check if it matches the regex pattern
                            if compiled_regex.match(test_word):
                                logger.info(f"✓ Test: '{test_word}' MATCHES pattern '{pattern}'!")
                                if test_word not in seen_words:
                                    results.append({
                                        'word': test_word,
                                        'description': f'מילה מוויקיפדיה העברית',
                                        'url': f"https://he.wikipedia.org/wiki/{test_word}"
                                    })
                                    seen_words.add(test_word)
                                    logger.info(f"✓ Added '{test_word}' directly to results!")
                            else:
                                logger.warning(f"✗ Test: '{test_word}' exists but does NOT match pattern '{pattern}'")
                        else:
                            logger.info(f"ℹ Test: '{test_word}' does NOT exist as Wikipedia page")
                    except Exception as e:
                        logger.debug(f"Test query error for '{test_word}': {e}")

            # Search Wikipedia with improved intitle: query
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': search_query,  # Use smart search query instead of just letters
                'srlimit': 50,
                'utf8': 1
            }

            response = self.session.get(self.base_url, params=search_params, timeout=5)
            response.raise_for_status()
            data = response.json()

            search_results = data.get('query', {}).get('search', [])
            logger.info(f"Wikipedia returned {len(search_results)} article results for '{search_query}'")

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

                    # Apply regex pattern matching to ensure exact match
                    if not compiled_regex.match(word):
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

            # FIRST: Check if specific word exists (for debugging)
            test_word = 'היפרבולה'
            test_params = {
                'action': 'query',
                'format': 'json',
                'titles': test_word,
                'prop': 'info'
            }
            try:
                test_response = self.session.get(wiktionary_url, params=test_params, timeout=5)
                test_data = test_response.json()
                test_pages = test_data.get('query', {}).get('pages', {})
                if '-1' not in test_pages:
                    logger.info(f"✓ Test: '{test_word}' EXISTS as a Wiktionary page!")
                else:
                    logger.warning(f"✗ Test: '{test_word}' does NOT exist in Hebrew Wiktionary")
            except Exception as e:
                logger.debug(f"Test query error: {e}")

            # Search Wiktionary for pages containing the search term
            # Use intitle: to search specifically in page titles
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': f'intitle:{search_term}',  # Search in titles containing the letter
                'srlimit': 500,  # Get up to 500 results
                'srnamespace': 0,  # Main namespace only
            }

            try:
                response = self.session.get(wiktionary_url, params=search_params, timeout=10)
                response.raise_for_status()
                data = response.json()

                search_results = data.get('query', {}).get('search', [])
                logger.info(f"Wiktionary search returned {len(search_results)} pages for 'intitle:{search_term}'")

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
