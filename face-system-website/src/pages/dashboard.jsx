import { useState } from "react";
import Users from "./users";

const Dashboard = () => {
  const [activeView, setActiveView] = useState("home");
  const esp32cam_ip = "10.246.64.144";
  const url = `http://${esp32cam_ip}/stream`;
  return (
    <div className="min-h-screen bg-linear-to-br from-gray-50 to-gray-100 p-6 md:p-10">
    <div className="max-w-7xl mx-auto">
    {/* Main Container */}
    <div className="flex flex-col lg:flex-row gap-8">
      
      {/* Sidebar/Left Panel - Modern Card Design */}
      <div className="lg:w-80 shrink-0">
        <div className="bg-white rounded-2xl p-8 shadow-lg 
                        border border-gray-100
                        hover:shadow-xl transition-shadow duration-300">
          <h3 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h3>
          <div className="space-y-4">
            <div
            onClick={() => setActiveView("home")}
            className="flex items-center p-3 rounded-xl hover:bg-blue-50 cursor-pointer"
          >
            <span className="font-medium">Home</span>
          </div>

          <div
            onClick={() => setActiveView("users")}
            className="flex items-center p-3 rounded-xl hover:bg-blue-50 cursor-pointer"
          >
            <span className="font-medium">Users</span>
          </div>

          <div
            onClick={() => setActiveView("stream")}
            className="flex items-center p-3 rounded-xl hover:bg-blue-50 cursor-pointer"
          >
            <span className="font-medium">Stream</span>
          </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="flex-1">
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            {activeView === "home" && (
          <>
            <h1 className="text-3xl font-bold mb-4">Dashboard Home</h1>
            <p className="text-gray-600">Welcome back.</p>
          </>
        )}

        {activeView === "users" && 
        <>
        <h1 className="text-3xl font-bold mb-4">Users:</h1>
        <Users />
        </>}

        {activeView === "stream" && (
          <div>
            <h1 className="text-3xl font-bold mb-4 text-center">Stream:</h1>
            {url ? <video src={url} autoPlay /> : <p>No stream</p>}
          </div>
        )}
          </div>
      </div>
    </div>
  </div>
</div>
  );
};

export default Dashboard;
