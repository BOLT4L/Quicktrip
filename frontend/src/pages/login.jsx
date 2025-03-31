import { useState } from "react";
import api from "../api";
import {jwtDecode} from 'jwt-decode'
import { ACCESS_TOKEN, REFRESH_TOKEN, USER_ROLE } from "../constants";

function Login() {

    const [phone_number, setPhonenumber] = useState('')
    const [password, setPassword] = useState('')
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) =>{
        setLoading(true);
        e.preventDefault();

        try {
            const res = await api.post('/api/token',{ phone_number,password})
             
            const decoded = jwtDecode(res.data.access)
            const role = decoded.role
            localStorage.setItem(USER_ROLE,role)
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
            console.log(role)
            if (role === 'a'){
                window.location.href = '/ad_dashboard';
            }else if (role === 's'){
                window.location.href = '/sub_dashboard'
            }

        }
        catch (error) {
            alert(error)
        }
        finally{
            setLoading(false)
        }
    };
    return (
       <div class="main-container">
        <div class="image-container">
            
        
        </div>
        <div class="login-container">
        <form onSubmit={handleSubmit} className="form-conteiner" id="loginForm">

        <div class="input-group">
                    
        <input
          className="form-input" 
          type="number"
          id="phonenumber"
          value={phone_number}
          onChange={(e) => setPhonenumber(e.target.value)}
          placeholder="phone number"
          /></div>
          <div class="input-group">
         
          <input
          id="password"
          className="form-input" 
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="password"
          />
          </div>

          
          <button type="submit" className="form-button" >Login</button>
              
         
    </form></div></div>
    
    )
}
export default Login