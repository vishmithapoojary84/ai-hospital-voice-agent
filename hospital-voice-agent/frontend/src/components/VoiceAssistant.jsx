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
  const [sttProvider, setSttProvider] = useState("deepgram");
  const [llmProvider, setLlmProvider] = useState("gemini");
  const [ttsProvider, setTtsProvider] = useState("sarvam");
  const [isConnecting, setIsConnecting] = useState(false);

  const joinRoom = async () => {
    setIsConnecting(true);
    try {
      const res = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/token?identity=Patient&room=hospital&language=${language}&stt_provider=${sttProvider}&tts_provider=${ttsProvider}&llm_provider=${llmProvider}`
      );

      if (!res.ok) {
        throw new Error("Failed to fetch token");
      }

      const data = await res.json();

      setToken(data.token);
      setServerUrl(data.url);
    } catch (error) {
      console.error("Error connecting:", error);
      setIsConnecting(false);
      alert("Failed to connect to the server. Please ensure the backend is running.");
    }
  };

  const handleDisconnect = () => {
    setToken("");
    setServerUrl("");
    setIsConnecting(false);
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
            disabled={isConnecting}
            style={{ padding: "10px 20px", fontSize: "1rem", borderRadius: "8px", border: "1px solid #E2E8F0", outline: "none", cursor: "pointer", opacity: isConnecting ? 0.6 : 1 }}
          >
            <option value="english">English</option>
            <option value="hindi">Hindi (हिंदी)</option>
          </select>
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "10px",
            marginBottom: "20px",
          }}
        >
          <label style={{ color: "#64748B", fontWeight: "500" }}>
            Speech-to-Text Provider
          </label>

          <select
            value={sttProvider}
            onChange={(e) => setSttProvider(e.target.value)}
            disabled={isConnecting}
            style={{
              padding: "10px 20px",
              borderRadius: "8px",
              fontSize: "1rem",
              opacity: isConnecting ? 0.6 : 1
            }}
          >
            <option value="deepgram">Deepgram</option>
            <option value="elevenlabs">ElevenLabs</option>
            <option value="sarvam">Sarvam AI</option>
          </select>
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "10px",
            marginBottom: "32px",
          }}
        >
          <label style={{ color: "#64748B", fontWeight: "500" }}>
            AI Model
          </label>

          <select
            value={llmProvider}
            onChange={(e) => setLlmProvider(e.target.value)}
            disabled={isConnecting}
            style={{
              padding: "10px 20px",
              borderRadius: "8px",
              fontSize: "1rem",
              opacity: isConnecting ? 0.6 : 1
            }}
          >
            <option value="gemini">Gemini 3.1 Flash Lite</option>
            <option value="gpt">GPT-4.1</option>
            <option value="claude">Claude Sonnet</option>
          </select>
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "10px",
            marginBottom: "32px",
          }}
        >
          <label
            style={{
              color: "#64748B",
              fontWeight: "500",
            }}
          >
            Text To Speech
          </label>

          <select
            value={ttsProvider}
            onChange={(e) => setTtsProvider(e.target.value)}
            disabled={isConnecting}
            style={{
              padding: "10px 20px",
              borderRadius: "8px",
              fontSize: "1rem",
              opacity: isConnecting ? 0.6 : 1
            }}
          >
            <option value="sarvam">Sarvam AI</option>
            <option value="elevenlabs">ElevenLabs</option>
          </select>
        </div>

        <button 
          onClick={joinRoom} 
          className="start-btn"
          disabled={isConnecting}
          style={isConnecting ? { opacity: 0.7, cursor: "not-allowed" } : {}}
        >
          {isConnecting ? "📞 Calling Reception..." : "🎤 Start Voice Session"}
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
      onConnected={() => {}}
      onDisconnected={handleDisconnect}
      onError={(e) => console.error(e)}
    >
      <RoomAudioRenderer />
      <StartAudio label="Enable Audio" />
      <AssistantUI />
    </LiveKitRoom>
  );
}