import { useState, useEffect} from "react"
import Sidebar from "../../component/sidebar"
import Header from "../../component/Header"
import ReportChart from "../../component/ReportChart"
import ReceiptGenerator from "../../component/ReceiptGenerator"
import RevenueChart from "../../component/RevenueChart"
import api from "../../api"
export default function Revenue() {
  
  const [report, setReport] = useState([]);
  const [reportType, setReportType] = useState("revenue")
  const [timeRange, setTimeRange] = useState("monthly")
  const [showReceiptGenerator, setShowReceiptGenerator] = useState(false)
 
  useEffect(()=>{
    getReport()
  },[])
  const getReport = () => {
    api
      .get('api/payments/')
      .then((res) => res.data)
      .then((data) => {
        setReport(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };
  const totalRevenue = report.reduce((sum, payment) => {

    if (payment.types === 'i') {  // or whatever field indicates income
      const amount = typeof payment.amount === 'string' 
        ? parseFloat(payment.amount.replace(/[^0-9.-]/g, '')) 
        : payment.amount;
        
      return sum + (amount || 0);
    }
    return sum;  // Skip non-income payments
  }, 0);
  const totalExpense = report.reduce((sum, payment) => {

    if (payment.types === 'e') {  // or whatever field indicates income
      const amount = typeof payment.amount === 'string' 
        ? parseFloat(payment.amount.replace(/[^0-9.-]/g, '')) 
        : payment.amount;
        
      return sum + (amount || 0);
    }
    return sum;  // Skip non-income payments
  }, 0);
  const totaltax= report.reduce((sum, payment) => {

    if (payment.types === 't') {  // or whatever field indicates income
      const amount = typeof payment.amount === 'string' 
        ? parseFloat(payment.amount.replace(/[^0-9.-]/g, '')) 
        : payment.amount;
        
      return sum + (amount || 0);
    }
    return sum;  // Skip non-income payments
  }, 0);
  return (
    <div className="reports-page">
        <Sidebar/>
        <div className="right">
            <Header/>
      <div className="page-header">
        <h1>Reports & Analytics</h1>
        <button className="btn btn-primary" onClick={() => setShowReceiptGenerator(true)}>
          Generate Receipt
        </button>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="report-controls">
          
            <div className="time-range-selector">
              <label htmlFor="timeRange" className="control-label">
                Time Range:
              </label>
              <select
                id="timeRange"
                className="form-control"
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
              >
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
              </select>
            </div>
          </div>
        </div>

        <div className="chart-container">
        <RevenueChart timeRange={timeRange}  payments = {report}  />
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Summary Statistics</h2>
          </div>
          <div className="card-content">
            <div className="summary-stats">
              <div className="stat-item">
                <span className="stat-label">Total Revenue</span>
                <span className="stat-value">${totalRevenue}</span>
                <span className="stat-change positive">+12.5%</span>
              </div>

              <div className="stat-item">
                <span className="stat-label">Total Expense</span>
                <span className="stat-value">${totalExpense}</span>
                <span className="stat-change positive">+8.3%</span>
              </div>

              <div className="stat-item">
                <span className="stat-label">Total Passengers</span>
                <span className="stat-value">12,450</span>
                <span className="stat-change positive">+15.2%</span>
              </div>

              <div className="stat-item">
                <span className="stat-label">Tax Collected</span>
                <span className="stat-value">${totaltax}</span>
                <span className="stat-change positive">+10.7%</span>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Recent Reports</h2>
          </div>
          <div className="card-content">
            <div className="recent-reports">
              <div className="report-item">
                <div className="report-icon">📊</div>
                <div className="report-details">
                  <h3>Monthly Revenue Report</h3>
                  <p>October 2023</p>
                </div>
                <button className="btn btn-sm btn-outline">Download</button>
              </div>

              <div className="report-item">
                <div className="report-icon">🚗</div>
                <div className="report-details">
                  <h3>Vehicle Registration Report</h3>
                  <p>Q3 2023</p>
                </div>
                <button className="btn btn-sm btn-outline">Download</button>
              </div>

              <div className="report-item">
                <div className="report-icon">💰</div>
                <div className="report-details">
                  <h3>Tax Collection Report</h3>
                  <p>September 2023</p>
                </div>
                <button className="btn btn-sm btn-outline">Download</button>
              </div>

              <div className="report-item">
                <div className="report-icon">👥</div>
                <div className="report-details">
                  <h3>Passenger Analytics</h3>
                  <p>August 2023</p>
                </div>
                <button className="btn btn-sm btn-outline">Download</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {showReceiptGenerator && <ReceiptGenerator onClose={() => setShowReceiptGenerator(false)} />}
      </div>
      <style jsx>{`
        .reports-page{
          display: flex;
        }
          .right {
            display: flex;
          flex-direction : column;
          width :100%;
          margin: 10px;
          }
        .page-header {
          display: flex;

          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }
        
        .report-controls {
          display: flex;
          gap: 20px;
          flex-wrap: wrap;
        }
        
        .control-label {
          display: block;
          margin-bottom: 5px;
          font-weight: 500;
        }
        
        .chart-container {
          height: 400px;
          padding: 20px;
        }
        
        .card-content {
          padding: 20px;
        }
        
        .summary-stats {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 20px;
        }
        
        .stat-item {
          display: flex;
          flex-direction: column;
          padding: 15px;
          background-color: rgba(0, 0, 0, 0.02);
          border-radius: 8px;
        }
        
        .stat-label {
          font-size: 0.875rem;
          color: var(--text-light);
        }
        
        .stat-value {
          font-size: 1.5rem;
          font-weight: 600;
          margin: 5px 0;
        }
        
        .stat-change {
          font-size: 0.875rem;
          font-weight: 500;
        }
        
        .stat-change.positive {
          color: var(--success-color);
        }
        
        .stat-change.negative {
          color: var(--danger-color);
        }
        
        .recent-reports {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }
        
        .report-item {
          display: flex;
          align-items: center;
          padding: 10px;
          border-radius: 8px;
          background-color: rgba(0, 0, 0, 0.02);
        }
        
        .report-icon {
          font-size: 1.5rem;
          margin-right: 15px;
        }
        
        .report-details {
          flex: 1;
        }
        
        .report-details h3 {
          font-size: 1rem;
          margin: 0;
        }
        
        .report-details p {
          font-size: 0.875rem;
          color: var(--text-light);
          margin: 0;
        }
        
        .btn-outline {
          background-color: transparent;
          border: 1px solid var(--primary-color);
          color: var(--primary-color);
        }
        
        .btn-outline:hover {
          background-color: rgba(58, 134, 255, 0.1);
        }
        
        .btn-sm {
          padding: 0.25rem 0.5rem;
          font-size: 0.875rem;
        }
        
        @media (max-width: 768px) {
          .summary-stats {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  )
}

