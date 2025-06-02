import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import api from "../api";
import Sidebar from "../component/sidebar";
import Header from "../component/Header";
import SubAdminModal from "../component/SubAdminModal";
import StationMap from "../component/StationMap";
import SubAdminEdit from "../component/SubAdminEdit";
function Sub_admin() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { bid } = useParams();
  const [mapZoom, setMapZoom] = useState(1);
  const [password, setPassword] = useState("");
  const [phone_number, setPhone_number] = useState("");
  const [employee, setEmployee] = useState({
    Fname: "",
    Lname: "",
    address: "",
    position: "",
  });
  const [showModal, setShowModal] = useState(false);
  const [showEditModal, setEditModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterRole, setFilterRole] = useState("all");
  const [showMap, setShowMap] = useState(false);
  const [branch, setBranch] = useState(null);
  const [subAdmins, setSubAdmins] = useState([]);
  const [selectedsubAdmins, setselectedSubAdmins] = useState([]);

  useEffect(() => {
    getStaffs();
    getBranch();
  }, []);
  const handleAddSubAdmin = (newSubAdmin) => {
    setSubAdmins([
      {
        id: subAdmins.length + 1,
        ...newSubAdmin,
      },
      ...subAdmins,
    ]);
    setShowModal(false);
  };
  const handleEditSubAdmin = () => {
    window.location.reload
    window.location.reload
    
  };
  const getStaffs = () => {
    api
      .get("api/staffs/")
      .then((res) => res.data)
      .then((data) => {
        setSubAdmins(data);
        console.log(data);
      })
      .catch((err) => console.log(err));
  };
  const getBranch = () => {
    api
      .get("api/branch/")
      .then((res) => res.data)
      .then((data) => {
        setBranch();
        console.log(data);
      })
      .catch((err) => console.log(err));
  };
  const handleDeactivate = (userId) => {
    setLoading(true);
    setError(null);

    try {
      const response = api.put(`/api/users/${userId}/`, { is_active: false });
      getStaffs();
      
    } catch (err) {
      setError(err.response?.data?.detail || "Error deactivating user");
    } finally {
      setLoading(false);
    }
  };
  const handleActivate = (userId) => {
    setLoading(true);
    setError(null);

    try {
      const response = api.put(`/api/users/${userId}/`, { is_active: true });
      getStaffs();
    } catch (err) {
      setError(err.response?.data?.detail || "Error deactivating user");
    } finally {
      setLoading(false);
    }
  };
  
  const filteredSubAdmins = subAdmins.filter((admin) => {
    const matchesSearch =
      admin.employee.Fname.toLowerCase().includes(searchTerm.toLowerCase()) ||
      admin.employee.Lname.toLowerCase().includes(searchTerm.toLowerCase()) ||
      admin.branch.name.toLowerCase().includes(searchTerm.toLowerCase());

    if (filterRole === "all") return matchesSearch;
    return (
      matchesSearch &&
      admin.user_type === filterRole  
    );
  });

  const [selectedOption, setSelectedOption] = useState("");

  return (
    <>
      <div className="sub-admins-page">
        <Sidebar />
        <div className="right">
          <Header />
          <div className="page-header">
            <h1>Sub-Admin Management</h1>
            <div className="header-actions">
              <button
                className="btn btn-primary"
                onClick={() => setShowModal(true)}
              >
                Add New Sub-Admin
              </button>
            </div>
          </div>

          <div className="card">
            <div className="search-filter-container">
              <div className="search-container">
                <input
                  type="text"
                  placeholder="Search by name, ID..."
                  className="search-input"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>

            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Phone</th>
                    <th>Role</th>
                    <th>Station</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredSubAdmins.map((admin) => (
                    <tr key={admin.id}>
                      <td>{admin.employee.Fname}</td>
                      <td>{admin.employee.Lname}</td>
                      <td>{admin.phone_number}</td>

                      <td>
                        <span className={`role-badge ${admin.role}`}>
                          {admin.employee.position}
                        </span>
                      </td>
                      <td>{admin.branch.name}</td>
                      <td className="button">
                      <div className="action-buttons">
                        <button className={`btn btn-edit`} onClick={() => {setEditModal(true),setselectedSubAdmins(admin)}}>Edit</button>
                      </div>
                        <div className="action-buttons">
                          {admin.is_active ? (<button
                            onClick={() => handleDeactivate(admin.id)}
                            disabled={loading}
                            className={`btn btn-danger ${
                              loading ? "disabled" : ""
                            }`}
                          >
                            {loading ? (
                              <>
                                <span
                                  className="spinner-border spinner-border-sm me-2"
                                  role="status"
                                  aria-hidden="true"
                                ></span>
                                Deactivating...
                              </>
                            ) : (
                              "Deactivate User"
                            )}
                          </button>):(<button
                            onClick={() => handleActivate(admin.id)}
                            disabled={loading}
                            style={{background : "lightgreen"}}
                            className={`btn btn-safe ${
                              loading ? "disabled" : ""
                            }`}
                          >
                            {loading ? (
                              <>
                                <span
                                  className="spinner-border spinner-border-sm me-2"
                                  role="status"
                                  aria-hidden="true"
                                ></span>
                                Activating...
                              </>
                            ) : (
                              "Activate User"
                            )}
                          </button>)}
                          {error && (
                            <div className="alert alert-danger mt-2">
                              {error}
                            </div>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {showModal && (
            <SubAdminModal
              onClose={() => setShowModal(false)}
              onSave={handleAddSubAdmin}
            />
          )}
          {showEditModal && (
            <SubAdminEdit
              onClose={() => {setEditModal(false), setselectedSubAdmins([])}}
              onSave={handleEditSubAdmin}
              subAdmin={selectedsubAdmins}
            />
          )}
        </div>
        <style jsx>{`
          .sub-admins-page {
            display: flex;
            flex-direction: row;
          }
          .right {
            width: 100%;
            margin: 10px;
          }
          .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 20px;
          }

          .header-actions {
            display: flex;
            gap: 10px;
          }

          .map-card {
            margin-bottom: 20px;
          }

          .search-filter-container {
            display: flex;
            margin-bottom: 20px;
            gap: 10px;
            flex-wrap: wrap;
          }

          .search-container {
            flex: 1;
            min-width: 250px;
          }

          .filter-container {
            width: 200px;
          }

          .action-buttons {
            display: flex;
            gap: 5px;
          }
            .button {
            display: flex;
            flex-direction :row;
            gap: 5px;
          }

          .btn-sm {
            padding: 0.25rem 0.5rem;
            font-size: 0.875rem;
          }

          .role-badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 1rem;
            font-weight: 500;
          }

          .role-badge.station-manager {
            background-color: rgba(58, 134, 255, 0.1);
            color: var(--primary-color);
          }

          .role-badge.vehicle-inspector {
            background-color: rgba(131, 56, 236, 0.1);
            color: var(--secondary-color);
          }
        `}</style>
      </div>
    </>
  );
}
export default Sub_admin;
