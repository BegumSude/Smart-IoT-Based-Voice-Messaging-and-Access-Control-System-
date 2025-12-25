import { useEffect, useState } from "react";
import { isAdmin } from "../utils/auth"; //to be added only for admins "{isAdmin() && "

const Users = () => {
  const [users, setUsers] = useState([]);  
  async function getUsers(){
        const res = await fetch("http://127.0.0.1:8000/users");
        const data = await res.json();    
        setUsers(data);
      }
  useEffect(()=>{
      getUsers();
    },[])

    async function createNewUsers(){
      fetch("http://127.0.0.1:8000/admin/create-user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ username, password })
});

    }
    return ( 
      <div>
        <div className="flex items-center gap-6 mb-2">
          <button className="transition delay-50 bg-gray-900 text-white text-l
                           rounded-2xl p-3
                           duration-700 ease-in-out hover:scale-110
                           hover:bg-white hover:text-gray-900">Add new user</button>
                           
        <button className="transition delay-50 bg-gray-900 text-white text-l
                           rounded-2xl p-3
                           duration-700 ease-in-out hover:scale-110
                           hover:bg-white hover:text-gray-900">Edit Users</button>
        </div>
        {users.map(user => (<div key={user.id} className="bg-linear-to-br from-gray-50 to-gray-100 rounded-2xl 
                                                          -me-5 p-4">
           <p>username: {user.role}</p>
           <p>Role: {user.role}</p>
           
        </div>))}
      </div>
     );
}
 
export default Users;