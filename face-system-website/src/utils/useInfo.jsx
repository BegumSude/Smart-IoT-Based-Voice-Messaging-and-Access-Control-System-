import { useEffect, useState } from "react";

const UseInfo = () => {
    const [users, setUsers] = useState([]);
    const esp32cam_ip = "192.168.1.43:81";
    const streamUrl = `http://${esp32cam_ip}/stream`;

    async function getUsers() {
    try {
      const res = await fetch("http://127.0.0.1:8000/users");
      const data = await res.json();
      setUsers(data);
    } catch (err) { console.error("Failed to fetch users"); }
  }
  
  useEffect(() => { 
    getUsers();
   }, []);

    return{ getUsers, users, setUsers, streamUrl, esp32cam_ip};
}
 
export default UseInfo;