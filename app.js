async function searchWords() {
    const pattern = document.getElementById('pattern').value.trim();
    const knownLetters = document.getElementById('knownLetters').value.trim();
    const length = document.getElementById('length').value;

    if (!pattern && !length) {
        alert('נא להזין תבנית או אורך מילה / Please enter a pattern or word length');
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').classList.remove('show');

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pattern: pattern,
                known_letters: knownLetters,
                length: length ? parseInt(length) : null
            })
        });

        if (!response.ok) {
            throw new Error('שגיאה בחיפוש / Search error');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        displayError('אירעה שגיאה בחיפוש. נסה שוב. / An error occurred during search. Please try again.');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function displayResults(data) {
    const resultsDiv = document.getElementById('resultsContent');
    resultsDiv.innerHTML = '';

    if (data.results && data.results.length > 0) {
        data.results.forEach(result => {
            const card = createWordCard(result);
            resultsDiv.appendChild(card);
        });
    } else {
        resultsDiv.innerHTML = '<div class="no-results">לא נמצאו תוצאות / No results found</div>';
    }

    document.getElementById('results').classList.add('show');
}

function createWordCard(result) {
    const card = document.createElement('div');
    card.className = 'word-card';

    const title = document.createElement('div');
    title.className = 'word-title';
    title.textContent = result.word;

    const source = document.createElement('div');
    source.className = 'word-source';
    source.textContent = `מקור: ${result.source} / Source: ${result.source}`;

    card.appendChild(title);
    card.appendChild(source);

    if (result.description) {
        const description = document.createElement('div');
        description.className = 'word-description';
        description.textContent = result.description;
        card.appendChild(description);
    }

    if (result.wiki_url) {
        const link = document.createElement('a');
        link.className = 'wiki-link';
        link.href = result.wiki_url;
        link.target = '_blank';
        link.textContent = 'קרא עוד בוויקיפדיה / Read more on Wikipedia →';
        card.appendChild(link);
    }

    if (result.wiktionary_url) {
        const link = document.createElement('a');
        link.className = 'wiki-link';
        link.href = result.wiktionary_url;
        link.target = '_blank';
        link.textContent = 'הגדרה בוויקימילון / Definition in Wiktionary →';
        card.appendChild(link);
    }

    return card;
}

function displayError(message) {
    const resultsDiv = document.getElementById('resultsContent');
    resultsDiv.innerHTML = `<div class="error">${message}</div>`;
    document.getElementById('results').classList.add('show');
}

// Allow Enter key to trigger search
document.getElementById('pattern').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchWords();
    }
});

document.getElementById('knownLetters').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchWords();
    }
});

document.getElementById('length').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchWords();
    }
});
