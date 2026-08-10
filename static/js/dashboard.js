document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // PREDICTION TREND CHART
    // =====================================================

    const predictionCanvas = document.getElementById("predictionChart");

    if (predictionCanvas) {

        const predictionCtx = predictionCanvas.getContext("2d");

        // Gradient for professional look
        const gradient = predictionCtx.createLinearGradient(
            0,
            0,
            0,
            350
        );

        gradient.addColorStop(0, "rgba(37, 99, 235, 0.30)");
        gradient.addColorStop(1, "rgba(37, 99, 235, 0.02)");

        new Chart(predictionCanvas, {

            type: "line",

            data: {

                labels: predictionLabels,

                datasets: [

                    {
                        label: "Predicted Score",

                        data: predictionScores,

                        borderColor: "#2563eb",

                        backgroundColor: gradient,

                        borderWidth: 3,

                        fill: true,

                        tension: 0.4,

                        pointBackgroundColor: "#2563eb",

                        pointBorderColor: "#ffffff",

                        pointBorderWidth: 2,

                        pointRadius: 5,

                        pointHoverRadius: 8
                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                interaction: {
                    intersect: false,
                    mode: "index"
                },

                plugins: {

                    legend: {
                        display: true,

                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },

                    tooltip: {

                        backgroundColor: "#111827",

                        titleColor: "#ffffff",

                        bodyColor: "#ffffff",

                        padding: 12,

                        displayColors: false,

                        callbacks: {

                            label: function (context) {

                                return " Score: "
                                    + context.parsed.y
                                    + "%";

                            }

                        }

                    }

                },

                scales: {

                    x: {

                        grid: {
                            display: false
                        },

                        ticks: {
                            color: "#6b7280"
                        }

                    },

                    y: {

                        min: 0,

                        max: 100,

                        ticks: {

                            stepSize: 20,

                            color: "#6b7280",

                            callback: function (value) {

                                return value + "%";

                            }

                        },

                        grid: {

                            color: "rgba(107, 114, 128, 0.12)"

                        }

                    }

                }

            }

        });

    }


    // =====================================================
    // RISK ANALYSIS CHART
    // =====================================================

    const riskCanvas = document.getElementById("riskChart");

    if (riskCanvas) {

        new Chart(riskCanvas, {

            type: "doughnut",

            data: {

                labels: [

                    "Low Risk",

                    "Medium Risk",

                    "High Risk"

                ],

                datasets: [

                    {

                        data: [

                            riskData.low,

                            riskData.medium,

                            riskData.high

                        ],

                        backgroundColor: [

                            "#22c55e",

                            "#f59e0b",

                            "#ef4444"

                        ],

                        borderWidth: 0,

                        hoverOffset: 8

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "68%",

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            padding: 20,

                            usePointStyle: true,

                            font: {
                                size: 13
                            }

                        }

                    },

                    tooltip: {

                        backgroundColor: "#111827",

                        titleColor: "#ffffff",

                        bodyColor: "#ffffff",

                        padding: 12

                    }

                }

            }

        });

    }

});