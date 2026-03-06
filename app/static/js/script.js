// Configuración de colores
const colors = {
    red: '#dc2626',
    redLight: '#fca5a5',
    redLighter: '#fecaca',
    redLightest: '#fee2e2'
};

// Datos para gráficos
const ventasData = {
    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    datasets: [{
        label: 'Ventas',
        data: [45000, 52000, 48000, 61000, 55000, 67000],
        backgroundColor: '#dc2626',
        borderRadius: 4,
        barThickness: 40
    }]
};

const pedidosData = {
    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    datasets: [{
        label: 'Pedidos',
        data: [45, 52, 48, 61, 55, 67],
        borderColor: '#dc2626',
        backgroundColor: 'rgba(220, 38, 38, 0.1)',
        borderWidth: 2,
        pointBackgroundColor: '#dc2626',
        pointBorderColor: '#dc2626',
        pointRadius: 4,
        tension: 0.4,
        fill: false
    }]
};

const categoriaData = {
    labels: ['Filtros', 'Frenos', 'Eléctrico', 'Suspensión', 'Motor'],
    datasets: [{
        data: [650, 520, 480, 390, 320],
        backgroundColor: [
            '#dc2626',
            '#ef4444',
            '#f87171',
            '#fca5a5',
            '#fecaca'
        ],
        borderWidth: 0
    }]
};

// Opciones comunes
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false
        }
    },
    scales: {
        x: {
            grid: {
                display: false
            },
            ticks: {
                font: {
                    size: 12
                },
                color: '#6b7280'
            }
        },
        y: {
            grid: {
                color: '#f3f4f6',
                drawBorder: false
            },
            ticks: {
                font: {
                    size: 12
                },
                color: '#6b7280',
                callback: function(value) {
                    return value >= 1000 ? (value / 1000) + 'k' : value;
                }
            }
        }
    }
};

// Inicializar gráficos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de Ventas
    const ventasCtx = document.getElementById('ventasChart');
    if (ventasCtx) {
        new Chart(ventasCtx, {
            type: 'bar',
            data: ventasData,
            options: {
                ...commonOptions,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + context.parsed.y.toLocaleString();
                            }
                        }
                    },
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Gráfico de Pedidos
    const pedidosCtx = document.getElementById('pedidosChart');
    if (pedidosCtx) {
        new Chart(pedidosCtx, {
            type: 'line',
            data: pedidosData,
            options: {
                ...commonOptions,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y + ' pedidos';
                            }
                        }
                    },
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Gráfico de Categorías (Pie)
    const categoriaCtx = document.getElementById('categoriaChart');
    if (categoriaCtx) {
        new Chart(categoriaCtx, {
            type: 'doughnut',
            data: categoriaData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            pointStyle: 'rectRounded',
                            padding: 15,
                            font: {
                                size: 12
                            },
                            generateLabels: function(chart) {
                                const data = chart.data;
                                return data.labels.map((label, i) => ({
                                    text: label + '  ' + data.datasets[0].data[i] + ' ventas',
                                    fillStyle: data.datasets[0].backgroundColor[i],
                                    strokeStyle: data.datasets[0].backgroundColor[i],
                                    lineWidth: 0,
                                    index: i,
                                    fontColor: '#6b7280'
                                }));
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + ' ventas';
                            }
                        }
                    }
                }
            }
        });
    }
});