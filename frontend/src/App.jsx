import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_URL = `${API_BASE_URL}/traffic/live`;
const HISTORY_URL = `${API_BASE_URL}/traffic/history`;
const STREAM_URL = `${API_BASE_URL}/traffic/stream`;
const VIDEOS_URL = `${API_BASE_URL}/traffic/videos`;

const ALL_CLASSES = ['car', 'motorcycle', 'bus', 'truck', 'microbus'];

function App() {
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [fullHistory, setFullHistory] = useState([]);
  const [apiConnected, setApiConnected] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [streamLatency, setStreamLatency] = useState(0);
  const [streamLoading, setStreamLoading] = useState(true);
  const [streamError, setStreamError] = useState(false);
  const [availableVideos, setAvailableVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState('input.mp4');
  const [streamKey, setStreamKey] = useState(Date.now());
  const streamRef = useRef(null);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const response = await fetch(VIDEOS_URL);
        if (response.ok) {
          const result = await response.json();
          setAvailableVideos(result);
        }
      } catch (error) {
        console.error('Error fetching videos:', error);
      }
    };
    fetchVideos();
  }, []);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(`${HISTORY_URL}?limit=100`);
        if (response.ok) {
          const result = await response.json();
          setFullHistory(result.history.map(item => ({
            time: new Date(item.timestamp).toLocaleTimeString(),
            total: item.vehicle_counts.total,
            congestion: item.congestion_index
          })));
        }
      } catch (error) {
        console.error('Error fetching history:', error);
      }
    };
    fetchHistory();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      const startTime = Date.now();
      try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('API not available');
        const result = await response.json();
        setData(result);
        setApiConnected(true);
        setLastUpdated(new Date());
        setStreamLatency(Date.now() - startTime);
        if (result.current_video) {
          setSelectedVideo(result.current_video);
        }
        
        setHistory(prev => {
          const newHistory = [...prev, {
            time: new Date().toLocaleTimeString(),
            total: result.vehicle_counts.total,
            congestion: result.congestion_index
          }];
          return newHistory.slice(-30);
        });
      } catch (error) {
        console.error('Error fetching data:', error);
        setApiConnected(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const refreshStream = () => {
      setStreamKey(Date.now());
    };
    const interval = setInterval(refreshStream, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleVideoChange = async (videoName) => {
    try {
      const response = await fetch(`${VIDEOS_URL}/${videoName}`, {
        method: 'POST',
      });
      if (response.ok) {
        setSelectedVideo(videoName);
        setStreamKey(Date.now());
      }
    } catch (error) {
      console.error('Error changing video:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'LOW': return 'bg-green-500';
      case 'MODERATE': return 'bg-yellow-500';
      case 'HEAVY': return 'bg-orange-500';
      case 'CRITICAL': return 'bg-red-600';
      default: return 'bg-gray-500';
    }
  };

  const getStatusTextColor = (status) => {
    switch (status) {
      case 'LOW': return 'text-green-400';
      case 'MODERATE': return 'text-yellow-400';
      case 'HEAVY': return 'text-orange-400';
      case 'CRITICAL': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const handleStreamLoad = () => {
    setStreamLoading(false);
    setStreamError(false);
  };

  const handleStreamError = () => {
    setStreamLoading(false);
    setStreamError(true);
    setStreamKey(Date.now());
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        <header className="mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/30">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl md:text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Nepal Traffic Intelligence
                </h1>
                <div className="flex items-center gap-2">
                  <p className="text-slate-400 text-sm">
                    Real-time Traffic Analytics Dashboard
                  </p>
                  <span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded-full border border-purple-500/30">
                    Model: Nepal Traffic v1
                  </span>
                  <span className="text-xs px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded-full border border-blue-500/30">
                    Powered by YOLOv8
                  </span>
                </div>
              </div>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              {availableVideos.length > 0 && (
                <select 
                  value={selectedVideo}
                  onChange={(e) => handleVideoChange(e.target.value)}
                  className="bg-slate-700/50 border border-slate-600 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:border-blue-500"
                >
                  {availableVideos.map(video => (
                    <option key={video} value={video}>{video}</option>
                  ))}
                </select>
              )}
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full border ${apiConnected ? 'bg-green-500/20 border-green-500' : 'bg-red-500/20 border-red-500'}`}>
                <div className={`w-2.5 h-2.5 rounded-full animate-pulse ${apiConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className={`text-sm font-medium ${apiConnected ? 'text-green-400' : 'text-red-400'}`}>
                  {apiConnected ? 'API Connected' : 'API Disconnected'}
                </span>
              </div>
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border bg-slate-700/30 border-slate-600">
                <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span className="text-slate-400 text-sm font-medium">{streamLatency}ms</span>
              </div>
            </div>
          </div>
          {data && (
            <div className="flex flex-wrap items-center gap-4 mt-4">
              <div className="flex items-center gap-2 text-slate-400 text-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span className="font-medium text-slate-300">{data.intersection}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400 text-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Last updated: {lastUpdated?.toLocaleString()}</span>
              </div>
            </div>
          )}
        </header>

        {data && data.alerts && data.alerts.length > 0 && (
          <div className="mb-6 space-y-2">
            {data.alerts.map((alert, idx) => (
              <div key={idx} className={`flex items-center gap-3 p-4 rounded-xl border ${
                alert.type === 'CRITICAL' ? 'bg-red-500/10 border-red-500' :
                alert.type === 'WARNING' ? 'bg-yellow-500/10 border-yellow-500' :
                'bg-blue-500/10 border-blue-500'
              }`}>
                <svg className={`w-6 h-6 ${
                  alert.type === 'CRITICAL' ? 'text-red-400' :
                  alert.type === 'WARNING' ? 'text-yellow-400' : 'text-blue-400'
                }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div>
                  <p className={`font-bold ${
                    alert.type === 'CRITICAL' ? 'text-red-400' :
                    alert.type === 'WARNING' ? 'text-yellow-400' : 'text-blue-400'
                  }`}>{alert.type}</p>
                  <p className="text-slate-300 text-sm">{alert.message}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {data ? (
          <>
            <div className="mb-6 bg-gradient-to-br from-slate-800 to-slate-900 border border-blue-500/30 rounded-2xl p-5 shadow-2xl shadow-blue-500/10">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4 gap-3">
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <div className="w-3 h-3 bg-red-600 rounded-full animate-pulse"></div>
                    <div className="absolute inset-0 w-3 h-3 bg-red-600 rounded-full animate-ping opacity-75"></div>
                  </div>
                  <h3 className="text-xl font-bold text-white">LIVE - Kathmandu Durbar Marg</h3>
                </div>
                <a 
                  href={STREAM_URL} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-sm text-blue-400 hover:text-blue-300 underline"
                >
                  Open Stream Directly
                </a>
              </div>
              <div className="relative rounded-xl overflow-hidden bg-black aspect-video border-2 border-slate-700">
                {streamLoading && (
                  <div className="absolute inset-0 flex items-center justify-center bg-slate-900/90 z-10">
                    <div className="text-center">
                      <div className="w-16 h-16 border-4 border-slate-600 border-t-blue-500 rounded-full animate-spin mx-auto mb-4"></div>
                      <p className="text-slate-400 text-lg">Connecting to stream...</p>
                    </div>
                  </div>
                )}
                {streamError && (
                  <div className="absolute inset-0 flex items-center justify-center bg-slate-900/90 z-10">
                    <div className="text-center">
                      <svg className="w-16 h-16 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      <p className="text-red-400 text-lg">Stream unavailable</p>
                      <p className="text-slate-500 text-sm mt-2">Check backend is running</p>
                    </div>
                  </div>
                )}
                <img 
                  key={streamKey}
                  ref={streamRef}
                  src={`${STREAM_URL}?t=${streamKey}`} 
                  alt="Live Traffic Feed" 
                  className="w-full h-full object-cover"
                  onLoad={handleStreamLoad}
                  onError={handleStreamError}
                  style={{ display: streamError ? 'none' : 'block' }}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4 mb-6">
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-4 hover:border-blue-500/50 transition-all duration-300 shadow-xl hover:shadow-blue-500/10">
                <p className="text-slate-400 text-xs font-medium mb-2">Avg Confidence</p>
                <p className={`text-2xl font-bold ${data.avg_confidence >= 0.7 ? 'text-green-400' : data.avg_confidence >= 0.5 ? 'text-yellow-400' : 'text-red-400'}`}>
                  {data.avg_confidence?.toFixed(2) || '0.00'}
                </p>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-4 hover:border-blue-500/50 transition-all duration-300 shadow-xl hover:shadow-blue-500/10">
                <p className="text-slate-400 text-xs font-medium mb-2">Active Now</p>
                <p className="text-2xl font-bold text-blue-400">
                  {data.current_frame_count || 0}
                </p>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-4 hover:border-blue-500/50 transition-all duration-300 shadow-xl hover:shadow-blue-500/10">
                <p className="text-slate-400 text-xs font-medium mb-2">Total Counted</p>
                <p className="text-2xl font-bold text-white animate-pulse">
                  {data.vehicle_counts.total}
                </p>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-4 hover:border-blue-500/50 transition-all duration-300 shadow-xl hover:shadow-blue-500/10">
                <p className="text-slate-400 text-xs font-medium mb-2">Vehicles/min</p>
                <p className="text-2xl font-bold text-purple-400">
                  {data.detection_rate || 0}
                </p>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-4 hover:border-blue-500/50 transition-all duration-300 shadow-xl hover:shadow-blue-500/10 col-span-2">
                <p className="text-slate-400 text-xs font-medium mb-2">Peak Time</p>
                <p className="text-2xl font-bold text-orange-400">
                  {data.peak_time || '--:--'}
                </p>
                <p className="text-xs text-slate-500">
                  {data.peak_vehicles ? `(${data.peak_vehicles} vehicles)` : ''}
                </p>
              </div>

              {ALL_CLASSES.slice(0, 3).map((cls) => (
                <div key={cls} className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-4 hover:border-blue-500/50 transition-all duration-300 shadow-xl hover:shadow-blue-500/10">
                  <p className="text-slate-400 text-xs font-medium mb-1 capitalize">{cls}</p>
                  <p className="text-2xl font-bold text-white">
                    {data.vehicle_counts.per_class?.[cls] || 0}
                  </p>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              {ALL_CLASSES.slice(3, 5).map((cls) => (
                <div key={cls} className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-5 hover:border-blue-500/50 transition-all duration-300 shadow-xl hover:shadow-blue-500/10">
                  <div className="flex items-center justify-between mb-3">
                    <div className="w-10 h-10 bg-purple-500/20 rounded-xl flex items-center justify-center">
                      <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM9 3a2 2 0 11-4 0 2 2 0 014 0zM15 17a2 2 0 11-4 0 2 2 0 014 0zM15 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a5 5 0 0110 0H7z" />
                      </svg>
                    </div>
                  </div>
                  <p className="text-slate-400 text-xs font-medium mb-1 capitalize">{cls}</p>
                  <p className="text-2xl font-bold text-white">
                    {data.vehicle_counts.per_class?.[cls] || 0}
                  </p>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
              <div className="lg:col-span-2 bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-5 shadow-xl">
                <h3 className="text-lg font-semibold text-white mb-4">Vehicle Count & Congestion Trend</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={history}>
                      <defs>
                        <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorCongestion" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis dataKey="time" stroke="#94a3b8" tick={{fontSize: 12}} />
                      <YAxis stroke="#94a3b8" tick={{fontSize: 12}} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569', borderRadius: '8px' }}
                        itemStyle={{ color: '#f1f5f9' }}
                      />
                      <Area type="monotone" dataKey="total" stroke="#3b82f6" fillOpacity={1} fill="url(#colorTotal)" name="Total Vehicles" />
                      <Area type="monotone" dataKey="congestion" stroke="#f59e0b" fillOpacity={1} fill="url(#colorCongestion)" name="Congestion" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-5 shadow-xl">
                <h3 className="text-lg font-semibold text-white mb-4">Congestion Level</h3>
                <div className="flex flex-col items-center gap-4">
                  <div className="w-full">
                    <div className="flex justify-between mb-2">
                      <span className="text-slate-400 text-sm">0%</span>
                      <span className={`text-2xl font-bold ${getStatusTextColor(data.traffic_status)}`}>
                        {(data.congestion_index * 100).toFixed(0)}%
                      </span>
                      <span className="text-slate-400 text-sm">100%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-4 overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${getStatusColor(data.traffic_status)}`}
                        style={{ width: `${data.congestion_index * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3 w-full">
                    <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3 text-center">
                      <div className="text-green-400 font-bold">LOW</div>
                      <div className="text-slate-500 text-xs">&lt;25%</div>
                    </div>
                    <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3 text-center">
                      <div className="text-yellow-400 font-bold">MODERATE</div>
                      <div className="text-slate-500 text-xs">25-50%</div>
                    </div>
                    <div className="bg-orange-500/10 border border-orange-500/30 rounded-lg p-3 text-center">
                      <div className="text-orange-400 font-bold">HEAVY</div>
                      <div className="text-slate-500 text-xs">50-75%</div>
                    </div>
                    <div className="bg-red-600/10 border border-red-600/30 rounded-lg p-3 text-center">
                      <div className="text-red-400 font-bold">CRITICAL</div>
                      <div className="text-slate-500 text-xs">&gt;75%</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="flex items-center justify-center h-96">
            <div className="text-center">
              <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-slate-400 text-lg">Connecting to backend...</p>
              <p className="text-slate-500 text-sm mt-2">Make sure the FastAPI server is running on http://localhost:8000</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
