import re
from typing import List, Dict, Optional
from hebrew_dictionary import HebrewDictionary
from wikipedia_search import WikipediaSearch
from online_dictionary import OnlineDictionary
import logging

logger = logging.getLogger(__name__)

class CrosswordSolver:
    def __init__(self):
        self.dictionary = HebrewDictionary()
        self.wiki_search = WikipediaSearch()
        self.online_dict = OnlineDictionary()

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
        logger.info("="*60)
        logger.info(f"SEARCH REQUEST: pattern='{pattern}', known_letters='{known_letters}', length={length}")
        logger.info("="*60)

        results = []
        seen_words = set()

        # Get pattern length if specified
        if pattern and '_' in pattern:
            pattern_length = len(pattern)
        else:
            pattern_length = length

        logger.info(f"Determined pattern length: {pattern_length}")

        # Search in dictionary
        logger.info("\n[SOURCE 1/4] Searching Local Hebrew Dictionary...")
        try:
            dict_results = self.dictionary.search(pattern, known_letters, pattern_length)
            logger.info(f"✓ Local Dictionary found {len(dict_results)} matches")
            if dict_results:
                logger.info(f"  Sample results: {dict_results[:5]}")

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
            logger.error(f"✗ Error searching dictionary: {e}")

        # Search in Wikipedia for additional context
        logger.info("\n[SOURCE 2/4] Searching Wikipedia...")
        try:
            # Enrich ALL dictionary results with Wikipedia info (not just top 10)
            logger.info(f"Enriching {len(results)} dictionary results with Wikipedia data...")
            enriched_count = 0
            for result in results:
                word = result['word']
                wiki_result = self.wiki_search.search(word)
                if wiki_result:
                    result['description'] = wiki_result.get('description')
                    result['wiki_url'] = wiki_result.get('url')
                    result['source'] = 'Dictionary + Wikipedia'
                    enriched_count += 1
            logger.info(f"✓ Enriched {enriched_count} words with Wikipedia data")

            # ALWAYS search Wikipedia directly with pattern for comprehensive results
            # Remove the restriction that prevented patterns starting with underscores
            if pattern:
                logger.info(f"Searching Wikipedia for pattern '{pattern}'...")
                wiki_results = self.wiki_search.search_pattern(pattern, pattern_length)
                logger.info(f"✓ Wikipedia pattern search returned {len(wiki_results)} candidate words")

                matched_count = 0
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
                            matched_count += 1

                logger.info(f"✓ {matched_count} Wikipedia words matched pattern '{pattern}'")
                if matched_count > 0:
                    logger.info(f"  Sample Wikipedia matches: {list(seen_words)[:5]}")

        except Exception as e:
            logger.error(f"✗ Error searching Wikipedia: {e}")

        # Enrich ALL results with online dictionary definitions (not just top 10)
        logger.info("\n[SOURCE 3/4] Enriching with Online Dictionaries (Wiktionary, Morfix, Reverso)...")
        try:
            enriched_online = 0
            for result in results:
                if not result.get('description'):  # Only if no Wikipedia description
                    word = result['word']
                    online_result = self.online_dict.search_all_sources(word)
                    if online_result:
                        result['description'] = online_result.get('definition')
                        source_name = online_result.get('source', '')

                        # Add source attribution
                        if source_name:
                            result['source'] += f' + {source_name}'

                        # Add appropriate URL based on source
                        if 'Wiktionary' in source_name:
                            result['wiktionary_url'] = online_result.get('url')
                        elif 'Morfix' in source_name:
                            result['morfix_url'] = online_result.get('url')
                        elif 'Reverso' in source_name:
                            result['reverso_url'] = online_result.get('url')
                        elif 'Academy' in source_name:
                            result['academy_url'] = online_result.get('url')

                        # Add translation if available (from Morfix/Reverso)
                        if 'translation' in online_result:
                            result['translation'] = online_result.get('translation')

                        enriched_online += 1

            logger.info(f"✓ Enriched {enriched_online} words with online dictionary data")

        except Exception as e:
            logger.error(f"✗ Error enriching with online dictionary: {e}")

        # Sort by source priority (Dictionary + Wikipedia first)
        logger.info("\n[SOURCE 4/4] Sorting and preparing final results...")
        results.sort(key=lambda x: (
            0 if 'Wikipedia' in x['source'] else
            1 if 'Wiktionary' in x['source'] or 'Morfix' in x['source'] or 'Reverso' in x['source'] else
            2 if x['source'] == 'Hebrew Dictionary' else 3
        ))

        # Return ALL results (no limit)
        logger.info("="*60)
        logger.info(f"FINAL RESULTS: {len(results)} total matches for pattern '{pattern}'")
        logger.info("="*60)
        if results:
            logger.info("Top results:")
            for i, r in enumerate(results[:10], 1):
                logger.info(f"  {i}. {r['word']} (source: {r['source']})")
        else:
            logger.warning(f"⚠️  NO RESULTS FOUND for pattern '{pattern}'")
            logger.info("Troubleshooting tips:")
            logger.info("  - Check that pattern is correct (use _ for unknown letters)")
            logger.info("  - Verify internet connection for online sources")
            logger.info("  - Try a simpler pattern or fewer letters")

        return results

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
