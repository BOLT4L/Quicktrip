import { useEffect, useRef, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Line, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const RevenueChart = ({ timeRange, payments }) => {
  const chartRef = useRef(null);

  // Group payments by time range
  const chartData = useMemo(() => {
    const groupedData = {
      labels: [],
      revenue: [],
      expenses: []
    };

    // Helper function to format dates
    const formatDate = (date, range) => {
      const d = new Date(date);
      switch(range) {
        case 'daily':
          return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        case 'weekly':
          const weekStart = new Date(d);
          weekStart.setDate(d.getDate() - d.getDay()); // Start of week (Sunday)
          const weekEnd = new Date(weekStart);
          weekEnd.setDate(weekStart.getDate() + 6);
          return `${weekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${weekEnd.toLocaleDateString('en-US', { day: 'numeric' })}`;
        case 'monthly':
          return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
        case 'yearly':
          return d.getFullYear().toString();
        default:
          return d.toLocaleDateString();
      }
    };

    // Helper function to get week key for grouping
    const getWeekKey = (date) => {
      const d = new Date(date);
      const weekStart = new Date(d);
      weekStart.setDate(d.getDate() - d.getDay()); // Start of week (Sunday)
      return weekStart.toISOString().split('T')[0]; // YYYY-MM-DD format
    };

    // Get min and max dates from payments
    const dates = payments.map(p => new Date(p.date));
    const minDate = new Date(Math.min(...dates));
    const maxDate = new Date(Math.max(...dates));

    // Generate all possible time periods in the range
    const allPeriods = [];
    const current = new Date(minDate);

    while (current <= maxDate) {
      let periodDate = new Date(current);
      let key;
      
      if (timeRange === 'weekly') {
        key = getWeekKey(periodDate);
        // Advance to next week
        current.setDate(current.getDate() + 7);
      } else if (timeRange === 'monthly') {
        key = formatDate(periodDate, timeRange);
        // Advance to next month
        current.setMonth(current.getMonth() + 1);
      } else if (timeRange === 'yearly') {
        key = formatDate(periodDate, timeRange);
        // Advance to next year
        current.setFullYear(current.getFullYear() + 1);
      } else {
        // Daily
        key = formatDate(periodDate, timeRange);
        // Advance to next day
        current.setDate(current.getDate() + 1);
      }

      if (!allPeriods.some(p => p.key === key)) {
        allPeriods.push({
          key,
          date: new Date(periodDate),
          revenue: 0,
          expenses: 0
        });
      }
    }

    // Group payments by time range
    payments.forEach(payment => {
      const paymentDate = new Date(payment.date);
      let key;
      
      if (timeRange === 'weekly') {
        key = getWeekKey(paymentDate);
      } else {
        key = formatDate(paymentDate, timeRange);
      }

      const period = allPeriods.find(p => p.key === key);
      if (period) {
        if (payment.types === 'i') {  
          period.revenue += Number(payment.amount);
        } else {
          period.expenses += Number(payment.amount);
        }
      }
    });

    // Sort periods by date and convert to chart data format
    allPeriods
      .sort((a, b) => a.date - b.date)
      .forEach(({ key, revenue, expenses }) => {
        groupedData.labels.push(key);
        groupedData.revenue.push(revenue);
        groupedData.expenses.push(expenses);
      });

    return groupedData;
  }, [payments, timeRange]);

  const revenueData = {
    labels: chartData.labels,
    datasets: [
      {
        label: 'Revenue',
        data: chartData.revenue,
        borderColor: 'rgb(58, 134, 255)',
        backgroundColor: 'rgba(58, 134, 255, 0.1)',
        tension: 0.4,
        fill: true,
      },
      {
        label: 'Expenses',
        data: chartData.expenses,
        borderColor: 'rgb(131, 56, 236)',
        backgroundColor: 'rgba(131, 56, 236, 0.1)',
        tension: 0.4,
        fill: true,
      }
    ],
  };

  const barData = {
    labels: chartData.labels,
    datasets: [
      {
        label: 'Revenue',
        data: chartData.revenue,
        backgroundColor: 'rgba(58, 134, 255, 0.7)',
      },
      {
        label: 'Expenses',
        data: chartData.expenses,
        backgroundColor: 'rgba(131, 56, 236, 0.7)',
      }
    ],
  };

  const options = {
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
        ticks: {
          callback: function(value) {
            return value.toLocaleString() + ' ETB';
          }
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Revenue Overview</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="line" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="line">Line Chart</TabsTrigger>
            <TabsTrigger value="bar">Bar Chart</TabsTrigger>
          </TabsList>
          <TabsContent value="line" className="h-[400px]">
            <Line data={revenueData} options={options} />
          </TabsContent>
          <TabsContent value="bar" className="h-[400px]">
            <Bar data={barData} options={options} />
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};

export default RevenueChart;