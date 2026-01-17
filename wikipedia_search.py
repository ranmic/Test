import requests
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class WikipediaSearch:
    def __init__(self):
        self.base_url = "https://he.wikipedia.org/w/api.php"
        self.session = requests.Session()

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
                return []

            # Search Wikipedia
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': search_term,
                'srlimit': 10,
                'utf8': 1
            }

            response = self.session.get(self.base_url, params=search_params, timeout=5)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get('query', {}).get('search', []):
                title = item['title']

                # Filter by length if specified
                if length and len(title) != length:
                    continue

                snippet = item.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')

                results.append({
                    'word': title,
                    'description': snippet[:200] + '...' if len(snippet) > 200 else snippet,
                    'url': f"https://he.wikipedia.org/wiki/{title.replace(' ', '_')}"
                })

            return results

        except Exception as e:
            logger.error(f"Error in pattern search: {e}")
            return []
