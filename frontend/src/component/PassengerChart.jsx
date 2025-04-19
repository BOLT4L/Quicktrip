import { useEffect, useRef, useMemo } from "react";

const PassengerChart = ({ timeRange, passengerHistory }) => {
  const chartRef = useRef(null);

  // Process passenger data to group by time range
  const chartData = useMemo(() => {
    const groupedData = {
      labels: [],
      values: []
    };

    // Helper function to format dates and group by time range
    const groupByTimeRange = () => {
      const groups = {};

      passengerHistory?.forEach((trip) => {
        if (!trip?.ticket ) return;

        const tripDate = new Date(trip.time);
        let key;

        switch(timeRange) {
          case 'daily':
            key = tripDate.toLocaleDateString('en-US', { weekday: 'short' });
            break;
          case 'weekly':
            const weekNum = Math.ceil(tripDate.getDate() / 7);
            key = `Week ${weekNum}`;
            break;
          case 'monthly':
            key = tripDate.toLocaleDateString('en-US', { month: 'short' });
            break;
          case 'yearly':
            key = tripDate.getFullYear().toString();
            break;
          default:
            key = tripDate.toLocaleDateString();
        }

        if (!groups[key]) {
          groups[key] = new Set(); // Using Set to avoid counting duplicate users
        }

        if (trip?.ticket?.user) {
          groups[key].add(trip.ticket.user);
      }
      
      });

      return groups;
    };

    const groupedPassengers = groupByTimeRange();

    // Convert to chart data format
    Object.entries(groupedPassengers).forEach(([label, userSet]) => {
      groupedData.labels.push(label);
      groupedData.values.push(userSet.size); // Count unique users
    });

    return groupedData;
  }, [passengerHistory, timeRange]);

  useEffect(() => {
    if (!chartRef.current || !chartData.labels.length) return;

    const ctx = chartRef.current.getContext("2d");
    const width = chartRef.current.width;
    const height = chartRef.current.height;
    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;

    // Clear previous chart
    ctx.clearRect(0, 0, width, height);

    // Find max value for scaling (with 10% headroom)
    const maxValue = Math.max(...chartData.values, 1) * 1.1;

    // Draw axes and grid
    drawAxesAndGrid();
    
    // Draw chart line and points
    drawChartLine();
    
    // Draw area under line
    drawAreaUnderLine();

    function drawAxesAndGrid() {
      // Draw axes
      ctx.beginPath();
      ctx.moveTo(padding, padding);
      ctx.lineTo(padding, height - padding);
      ctx.lineTo(width - padding, height - padding);
      ctx.strokeStyle = "#e9ecef";
      ctx.stroke();

      // Draw grid lines and Y-axis labels
      const gridCount = 5;
      ctx.font = "10px Arial";
      ctx.fillStyle = "#6c757d";
      ctx.textAlign = "right";
      
      for (let i = 0; i <= gridCount; i++) {
        const value = Math.round((maxValue * i) / gridCount);
        const y = height - padding - (i / gridCount) * chartHeight;
        
        // Grid line
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.strokeStyle = "rgba(233, 236, 239, 0.5)";
        ctx.stroke();
        
        // Y-axis label
        ctx.fillText(value.toString(), padding - 10, y + 4);
      }

      // Draw x-axis labels
      ctx.font = "12px Arial";
      ctx.fillStyle = "#6c757d";
      ctx.textAlign = "center";

      chartData.labels.forEach((label, i) => {
        const x = padding + (i + 0.5) * (chartWidth / chartData.labels.length);
        ctx.fillText(label, x, height - padding + 20);
      });
    }

    function drawChartLine() {
      // Draw line
      ctx.beginPath();
      chartData.values.forEach((value, i) => {
        const x = padding + (i + 0.5) * (chartWidth / chartData.labels.length);
        const y = height - padding - (value / maxValue) * chartHeight;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.strokeStyle = "rgba(255, 0, 110, 0.7)";
      ctx.lineWidth = 3;
      ctx.stroke();

      // Draw points with value labels
      chartData.values.forEach((value, i) => {
        const x = padding + (i + 0.5) * (chartWidth / chartData.labels.length);
        const y = height - padding - (value / maxValue) * chartHeight;

        // Draw point
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(255, 0, 110, 0.7)";
        ctx.fill();
        ctx.strokeStyle = "white";
        ctx.lineWidth = 2;
        ctx.stroke();

        // Draw value above point
        ctx.font = "bold 10px Arial";
        ctx.fillStyle = "rgba(255, 0, 110, 1)";
        ctx.textAlign = "center";
        ctx.fillText(value.toString(), x, y - 10);
      });
    }

    function drawAreaUnderLine() {
      ctx.beginPath();
      chartData.values.forEach((value, i) => {
        const x = padding + (i + 0.5) * (chartWidth / chartData.labels.length);
        const y = height - padding - (value / maxValue) * chartHeight;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });

      // Complete the area path
      const lastX = padding + (chartData.values.length - 0.5) * (chartWidth / chartData.labels.length);
      ctx.lineTo(lastX, height - padding);
      ctx.lineTo(padding, height - padding);
      ctx.closePath();

      // Fill the area with gradient
      const gradient = ctx.createLinearGradient(0, height - padding, 0, padding);
      gradient.addColorStop(0, "rgba(255, 0, 110, 0.1)");
      gradient.addColorStop(1, "rgba(255, 0, 110, 0.3)");
      ctx.fillStyle = gradient;
      ctx.fill();
    }

  }, [timeRange, chartData]);

  return (
    <div style={{ position: 'relative' }}>
      <canvas 
        ref={chartRef} 
        width={600} 
        height={300} 
        style={{ 
          width: "100%", 
          height: "100%",
          backgroundColor: "white",
          borderRadius: "8px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
        }}
      />
      {chartData.labels.length === 0 && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
          color: '#6c757d'
        }}>
          No passenger data available for the selected time range
        </div>
      )}
    </div>
  );
};

export default PassengerChart;