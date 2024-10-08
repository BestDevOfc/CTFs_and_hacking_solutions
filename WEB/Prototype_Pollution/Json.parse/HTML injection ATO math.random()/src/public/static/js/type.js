const wordList = ['word', 'the', 'and', 'for', 'that', 'this', 'with', 'you', 'not', 'are', 'from', 'your', 'all', 'have', 'new', 'more', 'was', 'will', 'home', 'can', 'about', 'page', 'has', 'search', 'free', 'but', 'our', 'one', 'other', 'information', 'time', 'they', 'site', 'may', 'what', 'which', 'their', 'news', 'out', 'use', 'any', 'there', 'see', 'only', 'his', 'when', 'contact', 'here', 'business', 'who', 'web', 'also', 'now', 'help', 'get', 'view', 'online', 'first', 'been', 'would', 'how', 'were', 'services', 'some', 'these', 'click', 'its', 'like', 'service', 'than', 'find', 'price', 'date', 'back', 'top', 'people', 'had', 'list', 'name', 'just', 'over', 'state', 'year', 'day', 'into', 'email', 'two', 'health', 'world', 'next', 'used', 'work', 'last', 'most', 'products', 'music', 'buy', 'data', 'make', 'them', 'should', 'product', 'system', 'post', 'her', 'city', 'add', 'policy', 'number', 'such', 'please', 'available', 'copyright', 'support', 'message', 'after', 'best', 'software', 'then', 'jan', 'good', 'video', 'well', 'where', 'info', 'rights', 'public', 'books', 'high', 'school', 'through', 'each', 'links', 'she', 'review', 'years', 'order', 'very', 'privacy', 'book', 'items', 'company', 'read', 'group', 'need', 'many', 'user', 'said', 'does', 'set', 'under', 'general', 'research', 'university', 'january', 'mail', 'full', 'map', 'reviews', 'program', 'life', 'know', 'games', 'way', 'days', 'management', 'part', 'could', 'great', 'united', 'hotel', 'real', 'item', 'international', 'center', 'ebay', 'must', 'store', 'travel', 'comments', 'made', 'development', 'report', 'off', 'member', 'details', 'line', 'terms', 'before', 'hotels', 'did', 'send', 'right', 'type', 'because', 'local', 'those', 'using', 'results', 'office', 'education', 'national', 'car', 'design', 'take', 'posted', 'internet', 'address', 'community', 'within', 'states', 'area', 'want', 'phone', 'dvd', 'shipping', 'reserved', 'subject', 'between', 'forum', 'family', 'long', 'based', 'code', 'show', 'even', 'black', 'check', 'special', 'prices', 'website', 'index', 'being', 'women', 'much', 'sign', 'file', 'link', 'open', 'today', 'technology', 'south', 'case', 'project', 'same', 'pages', 'version', 'section', 'own', 'found', 'sports', 'house', 'related', 'security', 'both', 'county', 'american', 'photo', 'game', 'members', 'power', 'while', 'care', 'network', 'down', 'computer', 'systems', 'three', 'total', 'place', 'end', 'following', 'download', 'him', 'without', 'per', 'access', 'think', 'north', 'resources', 'current', 'posts', 'big', 'media', 'law', 'control', 'water', 'history', 'pictures', 'size', 'art', 'personal', 'since', 'including', 'guide', 'shop', 'directory', 'board', 'location', 'change', 'white', 'text', 'small', 'rating', 'rate', 'government', 'children', 'during', 'usa', 'return', 'students', 'shopping', 'account', 'times', 'sites', 'level', 'digital', 'profile', 'previous', 'form', 'events', 'love', 'old', 'john', 'main', 'call', 'hours', 'image', 'department', 'title', 'description', 'non', 'insurance', 'another', 'why', 'shall', 'property', 'class', 'still', 'money', 'quality', 'every', 'listing', 'content', 'country', 'private', 'little', 'visit', 'save', 'tools', 'low', 'reply', 'customer', 'december', 'compare', 'movies', 'include', 'college', 'value', 'article', 'york', 'man', 'card', 'jobs', 'provide', 'food', 'source', 'author', 'different', 'press', 'learn', 'sale', 'around', 'print', 'course', 'job', 'canada', 'process', 'teen', 'room', 'stock', 'training', 'too', 'credit', 'point', 'join', 'science', 'men', 'categories', 'advanced', 'west', 'sales', 'look', 'english', 'left', 'team', 'estate', 'box', 'conditions', 'select', 'windows', 'photos', 'thread', 'week', 'category', 'note', 'live', 'large', 'gallery', 'table', 'register', 'however', 'june', 'october', 'november', 'market', 'library', 'really', 'action', 'start', 'series', 'model', 'features', 'air', 'industry', 'plan', 'human', 'provided', 'yes', 'required', 'second', 'hot', 'accessories', 'cost', 'movie', 'forums', 'march', 'september', 'better', 'say', 'questions', 'july', 'yahoo'];

function getRandomWord() {
    return wordList[Math.floor(Math.random() * wordList.length)];
}

const wordsToShow = 10 * 3;
const secondsInTest = 30;

const typingInputEl = document.getElementsByClassName('typing-input-container')[0];

const buffer = [];
for (let i = 0; i < wordsToShow; i++) {
    buffer.push(getRandomWord());
}

typingInputEl.innerHTML = '';
for (let i = 0; i < wordsToShow; i++) {
    let wordHTML = '<word>';
    let word = buffer[i];
    for (let j = 0; j < word.length; j++) {
        wordHTML += `<letter>${word.charAt(j)}</letter>`;
    }
    wordHTML += '</word>';
    typingInputEl.innerHTML += wordHTML;
}

typingInputEl.children[0].children[0].classList.add('active');

let currentWord = 0;
let currentLetter = 0;
let started = false;
let startedTimer = null;
let events = {
    wordsToShow: wordsToShow,
    wordLength: buffer.map((word) => word.length),
    secondsInTest: secondsInTest,
    timed_events: [],
    sparse_events: {},
};
let testEnded = false;
let addedExtra = 0;

function removeExtraAfterCurrentLetter() {
    let currentWordEl = typingInputEl.children[currentWord];

    let extraEleToRemove = [];
    for (let i = currentLetter + 1; i < currentWordEl.children.length; i++) {
        if (currentWordEl.children[i].classList.contains('extra')) {
            extraEleToRemove.push(i);
        }
    }

    for (let i = extraEleToRemove.length - 1; i >= 0; i--) {
        currentWordEl.children[extraEleToRemove[i]].remove();
        addedExtra = Math.max(addedExtra - 1, 0);
    }
}

function processKey(key) {
    if (key == ' ') {
        if (currentWord == wordsToShow - 1) {
            gameOver();
            return;
        }

        for (let i = currentLetter; i < typingInputEl.children[currentWord].children.length; i++) {
            typingInputEl.children[currentWord].children[i].classList.add('incorrect');
        }

        currentWord++;
        currentLetter = 0;
        return;
    }

    let currentWordEl = typingInputEl.children[currentWord];

    if (currentLetter >= currentWordEl.children.length && (key !== 'Backspace')) {
        let letterEl = document.createElement('letter');
        letterEl.classList.add('extra');
        letterEl.classList.add('incorrect');
        letterEl.innerText = key;
        currentWordEl.appendChild(letterEl);
        addedExtra++;

        let tmpSparseKey = (Math.floor((new Date() - startedTimer) / 100));
        if (tmpSparseKey in events.sparse_events) {
            events.sparse_events[tmpSparseKey] += 1;
        }
        else {
            events.sparse_events[tmpSparseKey] = 1;
        }

        return;
    }

    let currentLetterEl = currentWordEl.children[currentLetter];

    if (key === 'Backspace') {
        if (currentLetter >= 0) {
            if (currentLetter > (currentWordEl.children.length - addedExtra) && currentWordEl.children[currentLetter - 1].classList.contains('extra')) {
                currentWordEl.children[currentLetter - 1].remove();
                addedExtra--;
            }
            else {
                currentLetterTmp = Math.max(currentLetter - 1, 0);
                currentWordEl.children[currentLetterTmp].classList.remove('incorrect');
                currentWordEl.children[currentLetterTmp].classList.remove('correct');
            }

            if (currentLetter > 0) {
                currentLetter--;
            }
        }

        if (currentLetter < currentWordEl.children.length) {
            removeExtraAfterCurrentLetter();
        }

        return;
    }

    if (key === currentLetterEl.innerText) {
        currentLetterEl.classList.add('correct');
        events.timed_events.push({
            t: Math.floor((new Date() - startedTimer) / 100),
            k: key,
            c: 'c'
        });
    } else {
        currentLetterEl.classList.add('incorrect');
        events.timed_events.push({
            t: Math.floor((new Date() - startedTimer) / 100),
            k: key,
            c: 'i'
        });
    }

    if (currentLetter < currentWordEl.children.length) {
        removeExtraAfterCurrentLetter();
    }

    currentLetter++;
}

timerEle = document.getElementsByClassName('typing-test-timer')[0];

function gameOver() {
    testEnded = true;
    clearInterval(intervalIdDecrementTimer);

    events['te_t'] = [];
    events['te_c'] = '';
    for (let i = 0; i < events.timed_events.length; i++) {
        events['te_t'].push(events.timed_events[i].t);
        events['te_c'] += events.timed_events[i].c.toString();
    }

    delete events.timed_events;

    if (timerEle.innerText !== '0') {
        events.secondsInTest = Math.floor((new Date() - startedTimer) / 1000) + 1;
    }
    
    let encodedObj = btoa(JSON.stringify(events));
    window.location.href = `/results?data=${encodedObj}`;
}

function decrementTimer() {
    if (!started) {
        return;
    }

    timerEle.removeAttribute('hidden');

    let currentTime = new Date();
    let timeDiffInSeconds = (currentTime - startedTimer) / 1000;
    let timeLeft = Math.floor(secondsInTest - timeDiffInSeconds);

    if (timeLeft <= 0) {
        timerEle.innerText = '0';
        gameOver();
        return;
    }

    timerEle.innerText = timeLeft;
}

var intervalIdDecrementTimer = window.setInterval(function(){
    decrementTimer();
}, 250);

mainEle = document.getElementsByTagName('html')[0];

mainEle.addEventListener('keydown', (event) => {
    if (testEnded) {
        return;
    }

    let letter = event.key;

    if (letter.length === 1) {
        letter = letter.toLowerCase();
    }

    if (!started) {
        if (letter.match(/[a-z ]/i)) {
            started = true;
            startedTimer = new Date();
        } else {
            return;
        }
    }

    if (! (letter.length === 1 || letter === 'Backspace' || letter === ' ')) {
        return;
    }

    processKey(event.key);

    for (let i = 0; i < typingInputEl.children[currentWord].children.length; i++) {
        typingInputEl.children[currentWord].children[i].classList.remove('active');
        typingInputEl.children[currentWord].children[i].classList.remove('activeLast');
    }

    if (currentWord > 0) {
        for (let i = 0; i < typingInputEl.children[currentWord - 1].children.length; i++) {
            typingInputEl.children[currentWord - 1].children[i].classList.remove('active');
            typingInputEl.children[currentWord - 1].children[i].classList.remove('activeLast');
        }
    }

    let seenClass = false;
    let largestIndex = -1;
    for (let i = 0; i < typingInputEl.children[currentWord].children.length; i++) {
        if (typingInputEl.children[currentWord].children[i].classList.length > 0) {
            seenClass = true;
            largestIndex = i;
        }
    }

    if (seenClass) {
        if (largestIndex == typingInputEl.children[currentWord].children.length - 1) {
            typingInputEl.children[currentWord].children[largestIndex].classList.add('activeLast');
        } else {
            typingInputEl.children[currentWord].children[largestIndex + 1].classList.add('active');
        }
    } else {
        typingInputEl.children[currentWord].children[0].classList.add('active');
    }

    if (currentWord == wordsToShow - 1) {
        let lastWordEl = typingInputEl.children[currentWord];
        let lastWordElChildren = lastWordEl.children;
        for (let i = 0; i < lastWordElChildren.length; i++) {
            let classList = lastWordElChildren[i].classList;
            let classListLength = classList.length - 1;
            if (classListLength > 0) {
                classList.remove('active');
                classList.remove('activeLast');
            }

            if (classListLength === 0) {
                return;
            }
        }

        gameOver();
    }
});

document.onload = function() {
    mainEle.focus();
}