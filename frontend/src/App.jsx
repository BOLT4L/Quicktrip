import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/admin/home";
import Branch from "./pages/admin/branch";
import Add from "./pages/admin/add";
import Sub_home from "./pages/sub/home";
import Login from "./pages/login";
import Protected from "./pages/protected";
import Unauthorized from "./context/unauthorized";
import Level from "./pages/admin/level";
import Addbranch from "./pages/admin/addbranch";
import { Navigate } from "react-router-dom";
import Transportation from "./pages/admin/transportation";
import Addroute from "./pages/admin/addroute";
import Report from "./pages/admin/report";
import Loc from "./pages/admin/loc";
import Sub_route from "./pages/sub/sub_route";
import Add_veh from "./pages/sub/add_veh";
import Buyticket from "./pages/sub/ticket";
import Adduser from "./pages/sub/add_user";
import Non_fayda from "./pages/sub/non_fayda";
import Long_route from "./pages/sub/long_route";
import Alert from "./pages/sub/alert";
import { ThemeProvider } from './context/ThemeContext';
import Passengers from "./pages/admin/passengers";
import Revenue from "./pages/admin/revenue";
import Settings from "./pages/admin/setting";
import Authpro from "./pages/authpro";
import VehicleTracker from "./pages/admin/vehicle";
import Vehicles from "./pages/admin/vehicles";
import Payments from "./pages/admin/payment";
function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function App() {
  return (
    <ThemeProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/branchs"
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
        <Route
          path="/sub_alert"
          element={
            <Protected allowedRoles={"s"}>
              <Alert />
            </Protected>
          }
        />
         <Route
          path="/add_vehicle"
          element={
            <Protected allowedRoles={"s"}>
              <Add_veh/>
            </Protected>
          }
        />
         <Route
          path="/branch/:bid"
          element={
            <Protected allowedRoles={"a"}>
              <Branch />
            </Protected>
          }
        />
        <Route
          path="/passengers"
          element={
            <Protected allowedRoles={"a"}>
              <Passengers />
            </Protected>
          }
        />
        <Route
          path="/payment"
          element={
            <Protected allowedRoles={"s"}>
              <Payments />
            </Protected>
          }
        />
        <Route
          path="/vehicles"
          element={
            <Protected allowedRoles={"s"}>
              <Vehicles />
            </Protected>
          }
        />
        <Route
          path="/route/:rid"
          element={
            <Protected allowedRoles={"s"}>
              <Sub_route/>
            </Protected>
          }
        />
        <Route
          path="/nonfayda/"
          element={
            <Protected allowedRoles={"s"}>
              <Non_fayda/>
            </Protected>
          }
        />
        <Route
          path="/long_route/"
          element={
            <Protected allowedRoles={"s"}>
              <Long_route/>
            </Protected>
          }
        />
        <Route
          path="/adduser/"
          element={
            <Protected allowedRoles={"s"}>
              <Adduser/>
            </Protected>
          }
        />
        <Route
          path="/buyticket/"
          element={
            <Protected allowedRoles={"s"}>
              <Buyticket/>
            </Protected>
          }
        />
        <Route
          path="/level/"
          element={
            <Protected allowedRoles={"a"}>
              <Level />
            </Protected>
          }
        />
          <Route
          path="/addbranch/"
          element={
            <Protected allowedRoles={"a"}>
              <Addbranch />
            </Protected>
          }
        />
        <Route
          path="/addroute/"
          element={
            <Protected allowedRoles={"a"}>
              <Addroute />
            </Protected>
          }
        />
         <Route
          path="/home/"
          element={
            <Authpro>
              <Report />
            </Authpro>
          }
        />
        <Route
          path="/location/"
          element={
            <Protected allowedRoles={"s"}>
              <Loc />
            </Protected>
          }
        />
         <Route
          path="/revenue/"
          element={
            <Protected allowedRoles={"a"}>
              <Revenue />
            </Protected>
          }
        />
         <Route
          path="/setting/"
          element={
            
              <Settings />
      
          }
        />
   
        <Route
          path="/subadmin/"
          element={
            <Protected allowedRoles={"a"}>
              <Add />
            </Protected>
          }
        />
         <Route
          path="/transportation"
          element={
            <Protected allowedRoles={"a"}>
              <Transportation />
            </Protected>
          }
        />
        <Route path="/unauthorized" element={<Unauthorized />} />
        
        <Route path="/logout" element={<Logout />} />
        <Route path="*" element={<Unauthorized />} />
      </Routes>
    </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
