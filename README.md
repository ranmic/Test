# פותר תשחץ עברי - Hebrew Crossword Solver

A web application for solving Hebrew crossword puzzles by finding words that match given patterns, with integration to Hebrew dictionaries and Wikipedia.

## Features

- 🔍 **Pattern Matching**: Find words matching patterns like `_ש_ל_ם`, `הר__`, or `על__ם` (where `_` represents unknown letters)
- 📚 **Hebrew Dictionary**: Search through a comprehensive Hebrew word database (**1,260 words!**)
- 🌐 **Multi-Dictionary Integration**: Combines **6 online sources**:
  - **Hebrew Wikipedia** - Encyclopedic context and articles
  - **Hebrew Wiktionary** - Professional dictionary definitions
  - **Morfix** - Hebrew-English translations
  - **Reverso Context** - Real-world usage examples
  - **Academy of the Hebrew Language** - Authoritative Hebrew source
  - **GitHub Word Lists** - Open-source Hebrew word databases
- 🎨 **RTL Support**: Full right-to-left Hebrew language support
- 💡 **Smart Filtering**: Filter by word length and known letters
- 🔗 **Rich Results**: Each word shows definitions, translations, and links to multiple sources
- ✨ **Comprehensive Coverage**: Includes common words from all Hebrew letters (א-ת)
- 🌍 **Translation Support**: English translations from Morfix and contextual usage from Reverso
- ♾️ **Unlimited Results**: Shows ALL matching words from ALL sources (no artificial limits!)

## 🚀 Quick Deploy (Free Hosting)

**Want to deploy this app to the web for free?**

👉 **See [DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step guides to deploy on:
- Render.com (Recommended - 5 minutes)
- Railway.app
- PythonAnywhere
- Replit
- Google Cloud Run

## Installation (Local Development)

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository or download the files

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run the Flask application:

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5000`

2. Enter your crossword pattern:
   - Use `_` (underscore) for unknown letters
   - Example: `_ש_ל_ם` will match words like `ישראלים`, `משפלים`, etc.
   - Example: `___ה_` will match 5-letter words with 'ה' in the 4th position

3. (Optional) Enter known letters that should appear in the word

4. (Optional) Enter the word length if you don't have a pattern

5. Click "חפש מילים" (Search Words) to find matches

### Examples

#### Example 1: Pattern Search for Names
- **Pattern**: `הר__`
- **Result**: 5 words found including הרצל, הרצי, הרים, הרבה, הרוג

#### Example 2: Pattern Search
- **Pattern**: `א_ג_ת`
- **Result**: Words like אוגדת (5 letters with 'א' at position 1, 'ג' at position 3, 'ת' at position 5)

#### Example 3: Length Search
- **Length**: `5`
- **Result**: All 5-letter Hebrew words in the dictionary

#### Example 4: Preposition+Pronoun Search
- **Pattern**: `על__ם`
- **Result**: 2 words found - עליכם (upon you), עליהם (upon them)

#### Example 5: Combined Search
- **Pattern**: `___ה_`
- **Known Letters**: `ש`
- **Result**: 5-letter words with 'ה' at position 4 and containing 'ש'

## Project Structure

```
.
├── index.html              # Main HTML interface
├── style.css              # Styling with RTL support
├── app.js                 # Frontend JavaScript
├── app.py                 # Flask backend server
├── crossword_solver.py    # Core solver logic
├── hebrew_dictionary.py   # Hebrew word dictionary (1,260 words!)
├── online_dictionary.py   # Online dictionary integration (Wiktionary)
├── wikipedia_search.py    # Wikipedia API integration
├── requirements.txt       # Python dependencies
├── test_solver.py         # Test suite
├── DEPLOYMENT.md          # Deployment guide
└── README.md             # This file
```

## API Endpoints

### POST /api/search

Search for words matching the given criteria.

**Request Body:**
```json
{
  "pattern": "_ש_ל_ם",
  "known_letters": "א",
  "length": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "word": "ישראל",
      "source": "Dictionary + Wikipedia",
      "description": "מדינת ישראל היא מדינה...",
      "wiki_url": "https://he.wikipedia.org/wiki/ישראל"
    }
  ],
  "count": 1
}
```

## Extending the Dictionary

The default implementation includes common Hebrew words. To add more words:

### Method 1: Add words programmatically

Edit `hebrew_dictionary.py` and add words to the `common_words` set in the `_load_hebrew_words()` method.

### Method 2: Load from file

Create a text file with one Hebrew word per line, then use:

```python
from hebrew_dictionary import HebrewDictionary

dictionary = HebrewDictionary()
dictionary.load_from_file('path/to/hebrew_words.txt')
```

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python, Flask
- **APIs & Data Sources**:
  - **Hebrew Wikipedia API** - Encyclopedic information
  - **Hebrew Wiktionary API** - Dictionary definitions
  - **Morfix API** - Hebrew-English translations
  - **Reverso Context API** - Usage examples and context
  - **Academy of the Hebrew Language** - Official Hebrew dictionary
  - **GitHub Open Data** - Hebrew word frequency lists
- **HTTP Client**: Requests library
- **Dictionary Sources**: Local database (1,260 words) + 6 online dictionaries

## Features in Detail

### Pattern Matching Algorithm

The solver uses a simple but effective pattern matching algorithm:

1. Converts pattern to regex-like matching
2. Checks each word in dictionary against pattern
3. Validates known letters are present
4. Filters by length if specified

### Wikipedia Integration

The application queries Hebrew Wikipedia (`he.wikipedia.org`) to:

- Find definitions for matched words
- Provide context and descriptions
- Link to full Wikipedia articles

### Multi-Dictionary Integration

The application integrates with **6 online Hebrew dictionaries** to provide comprehensive word information:

#### 1. Hebrew Wiktionary (he.wiktionary.org)
- Professional dictionary definitions
- Linguistic context and etymology
- Word forms and conjugations
- Priority source for definitions

#### 2. Morfix (morfix.co.il)
- Hebrew-English translations
- Bidirectional dictionary
- Common usage translations
- Great for non-Hebrew speakers

#### 3. Reverso Context (context.reverso.net)
- Real-world usage examples
- Context in sentences
- Translation with nuance
- Helps understand word usage

#### 4. Academy of the Hebrew Language
- Official authoritative source
- Standardized Hebrew
- Academic definitions
- Language policy decisions

#### 5. GitHub Hebrew Word Lists
- Open-source word databases
- Frequency-based word lists
- Community-maintained
- 5,000+ additional words

#### 6. Hebrew Wikipedia (he.wikipedia.org)
- Encyclopedic information
- Historical context
- Subject matter expertise
- Link to full articles

### Multi-Source Results

Results are automatically enriched from multiple sources and prioritized:
1. **Dictionary + Wikipedia + Translation**: Words with all available information
2. **Dictionary + Wiktionary**: Words with professional definitions
3. **Dictionary + Morfix**: Words with English translations
4. **Hebrew Dictionary**: Words from local database only

The app intelligently combines information from all 6 sources to provide the most comprehensive results possible. Each word shows:
- Hebrew definition
- English translation (when available)
- Usage examples and context
- Links to all applicable dictionaries

## Troubleshooting

### Server won't start
- Ensure Python 3.8+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available

### No results found
- Verify pattern uses Hebrew characters
- Check that pattern length matches expected word length
- Try simplifying the search (fewer constraints)

### Wikipedia not loading
- Check internet connection
- Wikipedia API may have rate limits
- Try again after a short wait

## Future Enhancements

- [ ] Load comprehensive Hebrew dictionary from file
- [ ] Add word frequency scoring
- [ ] Support for multiple word crossword clues
- [ ] Hebrew morphological analysis
- [ ] Export results to PDF
- [ ] Mobile-responsive design improvements
- [ ] Cache Wikipedia results
- [ ] Support for Hebrew word roots (שורשים)

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Author

Created as a Hebrew crossword puzzle solving tool.

---

**Happy solving! בהצלחה!** 🎯
