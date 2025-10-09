import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ChartSection = ({ stats }) => {
  const hourlyData = stats.hourly_distribution.map(item => ({
    time: new Date(item.hour).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
    tokens: item.count
  }));

  const networkData = Object.entries(stats.by_network).map(([network, count]) => ({
    network,
    count
  }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      {/* Hourly Distribution */}
      <div className="bg-slate-800 rounded-xl p-6 shadow-lg border border-slate-700">
        <h3 className="text-xl font-bold text-white mb-4">📊 Tokens per Hour (Last 24h)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={hourlyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis 
              dataKey="time" 
              stroke="#94a3b8"
              tick={{ fill: '#94a3b8' }}
              interval={2}
            />
            <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8' }} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1e293b', 
                border: '1px solid #475569',
                borderRadius: '8px'
              }}
            />
            <Legend wrapperStyle={{ color: '#94a3b8' }} />
            <Line 
              type="monotone" 
              dataKey="tokens" 
              stroke="#8b5cf6" 
              strokeWidth={2}
              dot={{ fill: '#8b5cf6', r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Network Distribution */}
      <div className="bg-slate-800 rounded-xl p-6 shadow-lg border border-slate-700">
        <h3 className="text-xl font-bold text-white mb-4">🌐 Tokens by Network</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={networkData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis dataKey="network" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} />
            <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8' }} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1e293b', 
                border: '1px solid #475569',
                borderRadius: '8px'
              }}
            />
            <Legend wrapperStyle={{ color: '#94a3b8' }} />
            <Bar dataKey="count" fill="#10b981" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ChartSection;


