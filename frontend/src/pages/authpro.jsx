

import {Navigate, redirectDocument} from 'react-router-dom'
import { USER_ROLE } from '../constants'


const Authpro = ({ children }) => {
  // Assuming USER_ROLE is a constant defined elsewhere
  // You should get the role from localStorage, not compare USER_ROLE directly
  const userRole = localStorage.getItem('USER_ROLE');
 
  if (!userRole || (userRole !== "s" && userRole !== "a")) {
      return <Navigate to="/unauthorized" replace />; 
  }
  
  return children;
}

export default Authpro;