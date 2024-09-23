// Gender Distribution Chart
const genderData = {{ gender_distribution|safe }};
const genderCtx = document.getElementById('genderDistributionChart').getContext('2d');
new Chart(genderCtx, {
    type: 'pie',
    data: {
        labels: genderData.map(item => item.gender),
        datasets: [{
            data: genderData.map(item => item.count),
            backgroundColor: ['#36A2EB', '#FF6384']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Farmer Gender Distribution'
            }
        }
    }
});

// Top Countries Chart
const countryData = {{ top_cities|safe }};
const countriesCtx = document.getElementById('topCountriesChart').getContext('2d');
new Chart(countriesCtx, {
    type: 'bar',
    data: {
        labels: countryData.map(item => item.partner__country),
        datasets: [{
            label: 'Number of Farmers',
            data: countryData.map(item => item.count),
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: 'Top 10 Countries by Farmer Count'
            }
        }
    }
});

// Top Partners Chart
const partnerData = {{ top_partners|safe }};
const partnersCtx = document.getElementById('topPartnersChart').getContext('2d');
new Chart(partnersCtx, {
    type: 'bar',
    data: {
        labels: partnerData.map(item => item.name),
        datasets: [{
            label: 'Number of Farmers',
            data: partnerData.map(item => item.farmer_count),
            backgroundColor: 'rgba(153, 102, 255, 0.6)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        scales: {
            x: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: 'Top 10 Partners by Farmer Count'
            }
        }
    }
});

// Events Over Time Chart
const eventsData = {{ events_over_time|safe }};
const eventsCtx = document.getElementById('eventsOverTimeChart').getContext('2d');
new Chart(eventsCtx, {
    type: 'line',
    data: {
        labels: eventsData.map(item => new Date(item.month).toLocaleDateString('default', { month: 'short', year: 'numeric' })),
        datasets: [{
            label: 'Number of Events',
            data: eventsData.map(item => item.count),
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Events Over Time'
            }
        }
    }
});

// Crop Distribution Chart
const cropData = {{ crop_distribution|safe }};
const cropCtx = document.getElementById('cropDistributionChart').getContext('2d');
new Chart(cropCtx, {
    type: 'pie',
    data: {
        labels: Object.keys(cropData),
        datasets: [{
            data: Object.values(cropData),
            backgroundColor: [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#9966FF'
            ]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Crop Distribution'
            }
        }
    }
});

// Farmers Reached Chart
const farmersReachedData = {{ farmers_reached|safe }};
const farmersReachedCtx = document.getElementById('farmersReachedChart').getContext('2d');
new Chart(farmersReachedCtx, {
    type: 'bar',
    data: {
        labels: ['Male', 'Female'],
        datasets: [{
            label: 'Farmers Reached',
            data: [farmersReachedData.male, farmersReachedData.female],
            backgroundColor: ['#36A2EB', '#FF6384']
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Farmers Reached Through Dissemination'
            }
        }
    }
});