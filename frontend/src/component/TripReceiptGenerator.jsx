
import { useRef, useState } from "react"

const TripReceiptGenerator = ({ trip, passenger, onClose }) => {
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const receiptRef = useRef(null)

  const handleDownload = () => {
    setLoading(true)

    // In a real app, this would use a library like jsPDF to generate a PDF
    // For this demo, we'll simulate the PDF generation with a timeout
    setTimeout(() => {
      setLoading(false)
      setSuccess(true)

      // Reset success message after 3 seconds
      setTimeout(() => {
        setSuccess(false)
      }, 3000)
    }, 1500)
  }

  return (
    <div className="modal-backdrop">
      <div className="modal receipt-modal">
        <div className="modal-header">
          <h2 className="modal-title">Trip Receipt</h2>
          <button className="modal-close" onClick={onClose}>
            &times;
          </button>
        </div>

        <div className="modal-body">
          <div className="receipt" ref={receiptRef}>
            <div className="receipt-header">
              <h1 className="company-name">QuickTrip</h1>
              <p className="company-tagline">Vehicle Management System</p>
            </div>

            <div className="receipt-title">
              <h2>TRIP RECEIPT</h2>
              <div className="receipt-number">#{trip.id}</div>
            </div>

            <div className="receipt-details">
              <div className="detail-row">
                <span className="detail-label">Date:</span>
                <span className="detail-value"></span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Status:</span>
                <span className="detail-value status-completed">
                  Not used
                </span>
              </div>
            </div>

            <div className="receipt-section">
              <h3>Passenger Information</h3>
              <div className="detail-row">
                <span className="detail-label">Name:</span>
                <span className="detail-value">{passenger.nid.Fname}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">ID:</span>
                <span className="detail-value">{passenger.nid.FAN}</span>
              </div>
            </div>

            <div className="receipt-section">
              <h3>Trip Details</h3>
              <div className="trip-route">
                <div className="route-station">
                  <div className="station-marker start"></div>
                  <div className="station-details">
                    <div className="station-name">{trip.ticket.route.first_destination.name}</div>
                    <div className="station-time">Departure</div>
                  </div>
                </div>
                <div className="route-line"></div>
                <div className="route-station">
                  <div className="station-marker end"></div>
                  <div className="station-details">
                    <div className="station-name">{trip.ticket.route.last_destination.name}</div>
                    <div className="station-time">Arrival</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="receipt-section">
              <h3>Vehicle & Driver</h3>
              <div className="detail-row">
                <span className="detail-label">Vehicle:</span>
                <span className="detail-value">{trip.vehicle.name}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Driver:</span>
                <span className="detail-value">{trip.vehicle.user.employee.Fname}</span>
              </div>
            </div>

            <div className="receipt-payment">
              <div className="payment-row">
                <span className="payment-label">Fare:</span>
                <span className="payment-value">${trip.payment.amount}</span>
              </div>
              <div className="payment-row">
                <span className="payment-label">Tax (15%):</span>
                <span className="payment-value">${(trip.payment.amount * 0.15)}</span>
              </div>
              <div className="payment-row total">
                <span className="payment-label">Total:</span>
                <span className="payment-value">${(trip.payment.amount * 1.15)}</span>
              </div>
            </div>

            <div className="receipt-footer">
              <p>Thank you for choosing QuickTrip!</p>
              <p className="small">This is an official receipt from QuickTrip Vehicle Management System.</p>
              <div className="receipt-barcode">*QT{trip.id}*</div>
            </div>
          </div>

          <div className="receipt-actions">
            {success ? (
              <div className="success-message">
                <div className="success-icon">✓</div>
                <p>Receipt downloaded successfully!</p>
              </div>
            ) : (
              <button
                className={`btn btn-primary download-btn ${loading ? "loading" : ""}`}
                onClick={handleDownload}
                disabled={loading}
              >
                {loading ? "Generating PDF..." : "Download PDF Receipt"}
              </button>
            )}
            <button className="btn btn-outline" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>

      <style jsx>{`
        .receipt-modal {
          max-width: 600px;
        }
        
        .receipt {
          background-color: white;
          padding: 30px;
          border: 1px solid var(--border-color);
          border-radius: 8px;
          margin-bottom: 20px;
        }
        
        .receipt-header {
          text-align: center;
          margin-bottom: 20px;
        }
        
        .company-name {
          font-size: 2rem;
          margin: 0;
          color: var(--primary-color);
        }
        
        .company-tagline {
          margin: 0;
          color: var(--text-light);
        }
        
        .receipt-title {
          text-align: center;
          margin-bottom: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 15px;
        }
        
        .receipt-title h2 {
          display: inline-block;
          padding: 5px 20px;
          border: 2px solid var(--primary-color);
          color: var(--primary-color);
          margin: 0;
        }
        
        .receipt-number {
          font-size: 1.1rem;
          font-weight: 600;
          color: var(--text-secondary);
        }
        
        .receipt-details, .receipt-section {
          margin-bottom: 20px;
        }
        
        .receipt-section h3 {
          font-size: 1.1rem;
          padding-bottom: 5px;
          border-bottom: 1px solid var(--border-color);
          margin-bottom: 10px;
        }
        
        .detail-row {
          display: flex;
          margin-bottom: 5px;
        }
        
        .detail-label {
          font-weight: 600;
          width: 150px;
        }
        
        .status-completed {
          color: var(--success-color);
        }
        
        .trip-route {
          display: flex;
          flex-direction: column;
          gap: 10px;
          padding: 15px;
          background-color: var(--bg-secondary);
          border-radius: 8px;
          position: relative;
          margin-top: 10px;
        }
        
        .route-station {
          display: flex;
          align-items: center;
          gap: 15px;
          position: relative;
          z-index: 2;
        }
        
        .station-marker {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .station-marker.start {
          background-color: var(--primary-color);
        }
        
        .station-marker.end {
          background-color: var(--success-color);
        }
        
        .route-line {
          position: absolute;
          left: 23px;
          top: 25px;
          bottom: 25px;
          width: 2px;
          background-color: var(--border-color);
          z-index: 1;
        }
        
        .station-name {
          font-weight: 600;
          margin-bottom: 3px;
        }
        
        .station-time {
          font-size: 0.8rem;
          color: var(--text-secondary);
        }
        
        .receipt-payment {
          background-color: var(--bg-secondary);
          padding: 15px;
          border-radius: 8px;
          margin-bottom: 20px;
        }
        
        .payment-row {
          display: flex;
          justify-content: space-between;
          margin-bottom: 5px;
        }
        
        .payment-row.total {
          margin-top: 10px;
          padding-top: 10px;
          border-top: 1px solid var(--border-color);
          font-weight: 600;
          font-size: 1.1rem;
        }
        
        .receipt-footer {
          text-align: center;
          margin-top: 30px;
          padding-top: 20px;
          border-top: 1px solid var(--border-color);
        }
        
        .receipt-footer p {
          margin: 5px 0;
        }
        
        .receipt-footer .small {
          font-size: 0.8rem;
          color: var(--text-light);
        }
        
        .receipt-barcode {
          font-family: monospace;
          font-size: 1.2rem;
          margin-top: 15px;
          letter-spacing: 2px;
        }
        
        .receipt-actions {
          display: flex;
          gap: 10px;
          justify-content: center;
        }
        
        .download-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          min-width: 200px;
        }
        
        .download-btn.loading {
          opacity: 0.7;
          cursor: not-allowed;
        }
        
        .success-message {
          display: flex;
          align-items: center;
          gap: 10px;
          color: var(--success-color);
          font-weight: 500;
        }
        
        .success-icon {
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background-color: var(--success-color);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        @media (max-width: 576px) {
          .receipt-actions {
            flex-direction: column;
          }
          
          .detail-row {
            flex-direction: column;
          }
          
          .detail-label {
            width: 100%;
          }
        }
      `}</style>
    </div>
  )
}

export default TripReceiptGenerator

