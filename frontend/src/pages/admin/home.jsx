import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import api from "../../api"
function Home(){
   const [record, setRecord] =  useState([])
   useEffect(()=>{
    getRecord()
   },[])

   const getRecord = () => {
    api
      .get('api/admin_dashboard/')
      .then((res) => res.data)
      .then((data) => {
        setRecord(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };
   return  <>
    <div className="topbar">
        <ul>
            <li><a href ="#">Record</a></li>
            <li><a href ="#">Branch</a></li>
            <li><a href ="#">ECOM</a></li>
            <li><a href ="#">Transportation </a></li>
            <li><a href ="#">staff </a></li>
            <li><a href ="/logout">Logout</a></li>
        </ul>
    </div>
    </>

}
export default Home