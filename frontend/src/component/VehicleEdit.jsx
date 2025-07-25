import { useState, useEffect } from "react";
import api from "../api";

const VehicleEdit = ({onClose, onSave, vehicle}) => {
     const [branchs, setBranchs] = useState([]);
     const [branch, setBranch] = useState([]);
  const [errors, setErrors] = useState({});
   const [routes, setRoutes] = useState([]);
   const [driver, setDriver] = useState([]);
  const [message, setMessage] = useState({ type: "", text: "" });
  const [formData, setFormData] = useState({
    route: null,
    branch: null,
    driver: null,

  });

  useEffect(() => {
    getBranch();
    getDriver();
    getRoute();
    if (vehicle) {
      setFormData({
        route: vehicle.route?.id || null,
        branch: vehicle.branch?.id || null,
        driver: vehicle.user?.id || null,
      });
      setBranch(vehicle.branch);
    }
  }, [vehicle]);

  const getBranch = () => {
    api
      .get(`api/edit_branch/`)
      .then((res) => res.data)
      .then((data) => {
        setBranchs(data);
      })
      .catch((err) => console.log(err));
  };
  const getDriver = () => {
    api
      .get('api/driver/')
      .then((res) => res.data)
      .then((data) => setDriver(data))
      .catch((err) => console.error("Error fetching drivers:", err));
  };

  const getRoute = async () => {
    try {
      const res = await api.get(`api/route/`);
      setRoutes(res.data);
    } catch (err) {
      console.error("Failed to fetch routes:", err);
      setRoutes([]);
    }
  };
  const validateForm = () => {
    const newErrors = {};

    if (!formData.route) {
      newErrors.route = "Route is required";
    }

    if (!formData.branch) {
      newErrors.branch = "Branch is required";
    }
    if (!formData.driver) {
      newErrors.user = "Driver is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    try {
      const res = await api.patch(`api/editVehicle/${vehicle.id}/`, {
        route: formData.route,
        branch: formData.branch,
        user: formData.driver,
      });

      

      if (res.status === 200) {
        setMessage({
          type: "success",
          text: "Vehicle updated successfully!",
        });
        onSave(); 
      }
    } catch (error) {
      setMessage({
        type: "error",
        text: error.response?.data?.message || "An error occurred",
      });
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <div className="modal-header">
          <h2 className="modal-title">Edit {vehicle.plate_number} </h2>
          <button className="modal-close" onClick={onClose}>
            &times;
          </button>
        </div>

        <div className="modal-body">
          <form onSubmit={handleSubmit}>
            {message.text && (
              <div
                className={`alert ${
                  message.type === "success" ? "alert-success" : "alert-danger"
                }`}
              >
                {message.text}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="name" className="form-label">
                Current vehicle
              </label>
              <input
                type="text"
                className="form-control"
                value={
                   vehicle 
                    ? `${vehicle?.plate_number || ""} `
                    : ""
                }
                readOnly
              />
            </div>

            <h3 className="section-title">Station and Route</h3>

            <div className="form-group">
              <label htmlFor="route" className="form-label">
                Route
              </label>
             <select 
                  id="route" 
                  name="route"
                  className={`form-control ${errors.route ? "is-invalid" : ""}`}
                  value={formData.route}
                  onChange={(e) =>
                  setFormData({ ...formData, route: parseInt(e.target.value) })
                }
                  required
                >
                  <option value="">-- Select Route --</option>
                  {routes.map((rout) => (
                    <option key={rout.id} value={rout.id}>
                      {rout.name}
                    </option>
                  ))}
                </select>
              {errors.route && (
                <div className="error-message">{errors.route}</div>
              )}
            </div>
                        <div className="form-group">
              <label htmlFor="driver" className="form-label">
                Driver
              </label>
             <select 
                  id="route" 
                  name="route"
                  className={`form-control ${errors.user ? "is-invalid" : ""}`}
                  value={formData.driver}
                  onChange={(e) =>
                  setFormData({ ...formData, user: parseInt(e.target.value) })
                }
                  required
                >
                  <option value="">-- Select Driver --</option>
                  {driver.map((dr) => (
                    <option key={dr.id} value={dr.id}>
                      {dr.employee?.Fname}{dr.employee?.Lname}
                    </option>
                  ))}
                </select>
              {errors.user && (
                <div className="error-message">{errors.user}</div>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="branch" className="form-label">
                Branch
              </label>
              <select
                className={`form-control ${errors.branch ? "is-invalid" : ""}`}
                value={formData.branch || ""}
                onChange={(e) =>
                  setFormData({ ...formData, branch: parseInt(e.target.value) })
                }
                required
              >
                <option value="">Select a branch</option>
                {branchs.map((br) => (
                  <option key={br.id} value={br.id}>
                    {br.name}
                  </option>
                ))}
              </select>
              {errors.branch && (
                <div className="error-message">{errors.branch}</div>
              )}
            </div>

            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={onClose}
              >
                Cancel
              </button>
              <button type="submit" className="btn btn-primary">
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>

      <style jsx>{`
        .modal-backdrop {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: rgba(0, 0, 0, 0.5);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }
        
        .modal {
          background: white;
          border-radius: 8px;
          width: 500px;
          max-width: 90%;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .modal-header {
          padding: 15px 20px;
          border-bottom: 1px solid #eee;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .modal-title {
          margin: 0;
          font-size: 1.25rem;
        }
        
        .modal-close {
          background: none;
          border: none;
          font-size: 1.5rem;
          cursor: pointer;
        }
        
        .modal-body {
          padding: 20px;
        }
        
        .form-group {
          margin-bottom: 15px;
        }
        
        .form-label {
          display: block;
          margin-bottom: 5px;
          font-weight: 500;
        }
        
        .form-control {
          width: 100%;
          padding: 8px 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 14px;
        }
        
        .is-invalid {
          border-color: #dc3545;
        }
        
        .error-message {
          color: #dc3545;
          font-size: 0.875rem;
          margin-top: 5px;
        }
        
        .modal-footer {
          padding: 15px 20px;
          border-top: 1px solid #eee;
          display: flex;
          justify-content: flex-end;
          gap: 10px;
        }
        
        .btn {
          padding: 8px 16px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
        }
        
        .btn-secondary {
          background: #6c757d;
          color: white;
          border: none;
        }
        
        .btn-primary {
          background: #007bff;
          color: white;
          border: none;
        }
        
        .alert {
          padding: 10px 15px;
          margin-bottom: 15px;
          border-radius: 4px;
        }
        
        .alert-success {
          background: #d4edda;
          color: #155724;
        }
        
        .alert-danger {
          background: #f8d7da;
          color: #721c24;
        }
        
        .section-title {
          font-size: 1.1rem;
          font-weight: 600;
          margin: 20px 0 15px;
          padding-bottom: 5px;
          border-bottom: 1px solid #eee;
        }
      `}</style>
    </div>
  );
};

export default VehicleEdit;