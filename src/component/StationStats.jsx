import { useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function StationStats({ station, passengers, vehicles, report }) {
  // Get monthly data for the past 6 months
  const getMonthlyData = () => {
    const months = [];
    const passengerCounts = [];
    const revenueCounts = [];

    for (let i = 5; i >= 0; i--) {
      const date = new Date();
      date.setMonth(date.getMonth() - i);
      const monthYear = date.toLocaleString('default', { month: 'short', year: '2-digit' });
      months.push(monthYear);

      // Count passengers for this month
      const monthPassengers = passengers.filter(p => {
        if (!p.travel_history?.length) return false;
        return p.travel_history.some(h => {
          const historyDate = new Date(h.date);
          return historyDate.getMonth() === date.getMonth() &&
                 historyDate.getFullYear() === date.getFullYear() &&
                 h.branch === station.id;
        });
      }).length;
      passengerCounts.push(monthPassengers);

      // Calculate revenue for this month
      const monthRevenue = report.reduce((sum, rev) => {
        if (rev.branch === station.id && rev.types === 'i') {
          const revenueDate = new Date(rev.date);
          if (revenueDate.getMonth() === date.getMonth() &&
              revenueDate.getFullYear() === date.getFullYear()) {
            return sum + Number(rev.amount);
          }
        }
        return sum;
      }, 0);
      revenueCounts.push(monthRevenue);
    }

    return { months, passengerCounts, revenueCounts };
  };

  const { months, passengerCounts, revenueCounts } = getMonthlyData();

  const passengerData = {
    labels: months,
    datasets: [
      {
        label: 'Monthly Passengers',
        data: passengerCounts,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        tension: 0.4,
      },
    ],
  };

  const revenueData = {
    labels: months,
    datasets: [
      {
        label: 'Monthly Revenue (ETB)',
        data: revenueCounts,
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgb(54, 162, 235)',
        borderWidth: 1,
      },
    ],
  };

  // Vehicle distribution by type
  const vehicleTypes = vehicles
    .filter(v => v.branch.id === station.id)
    .reduce((acc, vehicle) => {
      acc[vehicle.type] = (acc[vehicle.type] || 0) + 1;
      return acc;
    }, {});

  const vehicleData = {
    labels: Object.keys(vehicleTypes).map(type => type.toUpperCase()),
    datasets: [
      {
        data: Object.values(vehicleTypes),
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  return (
    <div className="stats-container">
      <div className="chart-row">
        <div className="chart-container">
          <h3>Passenger Trends</h3>
          <div className="chart-wrapper">
            <Line data={passengerData} options={chartOptions} />
          </div>
        </div>
        <div className="chart-container">
          <h3>Revenue Analysis</h3>
          <div className="chart-wrapper">
            <Bar data={revenueData} options={chartOptions} />
          </div>
        </div>
      </div>
      <div className="chart-row">
        <div className="chart-container">
          <h3>Vehicle Distribution</h3>
          <div className="chart-wrapper donut-wrapper">
            <Doughnut data={vehicleData} options={{
              ...chartOptions,
              plugins: {
                ...chartOptions.plugins,
                legend: {
                  ...chartOptions.plugins.legend,
                  position: 'right',
                },
              },
            }} />
          </div>
        </div>
      </div>

      <style jsx>{`
        .stats-container {
          margin-top: 30px;
          padding: 20px;
          background-color: var(--bg-secondary);
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .chart-row {
          display: flex;
          gap: 20px;
          margin-bottom: 20px;
        }

        .chart-container {
          flex: 1;
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .chart-container h3 {
          margin: 0 0 15px 0;
          color: var(--text-primary);
          font-size: 1.1rem;
          font-weight: 600;
        }

        .chart-wrapper {
          height: 300px;
          position: relative;
        }

        .donut-wrapper {
          height: 400px;
        }

        @media (max-width: 992px) {
          .chart-row {
            flex-direction: column;
          }

          .chart-container {
            margin-bottom: 20px;
          }
        }
      `}</style>
    </div>
  );
}

export default StationStats; 