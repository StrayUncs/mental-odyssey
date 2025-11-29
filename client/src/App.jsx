import React, { useState, useEffect, useRef } from 'react';

// --- Icons (Inline SVGs) ---
const Activity = (props) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
);
const Hand = (props) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0"/><path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2"/><path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/></svg>
);
const User = (props) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
);
const LogOut = (props) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
);
const Send = (props) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
);
const LineChart = (props) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 3v18h18"/><path d="M18.5 8.1 13.9 15.3 11.5 12.5 5 20"/></svg>
);
const BarChart = (props) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>
);

// --- CSS Styles (Injected directly to avoid setup issues) ---
const css = `
  * { box-sizing: border-box; }
  body, html { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  
  .odyssey-app {
    display: flex;
    height: 100vh;
    background-color: #f8fafc; /* slate-50 */
    color: #334155; /* slate-700 */
    overflow: hidden;
  }

  /* SIDEBAR */
  .sidebar {
    width: 80px;
    background-color: white;
    border-right: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 24px 0;
    flex-shrink: 0;
    z-index: 10;
  }
  .sidebar-group { display: flex; flex-direction: column; gap: 32px; align-items: center; }
  
  .icon-btn {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
    background-color: #f1f5f9;
    color: #64748b;
  }
  .icon-btn:hover { background-color: #e2e8f0; }
  
  .icon-btn.active-hand {
    background-color: #fbbf24; /* amber-400 */
    color: #78350f; /* amber-900 */
    box-shadow: 0 0 0 4px #fef3c7;
    animation: pulse 2s infinite;
  }

  /* MAIN CHAT AREA */
  .chat-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
    background-color: #f8fafc;
  }

  /* HEADER */
  .header {
    height: 64px;
    background-color: white;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    flex-shrink: 0;
  }
  .title { font-size: 20px; font-weight: bold; display: flex; align-items: center; gap: 8px; }
  .tag { font-size: 12px; background: #f1f5f9; padding: 2px 8px; border-radius: 12px; font-weight: normal; color: #94a3b8; }
  
  .agents-list { display: flex; align-items: center; gap: 8px; }
  .agent-avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    border: 2px solid white;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    margin-left: -8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  /* MESSAGES */
  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .message-row {
    display: flex;
    gap: 12px;
    max-width: 80%;
  }
  .message-row.me { margin-left: auto; flex-direction: row-reverse; }
  
  .msg-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-size: 14px;
  }
  
  .msg-bubble {
    padding: 12px 16px;
    border-radius: 16px;
    position: relative;
    font-size: 14px;
    line-height: 1.5;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  }
  .msg-bubble.me { background-color: #2563eb; color: white; border-top-right-radius: 2px; }
  .msg-bubble.other { background-color: white; border: 1px solid #e2e8f0; border-top-left-radius: 2px; color: #334155; }
  
  .msg-meta { font-size: 11px; margin-bottom: 4px; display: flex; gap: 6px; align-items: center; }
  .msg-role { padding: 1px 4px; border-radius: 4px; font-size: 10px; text-transform: uppercase; font-weight: bold; }

  /* INPUT AREA */
  .input-area {
    padding: 20px;
    background-color: white;
    border-top: 1px solid #e2e8f0;
  }
  .input-wrapper {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    gap: 10px;
  }
  .input-field {
    flex: 1;
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid #cbd5e1;
    font-size: 15px;
    outline: none;
    transition: border-color 0.2s;
  }
  .input-field:focus { border-color: #2563eb; }
  
  .send-btn {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0 24px;
    cursor: pointer;
    transition: background 0.2s;
  }
  .send-btn:hover { background-color: #1d4ed8; }
  .send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

  .status-bar {
    text-align: right;
    font-size: 12px;
    color: #d97706;
    margin-bottom: 8px;
    font-weight: bold;
    animation: fade 1.5s infinite alternate;
  }

  /* VIEWS */
  .loading-view, .dashboard-view, .feedback-view {
    display: flex; align-items: center; justify-content: center;
    width: 100%; height: 100%;
  }
  .feedback-modal {
    background: white; padding: 32px; border-radius: 24px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    max-width: 400px; width: 100%;
    text-align: center;
  }
  .dashboard-container {
    background: white; width: 90%; max-width: 1000px;
    border-radius: 16px; overflow: hidden;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    height: 90vh; display: flex; flex-direction: column;
  }
  .dash-header { background: #0f172a; color: white; padding: 20px; display: flex; justify-content: space-between; align-items: center; }
  .dash-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; padding: 32px; overflow-y: auto; }
  .dash-card { border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; }
  .chart-placeholder { height: 200px; background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #94a3b8; }

  /* UTILS */
  .bg-indigo { background-color: #e0e7ff; color: #3730a3; }
  .bg-emerald { background-color: #d1fae5; color: #065f46; }
  .bg-amber { background-color: #fef3c7; color: #92400e; }
  .bg-blue { background-color: #dbeafe; color: #1e40af; }
  
  @keyframes pulse {
    0% { box-shadow: 0 0 0 0px rgba(251, 191, 36, 0.7); }
    100% { box-shadow: 0 0 0 10px rgba(251, 191, 36, 0); }
  }
  @keyframes fade { from { opacity: 0.6; } to { opacity: 1; } }
`;

// --- Mock Data ---
const MOCK_BACKEND_DATA = {
  participants: [
    { id: 'u1', name: 'You', role: 'user', avatar: '👤', style: 'bg-blue' },
    { id: 'ai1', name: 'Dr. Orion', role: 'Palliative Care', avatar: '🩺', style: 'bg-indigo' },
    { id: 'ai2', name: 'Counselor Nova', role: 'Addiction Recovery', avatar: '🌱', style: 'bg-emerald' },
    { id: 'ai3', name: 'Guide Atlas', role: 'CBT Specialist', avatar: '🧠', style: 'bg-amber' }
  ],
  initial_messages: [
    { id: 1, senderId: 'system', text: 'Welcome to the Odyssey Circle. This is a safe space.', timestamp: '10:00 AM' },
    { id: 2, senderId: 'ai3', text: 'Hello everyone. I am Atlas. Remember, we are here to support your journey.', timestamp: '10:01 AM' }
  ]
};

export default function App() {
  const [view, setView] = useState('loading'); 
  const [messages, setMessages] = useState([]);
  const [agents, setAgents] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isHandRaised, setIsHandRaised] = useState(false);
  const [moodRating, setMoodRating] = useState(3);
  const [selectedBestCounselor, setSelectedBestCounselor] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    // Simulate Backend Fetch
    setTimeout(() => {
      setAgents(MOCK_BACKEND_DATA.participants.filter(p => p.role !== 'user'));
      setMessages(MOCK_BACKEND_DATA.initial_messages);
      setView('chat');
    }, 1000);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = () => {
    if (!inputText.trim()) return;

    const newMessage = {
      id: Date.now(), senderId: 'u1', text: inputText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isHandRaised: isHandRaised
    };

    setMessages(prev => [...prev, newMessage]);
    setInputText("");
    
    if (isHandRaised) {
      setTimeout(() => {
        const responder = agents[Math.floor(Math.random() * agents.length)];
        setMessages(prev => [...prev, {
          id: Date.now() + 1, senderId: responder.id,
          text: `(Responding to raised hand) I hear you. Regarding "${newMessage.text}"... let's explore that feeling further.`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
        setIsHandRaised(false);
      }, 1500);
    }
  };

  const getSender = (id) => {
    if (id === 'u1') return MOCK_BACKEND_DATA.participants[0];
    if (id === 'system') return { name: 'System', avatar: '⚙️', style: 'bg-gray' };
    return agents.find(a => a.id === id) || { name: '?', avatar: '?', style: '' };
  };

  // --- Views ---

  if (view === 'loading') return (
    <div className="loading-view">
      <style>{css}</style>
      <div style={{display:'flex', alignItems:'center', gap:'10px', color:'#64748b'}}>
        <Activity className="spin" /> Connecting to Odyssey Circle...
      </div>
    </div>
  );

  if (view === 'dashboard') return (
    <div className="dashboard-view">
      <style>{css}</style>
      <div className="dashboard-container">
        <div className="dash-header">
          <h2>Odyssey Metrics</h2>
          <button onClick={() => setView('chat')} style={{background:'rgba(255,255,255,0.2)', border:'none', color:'white', padding:'8px 16px', borderRadius:'6px', cursor:'pointer'}}>Back to Circle</button>
        </div>
        <div className="dash-grid">
          <div className="dash-card">
             <h3>Mood Trend</h3>
             <div className="chart-placeholder"><LineChart size={48} /></div>
          </div>
          <div className="dash-card">
             <h3>Counselor Impact</h3>
             <div className="chart-placeholder"><BarChart size={48} /></div>
          </div>
        </div>
      </div>
    </div>
  );

  if (view === 'feedback') return (
    <div className="feedback-view" style={{background: 'rgba(0,0,0,0.5)', position: 'fixed', top:0, left:0, zIndex:100}}>
      <style>{css}</style>
      <div className="feedback-modal">
        <h2>Session Complete</h2>
        <p>How are you feeling?</p>
        <input type="range" min="1" max="5" value={moodRating} onChange={e=>setMoodRating(e.target.value)} style={{width:'100%', margin:'20px 0'}} />
        <p>Mood: {moodRating}/5</p>
        <button className="send-btn" onClick={() => setView('dashboard')}>Submit Feedback</button>
      </div>
    </div>
  );

  // Chat View
  return (
    <div className="odyssey-app">
      <style>{css}</style>

      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-group">
          <div className="icon-btn" title="Profile"><User /></div>
          <button 
            className={`icon-btn ${isHandRaised ? 'active-hand' : ''}`} 
            onClick={() => setIsHandRaised(!isHandRaised)} 
            title={isHandRaised ? "Lower Hand" : "Raise Hand"}
          >
            <Hand />
          </button>
        </div>
        <div className="sidebar-group">
          <button className="icon-btn" style={{color:'#ef4444', background:'#fef2f2'}} onClick={() => setView('feedback')} title="Leave Session">
            <LogOut />
          </button>
        </div>
      </div>

      {/* Main Area */}
      <div className="chat-area">
        <div className="header">
          <div className="title">Odyssey <span className="tag">#842</span></div>
          <div className="agents-list">
            <span style={{fontSize:'12px', color:'#94a3b8', marginRight:'8px'}}>ACTIVE COUNSELORS:</span>
            {agents.map(a => (
              <div key={a.id} className={`agent-avatar ${a.style}`} title={a.role}>{a.avatar}</div>
            ))}
          </div>
        </div>

        <div className="messages-container">
          {messages.map((msg, i) => {
            const sender = getSender(msg.senderId);
            const isMe = msg.senderId === 'u1';
            const isSystem = msg.senderId === 'system';

            if (isSystem) return <div key={i} style={{textAlign:'center', fontSize:'12px', color:'#94a3b8', margin:'10px 0'}}>{msg.text}</div>;

            return (
              <div key={i} className={`message-row ${isMe ? 'me' : ''}`}>
                <div className={`msg-avatar ${sender.style}`}>{sender.avatar}</div>
                <div>
                  <div className="msg-meta" style={{justifyContent: isMe ? 'flex-end' : 'flex-start'}}>
                    <span style={{fontWeight:'bold'}}>{sender.name}</span>
                    {sender.role !== 'user' && <span className={`msg-role ${sender.style}`}>{sender.role}</span>}
                    <span style={{color:'#cbd5e1'}}>{msg.timestamp}</span>
                  </div>
                  <div className={`msg-bubble ${isMe ? 'me' : 'other'}`}>
                    {msg.text}
                    {msg.isHandRaised && (
                      <div style={{position:'absolute', top:'-10px', right:'-10px', background:'#fbbf24', borderRadius:'50%', padding:'4px', border:'2px solid white'}}>
                        <Hand size={12} color="white" />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
          <div ref={chatEndRef} />
        </div>

        <div className="input-area">
          {isHandRaised && (
            <div className="status-bar">
               ✋ Hand Raised: Counselors will prioritize your next message
            </div>
          )}
          <div className="input-wrapper">
            <input 
              className="input-field" 
              placeholder={isHandRaised ? "Speaking to counselors..." : "Share your thoughts..."}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            />
            <button className="send-btn" onClick={handleSendMessage} disabled={!inputText.trim()}>
              <Send />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}