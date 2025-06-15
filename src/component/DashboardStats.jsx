import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowUpRight, ArrowDownRight, Car, Users, DollarSign, Receipt } from "lucide-react"

const DashboardStats = ({vehicles, payments}) => {
    const drivers = new Set(vehicles.map(v => v.user.id)).size;
    const totalIncome = payments.filter(payment => payment.types === 'i').reduce((sum, payment) => sum + Number(payment.amount), 0);
    const totalTax = payments.filter(payment => payment.types === 't').reduce((sum, payment) => sum + Number(payment.amount), 0);
    const stats = {
      totalVehicles: vehicles.length,
      totalRevenue: totalIncome,
      taxCollected: totalTax,
      activeDrivers: drivers,
    }

    // Calculate percentage changes (mock data for now)
    const changes = {
      vehicles: 12,
      revenue: 8,
      tax: -3,
      drivers: 5
    }
  
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Vehicles</CardTitle>
            <Car className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalVehicles}</div>
            <div className="flex items-center pt-1">
              {changes.vehicles > 0 ? (
                <ArrowUpRight className="h-4 w-4 text-green-500" />
              ) : (
                <ArrowDownRight className="h-4 w-4 text-red-500" />
              )}
              <span className={`text-xs ${changes.vehicles > 0 ? 'text-green-500' : 'text-red-500'}`}>
                {Math.abs(changes.vehicles)}% from last month
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalRevenue.toLocaleString()} ETB</div>
            <div className="flex items-center pt-1">
              {changes.revenue > 0 ? (
                <ArrowUpRight className="h-4 w-4 text-green-500" />
              ) : (
                <ArrowDownRight className="h-4 w-4 text-red-500" />
              )}
              <span className={`text-xs ${changes.revenue > 0 ? 'text-green-500' : 'text-red-500'}`}>
                {Math.abs(changes.revenue)}% from last month
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tax Collected</CardTitle>
            <Receipt className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.taxCollected.toLocaleString()} ETB</div>
            <div className="flex items-center pt-1">
              {changes.tax > 0 ? (
                <ArrowUpRight className="h-4 w-4 text-green-500" />
              ) : (
                <ArrowDownRight className="h-4 w-4 text-red-500" />
              )}
              <span className={`text-xs ${changes.tax > 0 ? 'text-green-500' : 'text-red-500'}`}>
                {Math.abs(changes.tax)}% from last month
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Drivers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activeDrivers}</div>
            <div className="flex items-center pt-1">
              {changes.drivers > 0 ? (
                <ArrowUpRight className="h-4 w-4 text-green-500" />
              ) : (
                <ArrowDownRight className="h-4 w-4 text-red-500" />
              )}
              <span className={`text-xs ${changes.drivers > 0 ? 'text-green-500' : 'text-red-500'}`}>
                {Math.abs(changes.drivers)}% from last month
              </span>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }
  
  export default DashboardStats
  
  