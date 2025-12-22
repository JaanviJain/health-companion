import React, { useState } from 'react';
import DocumentUpload from './components/DocumentUpload';
import HealthTimeline from './components/HealthTimeline';
import VoiceChat from './components/VoiceChat';
import EmergencyAccess from './components/EmergencyAccess';
// ADDED: ArrowLeft icon for the back button
import { LayoutDashboard, Upload, MessageSquare, AlertCircle, ArrowLeft } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('upload'); 
  const userId = "demo_user"; 

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">H</div>
            <h1 className="text-xl font-bold text-gray-800">Health Companion</h1>
          </div>
          
          {/* TOGGLE BUTTON LOGIC */}
          {activeTab === 'emergency' ? (
            <button 
              onClick={() => setActiveTab('upload')} // GO BACK TO DASHBOARD
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-bold border border-gray-300 hover:bg-gray-200 transition-colors"
            >
              <ArrowLeft size={18} /> Exit Emergency View
            </button>
          ) : (
            <button 
              onClick={() => setActiveTab('emergency')} // ENTER EMERGENCY MODE
              className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg font-bold border border-red-200 hover:bg-red-100 transition-colors animate-pulse"
            >
              <AlertCircle size={18} /> Emergency Mode
            </button>
          )}
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8">
        
        {/* Navigation Tabs - Hidden when in Emergency Mode */}
        {activeTab !== 'emergency' && (
            <div className="flex justify-center mb-8">
            <div className="bg-white p-1 rounded-xl shadow-sm border border-gray-200 inline-flex">
                <button onClick={() => setActiveTab('upload')} className={`flex items-center gap-2 px-6 py-3 rounded-lg text-sm font-medium transition-all ${activeTab === 'upload' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50'}`}>
                <Upload size={18} /> Upload
                </button>
                <button onClick={() => setActiveTab('timeline')} className={`flex items-center gap-2 px-6 py-3 rounded-lg text-sm font-medium transition-all ${activeTab === 'timeline' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50'}`}>
                <LayoutDashboard size={18} /> Timeline
                </button>
                <button onClick={() => setActiveTab('chat')} className={`flex items-center gap-2 px-6 py-3 rounded-lg text-sm font-medium transition-all ${activeTab === 'chat' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50'}`}>
                <MessageSquare size={18} /> Assistant
                </button>
            </div>
            </div>
        )}

        {/* Content Area */}
        <div className="animate-in fade-in zoom-in duration-300">
          {activeTab === 'upload' && <DocumentUpload userId={userId} />}
          {activeTab === 'timeline' && <HealthTimeline userId={userId} />}
          {activeTab === 'chat' && <VoiceChat userId={userId} />}
          {activeTab === 'emergency' && <EmergencyAccess userId={userId} />}
        </div>

      </main>
    </div>
  );
}

export default App;