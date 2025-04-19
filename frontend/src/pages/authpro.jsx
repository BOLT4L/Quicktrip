import {Navigate, redirectDocument} from 'react-router-dom'
import { USER_ROLE } from '../constants';



const Authpro = ({children })=>{
    
    const isAuthenticated = localStorage.getItem(USER_ROLE);
   
    if (!isAuthenticated) {
        return <Navigate to="/unauthorized" replace />; 
      }
    return children
}
export default Authpro