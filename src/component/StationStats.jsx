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
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

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
        backgroundColor: 'rgba(75, 192, 192, 0.1)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const revenueData = {
    labels: months,
    datasets: [
      {
        label: 'Monthly Revenue (ETB)',
        data: revenueCounts,
        backgroundColor: 'rgba(54, 162, 235, 0.7)',
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
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  };

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Passenger Trends</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px]">
            <Line data={passengerData} options={chartOptions} />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Revenue Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px]">
            <Bar data={revenueData} options={chartOptions} />
          </div>
        </CardContent>
      </Card>

      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle>Vehicle Distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[400px] flex justify-center">
            <div className="w-[400px]">
              <Doughnut 
                data={vehicleData} 
                options={{
                  ...chartOptions,
                  plugins: {
                    ...chartOptions.plugins,
                    legend: {
                      ...chartOptions.plugins.legend,
                      position: 'right',
                    },
                  },
                }} 
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default StationStats; 