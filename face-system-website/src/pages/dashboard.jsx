const Dashboard = () => {
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
            <div className="flex items-center p-3 rounded-xl hover:bg-blue-50 
                          transition-all duration-200 cursor-pointer group">
              <span className="text-gray-700 font-medium">Home</span>
            </div>

            <div className="flex items-center p-3 rounded-xl hover:bg-blue-50 
                          transition-all duration-200 cursor-pointer group">
              <span className="text-gray-700 font-medium">Analytics</span>
            </div>

            <div className="flex items-center p-3 rounded-xl hover:bg-blue-50 
                          transition-all duration-200 cursor-pointer group">
              <span className="text-gray-700 font-medium">Settings</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="flex-1">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Recordings:</h1>

        {/* Additional Section */}
        <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Recent Activity</h2>
            <button className="px-4 py-2 text-sm font-medium text-blue-600 
                             bg-blue-50 rounded-lg hover:bg-blue-100 
                             transition-colors duration-200">
              View All →
            </button>
          </div>
          {/* Add activity items here */}
          <div className="text-gray-500 text-center py-12">
            <p>No recent activity to display</p>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>
  );
};

export default Dashboard;
