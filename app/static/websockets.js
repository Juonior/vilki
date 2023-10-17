// websockets.js

const socket = io.connect(window.location.origin);

socket.on('connect', function () {
    console.log('Connected to the server.');
});

socket.on('update_events', function (data) {
    const eventsFlaskArray = data.events_flask;
    const tableBody = document.querySelector('tbody');
    tableBody.innerHTML = ''; // Clear the existing content

    eventsFlaskArray.forEach(newEvent => {
        const tableBody = document.querySelector('tbody');

        const currentTime = new Date(); // Current time

        const timeElapsed = Math.floor((currentTime - new Date(newEvent.time)) / 1000);

        const timeElapsedText = formatTimeElapsed(timeElapsed);

        const eventRow1 = document.createElement('tr');
        const eventData1 = [
            `<img src="/static/images/remove.png" alt="Игнорировать событие"><img src="/static/images/tennis.png" alt="Теннис"><br>${timeElapsedText}`,
            newEvent.profit,
            `<a href="${newEvent.link1}">${newEvent.site1}</a><br><a href="${newEvent.link2}">${newEvent.site2}</a>`,
            `<img src="/static/images/copy.png">${newEvent.matchName1}<br><img src="/static/images/copy.png">${newEvent.matchName2}`,
            `${newEvent.type1}<br>${newEvent.type2}`,
            `${newEvent.coefficient1}<br>${newEvent.coefficient2}`
        ];

        eventData1.forEach((data, index) => {
            const cell = document.createElement('td');
            const div = document.createElement('div');
            div.innerHTML = data;
            cell.appendChild(div);
            eventRow1.appendChild(cell);
        });

        tableBody.appendChild(eventRow1);
    });
});

function formatTimeElapsed(seconds) {
    if (seconds < 60) {
        if (seconds === 0) {
            return '0 сек';
        }
        return `${seconds} сек`;
    } else {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes} мин ${remainingSeconds} сек`;
    }
}
