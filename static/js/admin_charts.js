function renderCharts(userData, entryData) {
    const userChartContext = document.getElementById('userChart').getContext('2d');
    const entryChartContext = document.getElementById('entryChart').getContext('2d');

    const userChart = new Chart(userChartContext, {
        type: 'bar',
        data: {
            labels: userData.map(user => user.username),
            datasets: [{
                label: '# of Entries',
                data: userData.map(user => entryData.filter(entry => entry.user_id === user._id).length),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const entryChart = new Chart(entryChartContext, {
        type: 'pie',
        data: {
            labels: userData.map(user => user.username),
            datasets: [{
                label: '# of Entries',
                data: userData.map(user => entryData.filter(entry => entry.user_id === user._id).length),
                backgroundColor: userData.map((_, index) => `hsl(${index * 30}, 100%, 50%)`),
                borderColor: 'rgba(255, 255, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
}
