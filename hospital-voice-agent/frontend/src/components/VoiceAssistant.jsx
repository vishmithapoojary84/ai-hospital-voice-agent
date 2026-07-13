import { useState } from "react";
import { 
  RoomAudioRenderer, 
  StartAudio, 
  LiveKitRoom,
} from "@livekit/components-react";
import AssistantUI from "./AssistantUI";

export default function VoiceAssistant() {
  const [token, setToken] = useState("");
  const [serverUrl, setServerUrl] = useState("");
  const [language, setLanguage] = useState("english");

  const joinRoom = async () => {
    const res = await fetch(
      `http://localhost:8000/token?identity=Patient&room=hospital&language=${language}`
    );

    const data = await res.json();

    setToken(data.token);
    setServerUrl(data.url);
  };

  const handleDisconnect = () => {
    setToken("");
    setServerUrl("");
  };

  if (!token) {
    return (
      <div style={{ textAlign: "center" }}>
        <h2 style={{ fontSize: "1.5rem", color: "#0F172A", marginBottom: "8px" }}>NovaLife Hospital</h2>
        <h3 style={{ fontSize: "1.2rem", color: "#2563EB", marginBottom: "16px", fontWeight: "600" }}>AI Voice Reception Assistant</h3>
        <p style={{ color: "#64748B", marginBottom: "24px", fontSize: "1.1rem" }}>
          Next-generation patient reception. Powered by conversational AI.
        </p>
        
        <div style={{ marginBottom: "32px", display: "flex", flexDirection: "column", alignItems: "center", gap: "10px" }}>
          <label style={{ color: "#64748B", fontWeight: "500" }}>Preferred Language / पसंदीदा भाषा:</label>
          <select 
            value={language} 
            onChange={(e) => setLanguage(e.target.value)}
            style={{ padding: "10px 20px", fontSize: "1rem", borderRadius: "8px", border: "1px solid #E2E8F0", outline: "none", cursor: "pointer" }}
          >
            <option value="english">English</option>
            <option value="hindi">Hindi (हिंदी)</option>
          </select>
        </div>

        <button onClick={joinRoom} className="start-btn">
          🎤 Start Voice Session
        </button>
      </div>
    );
  }

  return (
    <LiveKitRoom
      token={token}
      serverUrl={serverUrl}
      connect
      audio
      video={false}
      data-lk-theme="default"
      onConnected={() => console.log("Connected")}
      onDisconnected={handleDisconnect}
      onError={(e) => console.error(e)}
    >
      <RoomAudioRenderer />
      <StartAudio label="Enable Audio" />
      <AssistantUI />
    </LiveKitRoom>
  );
}