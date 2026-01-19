import { useEffect, useRef, useState } from "react";
import UseInfo from "../utils/useInfo";

const FaceRecognition = () => {
  const { streamUrl } = UseInfo(); // ESP32 IP ve Stream URL'sini buradan alıyoruz
  const canvasRef = useRef(null);
  const imgRef = useRef(null); // Video yerine Image kullanacağız
  const [status, setStatus] = useState("Waiting for recognition...");

  // Backend ile yüz tanıma
  const captureAndSendFrame = async () => {
    const canvas = canvasRef.current;
    const img = imgRef.current;

    if (!img || !img.complete) return;

    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append("snapshot", blob, "frame.jpg");

      try {
        const response = await fetch("http://127.0.0.1:8000/face/recognize", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();

        drawBoxAndLabel(data.user);
        setStatus(
          data.user && data.user !== "UNKNOWN"
            ? `Recognized: ${data.user}`
            : "Unknown person"
        );
      } catch (err) {
        console.error("Face recognition error:", err);
        setStatus("Error in recognition");
      }
    }, "image/jpeg");
  };

  // Canvas üzerine isim yazma
  const drawBoxAndLabel = (username) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = "24px Arial";
    ctx.fillStyle = "red";
    ctx.fillText(username || "UNKNOWN", 10, 30);
  };
  
  useEffect(() => {
    // Webcam başlatan startVideo fonksiyonunu sildik!
    // Saniyede bir kare yakalayıp backend'e gönderiyoruz
    const interval = setInterval(captureAndSendFrame, 1000);

    return () => clearInterval(interval);
  }, [streamUrl]); // URL değişirse efekti yenile

  return (
    <div style={{ position: "relative", width: "640px", height: "480px", margin: "0 auto" }}>
      {/* ESP32-CAM yayınını göstermek için <img> etiketi kullanıyoruz */}
      <img
        ref={imgRef}
        src={streamUrl}
        alt="ESP32 Stream"
        crossOrigin="anonymous" // CORS hatasını önlemek için kritik
        style={{ width: "100%", height: "100%", objectFit: "cover", border: "2px solid #333" }}
        onLoad={() => setStatus("ESP32 Bağlantısı Aktif")}
        onError={() => setStatus("ESP32 Yayını Alınamıyor!")}
      />
      
      {/* Tanıma sonuçlarını (isimleri) üzerine çizmek için canvas */}
      <canvas
        ref={canvasRef}
        style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none" }}
      />
      
      <div style={{ marginTop: "10px", padding: "10px", background: "#eee", borderRadius: "5px" }}>
        <strong>Durum:</strong> {status}
      </div>
    </div>
  );
};

export default FaceRecognition;