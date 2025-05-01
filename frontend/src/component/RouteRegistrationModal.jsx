
import { useState , useEffect} from "react"
import api from "../api"
const RouteRegisterModal = ({ onClose , onSave }) => {
  
     const [name, setName] = useState("")
    const [prize, setPrize] = useState("")
    const [first_destination, setFirst_destination] = useState("")
    const [last_destination, setLast_destination]= useState("")
    const [branch, setBranch] =  useState([])

  const handleChange = (event) => {
    setLast_destination(event.target.value);
  };
const handleChanges = (event) => {
   setFirst_destination(event.target.value);
  };
  useEffect(()=>{
    getBranch()
   },[])
   const getBranch = () => {
    api
      .get('api/branch/')
      .then((res) => res.data)
      .then((data) => {
        setBranch(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };
  
  const [errors, setErrors] = useState({})

  
  
  
  const validateForm = () => {
    const newErrors = {}

    if (!name.trim()) {
      newErrors.name = "Branch name is required"
    }

    if (!prize.trim()) {
      newErrors.prize= "Address is required"
    }

   
    

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }
   const addRoute= async (e) => {
    
        e.preventDefault();
    
        try {
          const res = await api.post(`api/route/`, {
            name,
            first_destination,
            last_destination,
            route_prize :prize,
          });
          if (res.status === 201) {
            onClose();
          }
        } catch (error) {
          alert(error);
        } finally {
        }
      };

 

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <div className="modal-header">
          <h2 className="modal-title">Register New Route</h2>
          <button className="modal-close" onClick={onClose}>
            &times;
          </button>
        </div>

        <div className="modal-body">
          <form onSubmit={addRoute}>
            <h3 className="section-title">Route Information</h3>

            <div className="form-group">
              <label htmlFor="name" className="form-label">
                 Route Name
              </label>
              <input
            type="text"
            name="name"
            placeholder="Route Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className={`form-control ${errors.name ? "is-invalid" : ""}`}
            required
          />
              
            </div>

           

            <h3 className="section-title">Branch Information</h3>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="address" className="form-label">
                  Fare
                </label>
                <input
            type="text"
            name="Prize"
            placeholder="Fare"
            value={prize}
            onChange={(e) => setPrize(e.target.value)}
            className={`form-control ${errors.prize? "is-invalid" : ""}`}
            required
          />
              
              </div>

              
            </div>
            <div className="form-row">
            <div className="form-group">
            <select 
        id="options" 
        className="filter-dropdown"
        value={first_destination} 
        onChange={handleChanges}
        required
      >
            {branch.map((branchs, index) => (
              <option
                value={branchs.id}
               >
                {branchs.name}
              </option>
            ))}
    </select>
          </div>
          </div>
          <div className="form-row">
            <div className="form-group">
            <select 
        id="option" 
        className="filter-dropdown"
        value={last_destination} 
        onChange={handleChange}
        required
      >
            {branch.map((branchs, index) => (
              <option
                value={branchs.id}
               
              >
                {branchs.name}
              </option>
            ))}
    </select>
          </div>
          </div>


            <div className="modal-footer">
              <button type="button" className="btn btn-secondary"onClick={onClose}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" >
                Register Route
              </button>
            </div>
          </form>
        </div>
      </div>

      <style jsx>{`
        .section-title {
          font-size: 1.1rem;
          font-weight: 600;
          margin: 20px 0 15px;
          padding-bottom: 5px;
          border-bottom: 1px solid var(--border-color);
        }
        
        .form-row {
          display: flex;
          gap: 15px;
        }
        
        .form-row .form-group {
          flex: 1;
        }
        
        .is-invalid {
          border-color: var(--danger-color);
        }
        
        .error-message {
          color: var(--danger-color);
          font-size: 0.875rem;
          margin-top: 5px;
        }
        
        .file-hint {
          font-size: 0.8rem;
          color: var(--text-light);
        }
        
        .file-item.document {
          width: 100%;
          height: auto;
          display: flex;
          align-items: center;
          background-color: rgba(0, 0, 0, 0.05);
          padding: 10px;
        }
        
        .document-icon {
          font-size: 1.5rem;
          margin-right: 10px;
        }
        
        .document-name {
          flex: 1;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      `}</style>
    </div>
  )
}

export default RouteRegisterModal

