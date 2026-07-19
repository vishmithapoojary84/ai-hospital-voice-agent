let audioCtx = null;
let activeNodes = [];
let ringInterval = null;

export const startRingtone = () => {
  if (audioCtx) return; // already playing
  
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if (!AudioContext) return; // Not supported
  
  audioCtx = new AudioContext();
  
  const playRing = () => {
    if (!audioCtx || audioCtx.state === 'closed') return;
    
    const osc1 = audioCtx.createOscillator();
    const osc2 = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    osc1.frequency.value = 440; // US standard ring tone frequencies
    osc2.frequency.value = 480;
    
    osc1.connect(gainNode);
    osc2.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    // Envelope for a softer start/stop
    gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.1);
    gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime + 1.9);
    gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 2.0);
    
    osc1.start(audioCtx.currentTime);
    osc2.start(audioCtx.currentTime);
    osc1.stop(audioCtx.currentTime + 2.0);
    osc2.stop(audioCtx.currentTime + 2.0);
    
    activeNodes.push({ osc1, osc2, gainNode });
  };

  playRing(); // play first ring immediately
  ringInterval = setInterval(playRing, 4000); // repeat every 4s (2s ring, 2s silence)
};

export const stopRingtone = () => {
  if (ringInterval) {
    clearInterval(ringInterval);
    ringInterval = null;
  }
  if (audioCtx) {
    audioCtx.close().catch(() => {});
    audioCtx = null;
  }
  activeNodes = [];
};
