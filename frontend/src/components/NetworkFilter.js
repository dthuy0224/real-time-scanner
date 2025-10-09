import React from 'react';

const NetworkFilter = ({ selectedNetwork, onNetworkChange }) => {
  const networks = [
    { value: null, label: 'All Networks', color: 'bg-slate-600' },
    { value: 'ETH', label: 'Ethereum', color: 'bg-purple-600' },
    { value: 'BSC', label: 'BSC', color: 'bg-orange-600' }
  ];

  return (
    <div className="flex items-center space-x-4 mb-6">
      <span className="text-slate-400 font-medium">Filter by Network:</span>
      <div className="flex space-x-2">
        {networks.map((network) => (
          <button
            key={network.value || 'all'}
            onClick={() => onNetworkChange(network.value)}
            className={`
              px-4 py-2 rounded-lg font-medium transition-all
              ${selectedNetwork === network.value
                ? `${network.color} text-white shadow-lg`
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }
            `}
          >
            {network.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default NetworkFilter;


