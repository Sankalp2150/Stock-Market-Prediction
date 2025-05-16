async function predictPrice() {
  const symbol = document.getElementById("symbol").value.toUpperCase();

  if (!symbol) {
    alert("Please enter a stock symbol");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ symbol }),
    });

    const result = await response.json();
    console.log("API Response:", result);

    if (result.status === "success") {
      document.getElementById("prediction-result").innerHTML = `
        <div class="glass result-box">
          <h3>📈 Prediction for ${symbol}</h3>
          <p><strong>Predicted Price:</strong> $${result.predicted_price}</p>
          <p><strong>Model Accuracy:</strong> ${result.accuracy.toFixed(2)}%</p>
        </div>
      `;
      // Plotly chart rendering logic
      const chartData = result.chart;
      if (chartData && chartData.dates.length > 0) {
        const actualTrace = {
          x: chartData.dates,
          y: chartData.actual,
          mode: 'lines+markers',
          name: 'Actual Price',
          line: { color: 'blue', width: 3 },
          marker: { size: 6 }
        };

        const predictedTrace = {
          x: chartData.dates,
          y: chartData.predicted,
          mode: 'lines+markers',
          name: 'Predicted Price',
          line: { color: 'green', width: 2, dash: 'dash', opacity: 0.7 },
          marker: { size: 4, opacity: 0.7 }
        };

        const layout = {
          title: `📊 Accuracy Comparison for ${symbol}`,
          xaxis: { title: 'Date' },
          yaxis: { title: 'Price ($)' },
          template: 'plotly_dark',
          legend: { orientation: 'h', y: -0.2 }
        };

        Plotly.newPlot("predictionPlot", [actualTrace, predictedTrace], layout);
      } else {
        document.getElementById("predictionPlot").innerHTML = "<p>No historical data to display.</p>";
      }
    } else {
      document.getElementById("prediction-result").innerHTML = `
        <div class="glass result-box error">
          <p>❌ ${result.message}</p>
        </div>
      `;
    }
  } catch (error) {
    console.error("Prediction error:", error);
    document.getElementById("prediction-result").innerHTML = `
      <div class="glass result-box error">
        <p>❌ An error occurred while fetching prediction.</p>
      </div>
    `;
  }
}