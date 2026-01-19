import { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

 const handleLogin = async (e) => {
  e.preventDefault();

  const res = await fetch("http://127.0.0.1:8000/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username,
      password
    })
  });

  if (!res.ok) {
    alert("Invalid credentials");
    return;
  }

  const data = await res.json();
  localStorage.setItem("token", data.access_token);
  localStorage.setItem("role", data.role);

  navigate("/home");
};

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-87.5">
        <form onSubmit={handleLogin} className="space-y-4">
          <h2 className="text-xl font-semibold text-center">Welcome</h2>

          <div>
            <label className="text-sm">username</label>
            <input
              type="text"
              className="w-full border p-2 rounded-lg mt-1"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />

            <label className="text-sm block mt-4">Password</label>
            <input
              type="password"
              className="w-full border p-2 rounded-lg mt-1"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
