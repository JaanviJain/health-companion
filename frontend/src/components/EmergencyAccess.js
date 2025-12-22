import React, { useState, useEffect } from 'react';
import { AlertCircle, QrCode } from 'lucide-react';

function EmergencyAccess({ userId = "demo_user" }) {
  const [profile, setProfile] = useState(null);
  const [qrCode, setQrCode] = useState('');

  useEffect(() => {
    fetchEmergencyData();
  }, [userId]);

  const fetchEmergencyData = async () => {
    try {
      const profileRes = await fetch(`http://localhost:8000/emergency-profile/${userId}`);
      const profileData = await profileRes.json();
      setProfile(profileData);

      const qrRes = await fetch(`http://localhost:8000/emergency-qr/${userId}`);
      const qrData = await qrRes.json();
      setQrCode(qrData.qr_code);
    } catch (err) {
      console.error("Error loading emergency data", err);
    }
  };

  if (!profile) return <div className="p-6 text-center">Loading Emergency Data...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6 mt-8">
      {/* Red Alert Header */}
      <div className="bg-red-50 border-2 border-red-500 rounded-xl p-6 mb-8 flex items-start gap-4 shadow-sm">
        <div className="p-3 bg-red-100 rounded-full">
            <AlertCircle className="text-red-600" size={32} />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-red-700">Emergency Access Card</h2>
          <p className="text-red-600 mt-1">
            Show this screen to First Responders. It contains critical medical information.
          </p>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {/* Left Side: Medical Info */}
        <div className="md:col-span-2 space-y-6">
            
            <div className="grid grid-cols-2 gap-4">
                <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
                    <h4 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-1">Blood Type</h4>
                    <p className="text-3xl font-extrabold text-gray-800">{profile.blood_type}</p>
                </div>
                <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
                    <h4 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-1">Emergency Contact</h4>
                    <p className="text-lg font-bold text-gray-800">{profile.emergency_contact}</p>
                </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h4 className="text-red-500 font-bold uppercase tracking-wider mb-3 flex items-center gap-2">
                    <AlertCircle size={16} /> Allergies
                </h4>
                <div className="flex flex-wrap gap-2">
                    {profile.allergies.map((allergy, idx) => (
                        <span key={idx} className="px-3 py-1 bg-red-100 text-red-700 rounded-full font-medium">
                            {allergy}
                        </span>
                    ))}
                </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h4 className="text-blue-500 font-bold uppercase tracking-wider mb-3">Chronic Conditions</h4>
                <ul className="list-disc list-inside space-y-2">
                    {profile.chronic_conditions.map((item, idx) => (
                        <li key={idx} className="text-gray-700 font-medium">{item}</li>
                    ))}
                </ul>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h4 className="text-green-500 font-bold uppercase tracking-wider mb-3">Current Medications</h4>
                <ul className="space-y-2">
                    {profile.current_medications.map((med, idx) => (
                        <li key={idx} className="flex items-center gap-2 text-gray-700">
                            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                            {med}
                        </li>
                    ))}
                </ul>
            </div>
        </div>

        {/* Right Side: QR Code */}
        <div className="md:col-span-1">
            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 text-center sticky top-8">
                <h3 className="font-bold text-gray-800 mb-4 flex items-center justify-center gap-2">
                    <QrCode size={20} /> EMT Scan Code
                </h3>
                <div className="bg-gray-50 p-4 rounded-lg inline-block mb-4">
                    {qrCode && (
                        <img 
                           src={`data:image/png;base64,${qrCode}`} 
                           alt="Emergency QR Code"
                           className="w-48 h-48"
                        />
                    )}
                </div>
                <p className="text-xs text-gray-500 leading-relaxed">
                    Scanning this code grants temporary access to your full medical timeline for emergency personnel.
                </p>
            </div>
        </div>
      </div>
    </div>
  );
}

export default EmergencyAccess;