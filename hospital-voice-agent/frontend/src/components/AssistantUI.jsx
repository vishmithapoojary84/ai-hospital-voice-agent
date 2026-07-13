import {
  VoiceAssistantControlBar,
  BarVisualizer,
  useVoiceAssistant,
} from "@livekit/components-react";

import Avatar from "./Avatar";

export default function AssistantUI() {
    const { state, audioTrack } = useVoiceAssistant();

    let statusText = "";
    let statusDot = "";
    
    if (state === "listening") {
        statusText = "Listening...";
        statusDot = "🟢";
    } else if (state === "speaking") {
        statusText = "Speaking...";
        statusDot = "🔵";
    } else if (state === "thinking") {
        statusText = "Thinking...";
        statusDot = "🟡";
    } else {
        statusText = "Connected";
        statusDot = "⚪";
    }

    return (
        <div className="assistant">
            <h2 style={{ fontSize: "1.5rem", color: "#0F172A", margin: "0 0 4px 0" }}>NovaLife Hospital</h2>
            <h3 style={{ fontSize: "1.1rem", color: "#2563EB", margin: "0 0 8px 0", fontWeight: "600" }}>AI Voice Reception Assistant</h3>
            <p style={{ color: "#64748B", margin: "0 0 24px 0", fontSize: "0.95rem" }}>
              Next-generation patient reception. Powered by conversational AI.
            </p>
            
            <Avatar state={state}/>
            
            <p className="status" style={{ marginTop: "24px" }}>{statusDot} {statusText}</p>
            <BarVisualizer
                trackRef={audioTrack}
                state={state}
                barCount={7}
                className="bars"
            />
            <VoiceAssistantControlBar/>
        </div>
    );
}
