import React, { useState } from 'react';
import { Mic, MicOff, Send, MessageSquare } from 'lucide-react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

function VoiceChat({ userId = "demo_user" }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hello! I'm your health assistant. Ask me about your records." }
  ]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { transcript, listening, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition();

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = { role: 'user', content: text };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, message: text })
      });
      
      const data = await response.json();
      const assistantMessage = { role: 'assistant', content: data.response };
      setMessages(prev => [...prev, assistantMessage]);
      
      // Text-to-speech
      speakResponse(data.response);
      
    } catch (error) {
      console.error('Chat failed:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I had trouble connecting to the server." }]);
    } finally {
      setLoading(false);
    }
  };

  const speakResponse = (text) => {
    // Simple browser text-to-speech
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      window.speechSynthesis.speak(utterance);
    }
  };

  const handleMicClick = () => {
    if (listening) {
      SpeechRecognition.stopListening();
      if (transcript) {
        sendMessage(transcript);
        resetTranscript();
      }
    } else {
      resetTranscript();
      SpeechRecognition.startListening({ continuous: true });
    }
  };

  if (!browserSupportsSpeechRecognition) {
    return <div>Browser doesn't support speech recognition.</div>;
  }

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-sm border border-gray-100 mt-8">
      <div className="flex items-center gap-2 mb-4">
        <MessageSquare className="text-blue-500" />
        <h2 className="text-2xl font-bold text-gray-800">Health Assistant</h2>
      </div>

      <div className="bg-gray-50 rounded-lg p-4 h-96 overflow-y-auto mb-4 border border-gray-200">
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-4 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-2xl ${
              msg.role === 'user' 
                ? 'bg-blue-600 text-white rounded-br-none' 
                : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && <div className="text-sm text-gray-500 animate-pulse">Thinking...</div>}
        {listening && <div className="text-sm text-red-500 font-medium animate-pulse">Listening: {transcript}</div>}
      </div>

      <div className="flex gap-2">
        <button
          onClick={handleMicClick}
          className={`p-3 rounded-full transition-all ${
            listening ? 'bg-red-500 text-white animate-pulse' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          {listening ? <MicOff size={24} /> : <Mic size={24} />}
        </button>

        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage(inputText)}
          placeholder="Type or speak..."
          className="flex-1 border border-gray-300 rounded-full px-6 focus:outline-none focus:border-blue-500"
        />
        
        <button
          onClick={() => sendMessage(inputText)}
          disabled={loading || !inputText.trim()}
          className="bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 disabled:bg-gray-300 transition-colors"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}

export default VoiceChat;