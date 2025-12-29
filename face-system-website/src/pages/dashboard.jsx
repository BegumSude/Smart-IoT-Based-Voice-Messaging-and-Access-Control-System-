import { useState } from "react";
import Users from "./users";
import UseInfo from "../utils/useInfo";

const Dashboard = () => {
  const [activeView, setActiveView] = useState("home");
  const {esp32cam_ip, streamUrl} = UseInfo();
 
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col lg:flex-row gap-8">
          
          {/* Sidebar / Sol Panel */}
          <div className="lg:w-80 shrink-0">
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">Kontrol Paneli</h3>
              <div className="space-y-4">
                <button
                  onClick={() => setActiveView("home")}
                  className={`w-full flex items-center p-3 rounded-xl transition-all ${
                    activeView === "home" ? "bg-blue-600 text-white" : "hover:bg-blue-50 text-gray-700"
                  }`}
                >
                  <span className="font-medium">Ana Sayfa</span>
                </button>

                <button
                  onClick={() => setActiveView("users")}
                  className={`w-full flex items-center p-3 rounded-xl transition-all ${
                    activeView === "users" ? "bg-blue-600 text-white" : "hover:bg-blue-50 text-gray-700"
                  }`}
                >
                  <span className="font-medium">Kullanıcı Yönetimi</span>
                </button>

                <button
                  onClick={() => setActiveView("stream")}
                  className={`w-full flex items-center p-3 rounded-xl transition-all ${
                    activeView === "stream" ? "bg-blue-600 text-white" : "hover:bg-blue-50 text-gray-700"
                  }`}
                >
                  <span className="font-medium">Canlı Yayın</span>
                </button>
              </div>
            </div>
          </div>

          {/* Ana İçerik Alanı */}
          <div className="flex-1">
            <div className="bg-white rounded-2xl p-8 shadow-lg min-h-[500px]">
              
              {activeView === "home" && (
                <div className="animate-fade-in">
                  <h1 className="text-3xl font-bold mb-4 text-gray-800">Hoş Geldiniz</h1>
                  <p className="text-gray-600">Sistem aktif ve çalışıyor. Sol menüden işlem seçebilirsiniz.</p>
                </div>
              )}

              {activeView === "users" && (
                <div className="animate-fade-in">
                  <h1 className="text-3xl font-bold mb-6 text-gray-800">Kullanıcı Listesi</h1>
                  <Users />
                </div>
              )}

              {activeView === "stream" && (
                <div className="animate-fade-in flex flex-col items-center">
                  <h1 className="text-3xl font-bold mb-6 text-gray-800">ESP32 Canlı Yayın</h1>
                  
                  <div className="relative w-full max-w-2xl aspect-video bg-black rounded-xl overflow-hidden shadow-2xl border-4 border-gray-900">
                    {/* MJPEG Yayını için img etiketi şarttır */}
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
                    
                    {/* Hata Mesajı (Yayın yoksa görünür) */}
                    <div 
                      id="stream-error" 
                      className="absolute inset-0 hidden flex-col items-center justify-center text-white bg-gray-900 p-4 text-center"
                    >
                      <svg className="w-16 h-16 text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      <p className="text-xl font-semibold">Bağlantı Kurulamadı</p>
                      <p className="text-sm text-gray-400 mt-2">ESP32'nin {esp32cam_ip} adresinde aktif olduğundan emin olun.</p>
                    </div>
                  </div>
                  
                  <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100 w-full max-w-2xl">
                    <p className="text-sm text-blue-800">
                      <strong>İpucu:</strong> Eğer görüntü gelmiyorsa, tarayıcınızın adres çubuğuna doğrudan 
                      <a href={streamUrl} target="_blank" rel="noreferrer" className="underline ml-1 font-bold">
                        {streamUrl}
                      </a> yazarak yayının açık olup olmadığını test edin.
                    </p>
                  </div>
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