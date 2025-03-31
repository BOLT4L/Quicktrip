import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/admin/home";
import Sub_home from "./pages/sub/home";
import Login from "./pages/login";
import Protected from "./pages/protected";
import Unauthorized from "./context/unauthorized";
import { Navigate } from "react-router-dom";
function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/ad_dashboard"
          element={
            <Protected allowedRoles={"a"}>
              <Home />
            </Protected>
          }
        />
        <Route
          path="/sub_dashboard"
          element={
            <Protected allowedRoles={"s"}>
              <Sub_home />
            </Protected>
          }
        />
        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="*" element={<Unauthorized />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
