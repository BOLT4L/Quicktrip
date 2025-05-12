import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/stations";
import Sub_admin from "./pages/sub_admins";
import Login from "./pages/login";
import Protected from "./pages/protected";
import Unauthorized from "./context/unauthorized";
import { Navigate } from "react-router-dom";
import Report from "./pages/home";
import Loc from "./pages/loc";
import { ThemeProvider } from './context/ThemeContext';
import Passengers from "./pages/passengers";
import Revenue from "./pages/revenue";
import Settings from "./pages/setting";
import Vehicles from "./pages/vehicles";
import Payments from "./pages/payment";
import TicketPurchase from "./pages/ticket";
import Authpro from "./pages/authpro";
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
          path="/passengers"
          element={
            <Protected allowedRoles={"a"}>
              <Passengers />
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
          path="/subadmin/"
          element={
            <Protected allowedRoles={"a"}>
              <Sub_admin/>
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
          path="/vehicles"
          element={
            <Protected allowedRoles={"s"}>
              <Vehicles />
            </Protected>
          }
        />
        <Route
          path="/ticket/"
          element={
            <Protected allowedRoles={"s"}>
              <TicketPurchase/>
            </Protected>
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
          path="/payment"
          element={
            <Protected allowedRoles={"s"}>
              <Payments />
            </Protected>
          }
        />
        
        <Route
          path="/setting/"
          element={
            
              <Settings />
            
      
          }
        />
   
        <Route path="/unauthorized" element={<Unauthorized />} />
        
        <Route path="/logout" element={<Logout />} />
       
      </Routes>
    </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
