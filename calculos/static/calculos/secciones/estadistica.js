// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('Cargando gráficos...');
    
    // Verificar si Chart.js está cargado
    if (typeof Chart === 'undefined') {
        console.error('Error: Chart.js no está cargado correctamente');
        return;
    }
    
    // 0. Gráfico de Estadística Descriptiva
    const descriptiveCtx = document.getElementById('descriptiveChart');
    if (descriptiveCtx) {
        console.log('Inicializando gráfico de estadística descriptiva...');
        new Chart(descriptiveCtx, {
            type: 'bar',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [{
                    label: 'Ventas 2023',
                    data: [65, 59, 80, 81, 56, 55],
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { 
                        display: true, 
                        text: 'Ejemplo: Ventas Mensuales',
                        font: { size: 14 }
                    },
                    legend: { display: false }
                },
                scales: {
                    y: { 
                        beginAtZero: true,
                        title: { display: true, text: 'Cantidad' }
                    }
                }
            }
        });
    }
    
    // 0.1 Gráfico de Estadística Inferencial
    const inferenceCtx = document.getElementById('inferenceChart');
    if (inferenceCtx) {
        console.log('Inicializando gráfico de estadística inferencial...');
        new Chart(inferenceCtx, {
            type: 'line',
            data: {
                labels: ['Muestra 1', 'Muestra 2', 'Muestra 3', 'Muestra 4', 'Muestra 5'],
                datasets: [{
                    label: 'Media de la muestra',
                    data: [45, 48, 50, 52, 49],
                    borderColor: 'rgba(153, 102, 255, 1)',
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    fill: true,
                    tension: 0.4
                }, {
                    label: 'Intervalo de confianza',
                    data: [47, 50, 52, 54, 51],
                    borderColor: 'rgba(255, 159, 64, 0.5)',
                    backgroundColor: 'rgba(255, 159, 64, 0.1)',
                    borderDash: [5, 5],
                    borderWidth: 1,
                    fill: 1
                }, {
                    label: '',
                    data: [43, 46, 48, 50, 47],
                    borderColor: 'rgba(255, 159, 64, 0.5)',
                    backgroundColor: 'rgba(255, 159, 64, 0.1)',
                    borderDash: [5, 5],
                    borderWidth: 1,
                    fill: '-1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { 
                        display: true, 
                        text: 'Estimación del Parámetro Poblacional',
                        font: { size: 14 }
                    }
                },
                scales: {
                    y: { 
                        beginAtZero: false,
                        title: { display: true, text: 'Valor' }
                    }
                }
            }
        });
    }
    
    // 0.2 Gráfico de Tipos de Datos
    const dataTypesCtx = document.getElementById('dataTypesChart');
    if (dataTypesCtx) {
        console.log('Inicializando gráfico de tipos de datos...');
        new Chart(dataTypesCtx, {
            type: 'doughnut',
            data: {
                labels: ['Cualitativos', 'Cuantitativos'],
                datasets: [{
                    data: [35, 65],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { 
                        display: true, 
                        text: 'Distribución de Tipos de Datos',
                        font: { size: 14 }
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // 1. Gráfico de Media
    const meanCtx = document.getElementById('meanChart');
    if (meanCtx) {
        console.log('Inicializando gráfico de media...');
        new Chart(meanCtx, {
            type: 'line',
            data: {
                labels: ['P1', 'P2', 'P3'],
                datasets: [{
                    label: 'Datos',
                    data: [5, 7, 9],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }, {
                    label: 'Media',
                    data: [7, 7, 7],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderDash: [5, 5],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' },
                    title: { display: true, text: 'Media Aritmética' }
                },
                scales: { y: { beginAtZero: true } }
            }
        });
    }


    // 2. Gráfico de Mediana
    const medianCtx = document.getElementById('medianChart');
    if (medianCtx) {
        console.log('Inicializando gráfico de mediana...');
        new Chart(medianCtx, {
            type: 'bar',
            data: {
                labels: ['1', '3', '3', '6', '7', '8', '9'],
                datasets: [{
                    label: 'Datos Ordenados',
                    data: [1, 3, 3, 6, 7, 8, 9],
                    backgroundColor: function(context) {
                        return context.dataIndex === 3 ? 'rgba(255, 99, 132, 0.7)' : 'rgba(54, 162, 235, 0.7)';
                    },
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: 'Mediana = 6' }
                },
                scales: { y: { beginAtZero: true } }
            }
        });
    }


    // 3. Gráfico de Moda
    const modeCtx = document.getElementById('modeChart');
    if (modeCtx) {
        console.log('Inicializando gráfico de moda...');
        new Chart(modeCtx, {
            type: 'bar',
            data: {
                labels: ['1', '2', '3', '4'],
                datasets: [{
                    label: 'Frecuencia',
                    data: [1, 2, 1, 1],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(54, 162, 235, 0.7)'
                    ],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: 'Moda = 2' }
                },
                scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
            }
        });
    }


    // 4. Gráfico de Rango
    const rangeCtx = document.getElementById('rangeChart');
    if (rangeCtx) {
        console.log('Inicializando gráfico de rango...');
        new Chart(rangeCtx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Datos',
                    data: [
                        {x: 1, y: 1}, {x: 2, y: 2}, {x: 3, y: 4}, 
                        {x: 4, y: 7}, {x: 5, y: 9}
                    ],
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    pointRadius: 8,
                    pointHoverRadius: 10
                }, {
                    label: 'Rango',
                    data: [
                        {x: 1, y: 1}, {x: 5, y: 9}
                    ],
                    type: 'line',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false,
                    showLine: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Rango = 9 - 1 = 8' },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Valor: (${context.parsed.x}, ${context.parsed.y})`;
                            }
                        }
                    }
                },
                scales: {
                    x: { 
                        min: 0, 
                        max: 6,
                        title: { display: true, text: 'Índice' }
                    },
                    y: { 
                        min: 0,
                        max: 10,
                        title: { display: true, text: 'Valor' }
                    }
                }
            }
        });
    }


    // 5. Gráfico de Varianza
    const varianceCtx = document.getElementById('varianceChart');
    if (varianceCtx) {
        console.log('Inicializando gráfico de varianza...');
        new Chart(varianceCtx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Datos',
                    data: [2, 4, 4, 4, 5, 5, 7, 9],
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    pointRadius: 8
                }, {
                    label: 'Media',
                    data: [{x: 0, y: 5}, {x: 8, y: 5}],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    type: 'line'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'Dispersión alrededor de la media' },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Valor: ${context.parsed.y}`;
                            }
                        }
                    }
                },
                scales: {
                    x: { 
                        display: false,
                        min: -1,
                        max: 9
                    },
                    y: { 
                        min: 0,
                        max: 10,
                        title: { display: true, text: 'Valores' }
                    }
                }
            }
        });
    }


    // 6. Gráfico de Coeficiente de Variación
    const cvCtx = document.getElementById('cvChart');
    if (cvCtx) {
        console.log('Inicializando gráfico de coeficiente de variación...');
        new Chart(cvCtx, {
            type: 'bar',
            data: {
                labels: ['Conjunto A', 'Conjunto B'],
                datasets: [{
                    label: 'Media',
                    data: [50, 100],
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                }, {
                    label: 'Desviación Estándar',
                    data: [10, 30],
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { 
                        display: true, 
                        text: 'Comparación de CV: A (20%) vs B (30%)' 
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    y: { 
                        beginAtZero: true,
                        title: { display: true, text: 'Valor' }
                    }
                }
            }
        });
    }


    // 7. Gráfico de distribución (reemplazo para el diagrama de caja)
    const boxplotCtx = document.getElementById('boxplotChart');
    if (boxplotCtx) {
        console.log('Inicializando gráfico de distribución...');
        
        // Datos de ejemplo para mostrar la distribución
        const data = [5, 7, 8, 8, 9, 10, 12, 12, 15];
        
        // Contar frecuencias
        const frequency = {};
        data.forEach(value => {
            frequency[value] = (frequency[value] || 0) + 1;
        });
        
        new Chart(boxplotCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(frequency),
                datasets: [{
                    label: 'Frecuencia',
                    data: Object.values(frequency),
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { 
                        display: true, 
                        text: 'Distribución de Datos (Alternativa al Boxplot)',
                        font: { size: 16 }
                    },
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Frecuencia: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    y: { 
                        beginAtZero: true,
                        title: { 
                            display: true, 
                            text: 'Frecuencia',
                            font: { weight: 'bold' }
                        },
                        ticks: {
                            stepSize: 1
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Valores',
                            font: { weight: 'bold' }
                        }
                    }
                }
            }
        });
    }
});
