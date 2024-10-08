const ctx = document.getElementById('typing-test-chart');
const saveResultsEle = document.getElementsByClassName('save-results-button')[0];
const reportResultsEle = document.getElementsByClassName('report-results-button')[0];

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const encodedData = urlParams.get('data');
const decodedData = JSON.parse(atob(encodedData));
const dataPoints = 20;
const dataObj = {
    wordsToShow: 0,
    secondsInTest: 0,
};

dataObj.wordsToShow = decodedData.wordsToShow;
dataObj.secondsInTest = decodedData.secondsInTest;

var keys = Object.keys(decodedData);
keys.splice(keys.indexOf('wordsToShow'), 1);
keys.splice(keys.indexOf('secondsInTest'), 1);

for (const key of keys) {
    if (key.startsWith('te_')) {
        dataObj[key.slice(3)] = decodedData[key];
    } else {
        let value = decodedData[key];

        if (typeof value === 'object') {
            if (dataObj[key] === undefined) {
                dataObj[key] = {};
            }
            for (const [innerKey, innerValue] of Object.entries(value)) {
                if (typeof innerValue === 'string' && innerKey.match(/^[0-9]+$/)) {
                    innerKey = parseInt(innerKey);
                }

                if (typeof innerValue === 'string' && innerValue.match(/^[0-9]+$/)) {
                    innerValue = parseInt(innerValue);
                }

                dataObj[key][innerKey] = innerValue;
            }
        } else {
            dataObj[key] = value;
        }
    }
}

const avgWordLength = Object.values(dataObj.wordLength).reduce((a, b) => a + b, 0) / Object.values(dataObj.wordLength).length;
dataObj.avgWordLength = avgWordLength;

dataObj.wpm = [];
dataObj.error = {};

let intervalsToCheck = Math.floor((dataObj.secondsInTest / dataPoints) * 10);

let totalCorrect = 0;
for (let i = 0; i < dataPoints; i++) {
    let startInterval = i * intervalsToCheck;
    let endInterval = (i + 1) * intervalsToCheck;

    let lettersTypedCorrect = 0;
    let lettersTypedIncorrect = 0;

    for (let j = 0; j < dataObj.t.length; j++) {
        if (dataObj.t[j] >= startInterval && dataObj.t[j] <= endInterval) {
            lettersTypedCorrect += dataObj.c[j] == 'c';
            lettersTypedIncorrect += dataObj.c[j] == 'i';
        }
    }

    let intervalCompute = lettersTypedCorrect / dataObj.avgWordLength;

    dataObj.wpm.push(
        intervalCompute * 60 / (intervalsToCheck / 10)
    );

    if (lettersTypedIncorrect > 0) {
        dataObj.error[(endInterval / 10)] = lettersTypedIncorrect;
    }

    totalCorrect += lettersTypedCorrect;
}

if (totalCorrect >= 1) {
    let totalCorrectLettersTyped = 0;
    for (let j = 0; j < dataObj.c.length; j++) {
        totalCorrectLettersTyped += dataObj.c[j] == 'c';
    }

    dataObj.accuracy = (totalCorrectLettersTyped / dataObj.c.length) * 100;
    dataObj.wpm = dataObj.wpm.map(x => Math.round(x, 2));
    dataObj.avgWpm = dataObj.wpm.reduce((a, b) => a + b, 0) / dataObj.wpm.length;
    dataObj.accuracyStr = `${Math.ceil(dataObj.accuracy * 10) / 10}%`;
    dataObj.avgWpmStr = `${Math.ceil(dataObj.avgWpm * 10) / 10}`;

    fetch('/results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: "wpm=" + dataObj.avgWpmStr
    });
}

let labels = Array.from({length: dataPoints}, (_, i) => (i + 1) * (intervalsToCheck / 10));
labels = labels.map(x => Math.ceil(x * 10) / 10);

new Chart(ctx, {
    data: {
        labels: labels,
        datasets: [
            {
                type: 'line',
                label: 'WPM',
                data: dataObj.wpm,
                borderColor: '#F4CE14'
            },
            {
                type: 'scatter',
                label: 'Error',
                data: Object.values(dataObj.error),
                backgroundColor: '#ca4754',
                xAxisID: 'x2',
                yAxisID: 'y2'
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'WPM',
                    color: '#F4CE14'
                }
            },
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Time (s)',
                    color: '#F4CE14'
                }
            },
            x2: {
                beginAtZero: true,
                display: false,
            },
            y2: {
                beginAtZero: true,
                position: 'right',
                title: {
                    display: true,
                    text: 'Errors',
                    color: '#ca4754'
                },
                grid: {
                    display: false
                }
            }
        }
    }
});

saveResultsEle.addEventListener('click', () => {
    fetch('/results/latest', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: "data=" + encodedData
    });
});

reportResultsEle.addEventListener('click', () => {
    fetch('/results/report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: "data=" + encodedData
    });
});

const wpmEle = document.getElementById('wpm');
const accuracyEle = document.getElementById('accuracy');

wpmEle.innerHTML = dataObj.avgWpmStr;
accuracyEle.innerHTML = dataObj.accuracyStr;