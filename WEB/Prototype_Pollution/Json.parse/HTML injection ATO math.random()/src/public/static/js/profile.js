const highestWPMEle = document.getElementById('highest-wpm');
const averageWPMEle = document.getElementById('average-wpm');
const testsTakenEle = document.getElementById('tests-taken');
const ctx = document.getElementById('typing-stats-chart');

var wpms = [];

fetch('/profile/wpms')
    .then(response => response.json())
    .then(data => {
        wpms = data;

        let highestWPM = Math.max(...wpms);
        let averageWPM = wpms.reduce((a, b) => a + b, 0) / wpms.length;
        let testsTaken = wpms.length;

        highestWPMEle.innerText = `Highest WPM: ${Math.floor(highestWPM * 100) / 100}`;
        averageWPMEle.innerText = `Average WPM: ${Math.floor(averageWPM * 100) / 100}`;
        testsTakenEle.innerText = `Tests Taken: ${testsTaken}`;

        new Chart(ctx, {
            data: {
                labels: Array.from({length: wpms.length}, (_, i) => i + 1),
                datasets: [
                    {
                        type: 'line',
                        label: 'WPM',
                        data: wpms,
                        borderColor: '#F4CE14'  
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });