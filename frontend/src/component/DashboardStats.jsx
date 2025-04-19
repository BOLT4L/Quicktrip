
const DashboardStats = ({vehicles , payments}) => {
    const drivers = new Set(vehicles.map(v => v.user.id)).size;
    const totalIncome = payments.filter(payment => payment.types === 'i').reduce((sum, payment) => sum + Number(payment.amount), 0);
    const totalTax =  payments.filter(payment => payment.types === 't').reduce((sum, payment) => sum + Number(payment.amount), 0);
    const stats = {
      totalVehicles: vehicles.length,
      totalRevenue: totalIncome,
      taxCollected: totalTax ,
      activeDrivers: drivers,
    }
  
    return (
      <div className="grid grid-4">
        <div className="stat-card">
          <div className="stat-icon blue">🚗</div>
          <div className="stat-content">
            <h3>{stats.totalVehicles}</h3>
            <p>Total Vehicles</p>
          </div>
        </div>
  
        <div className="stat-card">
          <div className="stat-icon purple">💰</div>
          <div className="stat-content">
            <h3>${stats.totalRevenue}</h3>
            <p>Total Revenue</p>
          </div>
        </div>
  
        <div className="stat-card">
          <div className="stat-icon pink">📊</div>
          <div className="stat-content">
            <h3>${stats.taxCollected.toLocaleString()}</h3>
            <p>Tax Collected</p>
          </div>
        </div>
  
        <div className="stat-card">
          <div className="stat-icon green">👤</div>
          <div className="stat-content">
            <h3>{stats.activeDrivers}</h3>
            <p>Active Drivers</p>
          </div>
        </div>
      </div>
    )
  }
  
  export default DashboardStats
  
  