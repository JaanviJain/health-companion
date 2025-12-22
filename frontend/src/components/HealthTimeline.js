import React, { useState, useEffect } from 'react';
import { Calendar, FileText, Pill, Activity, Download } from 'lucide-react';

function HealthTimeline({ userId = "demo_user" }) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchTimeline();
  }, [userId]);

  const fetchTimeline = async () => {
    try {
      const response = await fetch(`http://localhost:8000/timeline/${userId}`);
      const data = await response.json();
      setEvents(data.events || []);
    } catch (error) {
      console.error('Failed to fetch timeline:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    // Direct link to download the file
    window.location.href = `http://localhost:8000/generate-report/${userId}`;
  };

  const getIcon = (eventType) => {
    const icons = {
      lab_report: <Activity className="text-blue-500" />,
      prescription: <Pill className="text-green-500" />,
      consultation: <FileText className="text-purple-500" />,
      imaging: <Calendar className="text-orange-500" />
    };
    return icons[eventType] || <FileText />;
  };

  const filteredEvents = filter === 'all' 
    ? events 
    : events.filter(e => e.event_type === filter);

  if (loading) return <div className="p-6 text-center">Loading your health history...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6 mt-8 bg-white rounded-xl shadow-sm border border-gray-100">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Your Health Timeline</h2>
        
        {/* DOWNLOAD BUTTON */}
        <button 
            onClick={handleDownloadPDF}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
            <Download size={18} /> Download Report
        </button>
      </div>
            
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        <button onClick={() => setFilter('all')} className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${filter === 'all' ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}>All</button>
        <button onClick={() => setFilter('lab_report')} className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${filter === 'lab_report' ? 'bg-blue-50 text-blue-600' : 'bg-blue-50 text-blue-600 hover:bg-blue-100'}`}>Labs</button>
        <button onClick={() => setFilter('prescription')} className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${filter === 'prescription' ? 'bg-green-500 text-white' : 'bg-green-50 text-green-600 hover:bg-green-100'}`}>Meds</button>
      </div>

      <div className="space-y-6">
        {filteredEvents.length === 0 ? (
           <p className="text-center text-gray-500 py-8">No records found yet. Upload a document to get started!</p>
        ) : (
          filteredEvents.map((event, index) => (
            <div key={index} className="flex gap-4 items-start group">
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-full bg-white border-2 border-gray-200 flex items-center justify-center shadow-sm group-hover:border-blue-400 transition-colors">
                  {getIcon(event.event_type)}
                </div>
                {index < filteredEvents.length - 1 && (
                  <div className="w-0.5 h-full bg-gray-200 my-2 group-hover:bg-blue-100"></div>
                )}
              </div>
              
              <div className="flex-1 bg-gray-50 rounded-lg p-4 hover:bg-white hover:shadow-md transition-all border border-transparent hover:border-gray-100">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-gray-900">{event.title}</h3>
                    <p className="text-gray-600 text-sm mt-1">{event.description}</p>
                  </div>
                  <span className="text-xs font-medium text-gray-400 bg-white px-2 py-1 rounded-full border border-gray-100">
                    {new Date(event.date).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default HealthTimeline;