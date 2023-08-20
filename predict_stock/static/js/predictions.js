function fetchPrediction() {
    const ticker = document.getElementById('tickerInput').value;
    if (!ticker) {
        alert('Please select a ticker.');
        return;
    }
    window.location.href = `/predict/${ticker}/`;
}

window.addEventListener('resize', adjustChartSize);

function adjustChartSize() {
    const containerHeight = document.querySelector('.chart-container').clientHeight;
    document.getElementById('predictionChart').style.height = `${containerHeight}px`;
}

adjustChartSize();
