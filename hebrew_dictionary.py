import re
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class HebrewDictionary:
    def __init__(self):
        # Common Hebrew words dictionary
        # In a production app, this would load from a file or database
        self.words = self._load_hebrew_words()

    def _load_hebrew_words(self) -> set:
        """
        Load Hebrew words. This is a basic set - in production,
        you'd load from a comprehensive Hebrew dictionary file.
        """
        common_words = {
            # Common Hebrew words for testing
            'שלום', 'עולם', 'ישראל', 'ירושלים', 'תל', 'אביב',
            'חיפה', 'באר', 'שבע', 'אילת', 'נתניה', 'אשדוד',
            'חולון', 'פתח', 'תקווה', 'ראשון', 'לציון',
            'בית', 'ספר', 'בית', 'חולים', 'משפחה',
            'אהבה', 'שמחה', 'חופש', 'שלווה', 'צדק',
            'אמת', 'יופי', 'תקווה', 'אור', 'חיים',
            'מים', 'אש', 'רוח', 'אדמה', 'שמיים',
            'ים', 'הר', 'מדבר', 'יער', 'גן',
            'פרח', 'עץ', 'שמש', 'ירח', 'כוכב',
            'ספר', 'עיתון', 'מחשב', 'טלפון', 'רדיו',
            'טלוויזיה', 'אינטרנט', 'דואר', 'מכתב', 'חבר',
            'אח', 'אחות', 'אב', 'אם', 'בן', 'בת',
            'סבא', 'סבתא', 'דוד', 'דודה', 'משפט',
            'מלה', 'אות', 'מספר', 'חשבון', 'פעולה',
            'תשובה', 'שאלה', 'בעיה', 'פתרון', 'דרך',
            'רחוב', 'כביש', 'שדרה', 'סמטה', 'כיכר',
            'פינה', 'מרכז', 'שוק', 'חנות', 'קניון',
            'בנק', 'דואר', 'משטרה', 'כיבוי', 'אש',
            'בית', 'דירה', 'חדר', 'מטבח', 'אמבטיה',
            'סלון', 'מרפסת', 'גינה', 'חצר', 'גג',
            'קיר', 'תקרה', 'רצפה', 'דלת', 'חלון',
            'שולחן', 'כיסא', 'מיטה', 'ארון', 'מדף',
            'ראי', 'שעון', 'תמונה', 'מנורה', 'שטיח',
            'תשחץ', 'תשבץ', 'משחק', 'חידה', 'פאזל',
            'קלפים', 'קוביה', 'לוח', 'כדור', 'רקטה',
            'בריכה', 'מגרש', 'אצטדיון', 'כושר', 'ריצה',
            'שחיה', 'כדורגל', 'כדורסל', 'טניס', 'שחמט',
            'יוגה', 'פילאטיס', 'אימון', 'תרגיל', 'מתיחה',
        }

        logger.info(f"Loaded {len(common_words)} Hebrew words")
        return common_words

    def search(self, pattern: str, known_letters: str = '', length: Optional[int] = None) -> List[str]:
        """
        Search for words matching the pattern.

        Args:
            pattern: Pattern with _ for unknown letters (e.g., "_ש_ל_ם")
            known_letters: Letters that must be in the word
            length: Required word length

        Returns:
            List of matching words
        """
        matches = []

        for word in self.words:
            if self._matches(word, pattern, known_letters, length):
                matches.append(word)

        return sorted(matches)

    def _matches(self, word: str, pattern: str, known_letters: str, length: Optional[int]) -> bool:
        """Check if a word matches all criteria."""

        # Check length
        if length and len(word) != length:
            return False

        # Check pattern
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

    def add_word(self, word: str):
        """Add a word to the dictionary."""
        self.words.add(word)

    def load_from_file(self, filepath: str):
        """
        Load words from a file (one word per line).
        This can be used to load a comprehensive Hebrew dictionary.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.words.add(word)
            logger.info(f"Loaded {len(self.words)} words from {filepath}")
        except FileNotFoundError:
            logger.warning(f"Dictionary file not found: {filepath}")
        except Exception as e:
            logger.error(f"Error loading dictionary: {e}")
