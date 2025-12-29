import { useEffect, useState } from "react";
import UseInfo from "../utils/useInfo";

const Users = () => {
  const [step, setStep] = useState(1);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [photoPath, setPhotoPath] = useState(null);
  const [isAdding, setIsAdding] = useState(false);
  const [loading, setLoading] = useState(false);  
  const {getUsers,streamUrl, users, setUsers} = UseInfo();
  
  // useEffect(() => { 
  //   getUsers();
  //  }, []);

  const handleCreateUser = async (e) => {
  e.preventDefault();
  const token = localStorage.getItem("token");

  try {
    const response = await fetch("http://127.0.0.1:8000/admin/create-user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json(); 

    if (response.ok) {
      alert("User created!");
      setIsAdding(false);
      getUsers();
    } else {
      const errorMessage = typeof data.detail === 'object' 
    ? JSON.stringify(data.detail) 
    : data.detail;
    
    alert(`Error: ${errorMessage || "Unknown error"}`);
    console.log("Full Error Data:", data);
    }
  } catch (error) {
    console.error("Network error:", error);
  }
};

  return (
    <div className="p-6">
      <div className="flex gap-4 mb-6">
        <button 
          className="bg-gray-900 text-white p-3 rounded-2xl hover:bg-gray-700"
          onClick={() => setIsAdding(!isAdding)}
        >
          {isAdding ? "Cancel" : "Add New User"}
        </button>
      </div>

      {isAdding && (
        <div className="bg-gray-800 text-white p-6 rounded-2xl mb-6 max-w-sm">
          <form className="flex flex-col gap-3">
            {step === 1 && (
            <>
            <label>Username</label>
            <input 
              className="text-black p-2 rounded bg-white"
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              required 
            />
            <label>Password</label>
            <input 
              className="text-black p-2 rounded bg-white"
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
            />
            <button type="button" onClick={() => setStep(2)} className="bg-blue-600 p-2 rounded mt-2">Next</button>
            </>)
            }
            {step === 2 && (
              <>
                <p className="text-4xl font-bold text-amber-400">Position the user's face and take a photo</p>
                <img
                      src={streamUrl}
                      alt="Canlı Yayın"
                      className="w-full h-full object-contain"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        const errorMsg = document.getElementById('stream-error');
                        if (errorMsg) errorMsg.style.display = 'flex';
                      }}
                    />
                <button
                  onClick={async (e) => {
                    e.preventDefault();
                    setLoading(true);
                    const res = await fetch("http://127.0.0.1:8000/admin/capture-photo", {
                      method: "POST",
                      headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`
                      }
                    });
                    const data = await res.json();
                     if (!res.ok) {
                        alert(data.detail || "Failed to capture photo");
                        setLoading(false);
                        return;
                      }
                      setPhotoPath(data.photo_path);
                      setStep(3);
                  }}
                  className="bg-blue-950 text-white p-2 rounded mt-2"
                >
                  {loading ? "Taking photo..." : "Take a shot"}
                </button>
              </>
            )}
            {step === 3 && (
            <>
              <p>Photo captured ✔</p>

              <button
                onClick={async () => {
                  const res = await fetch("http://127.0.0.1:8000/admin/create-user", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                      Authorization: `Bearer ${localStorage.getItem("token")}`
                    },
                    body: JSON.stringify({
                      username,
                      password,
                      photo_path: photoPath
                    })
                  });

                  if (res.ok) {
                    alert("User created!");
                    setStep(1);
                    setUsername("");
                    setPassword("");
                    setPhotoPath(null);
                  }
                }}
                className="bg-green-500 text-white p-2 rounded mt-2"
              >
                Create
              </button>
            </>
          )}

          </form>
        </div>
      )}

      <div className="grid gap-4">
        {users?.map(user => (
          <div key={user.id} className="bg-gray-100 p-4 rounded-2xl shadow-sm">
            <p><strong>Username:</strong> {user.username}</p>
            <p><strong>Role:</strong> {user.role}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Users;