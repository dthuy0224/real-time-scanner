import React from 'react';

const StatsCards = ({ stats }) => {
  const cards = [
    {
      title: 'Total Tokens',
      value: stats.total_tokens.toLocaleString(),
      icon: '📊',
      color: 'from-blue-500 to-blue-600'
    },
    {
      title: 'Last 24 Hours',
      value: stats.tokens_last_24h.toLocaleString(),
      icon: '📈',
      color: 'from-green-500 to-green-600'
    },
    {
      title: 'Last Hour',
      value: stats.tokens_last_hour.toLocaleString(),
      icon: '⚡',
      color: 'from-yellow-500 to-yellow-600'
    },
    {
      title: 'ETH Tokens',
      value: (stats.by_network.ETH || 0).toLocaleString(),
      icon: '⟠',
      color: 'from-purple-500 to-purple-600'
    },
    {
      title: 'BSC Tokens',
      value: (stats.by_network.BSC || 0).toLocaleString(),
      icon: '🔶',
      color: 'from-orange-500 to-orange-600'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
      {cards.map((card, index) => (
        <div
          key={index}
          className="bg-slate-800 rounded-xl p-6 shadow-lg border border-slate-700 card-hover"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm font-medium">{card.title}</p>
              <p className="text-2xl font-bold text-white mt-2">{card.value}</p>
            </div>
            <div className={`text-4xl bg-gradient-to-r ${card.color} p-3 rounded-lg`}>
              {card.icon}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StatsCards;


