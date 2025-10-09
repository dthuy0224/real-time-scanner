import React from 'react';
import { formatDistanceToNow } from 'date-fns';

const TokenTable = ({ tokens, loading, currentPage, onPageChange }) => {
  const truncateAddress = (address) => {
    return `${address.slice(0, 8)}...${address.slice(-6)}`;
  };

  const getNetworkBadge = (network) => {
    const badges = {
      ETH: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
      BSC: 'bg-orange-500/20 text-orange-300 border-orange-500/30'
    };
    
    return badges[network] || 'bg-slate-500/20 text-slate-300 border-slate-500/30';
  };

  const getRiskBadge = (score) => {
    if (score >= 7) return { label: 'High Risk', color: 'bg-red-500/20 text-red-300 border-red-500/30' };
    if (score >= 4) return { label: 'Medium Risk', color: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30' };
    return { label: 'Low Risk', color: 'bg-green-500/20 text-green-300 border-green-500/30' };
  };

  const getExplorerUrl = (network, address) => {
    const explorers = {
      ETH: `https://etherscan.io/address/${address}`,
      BSC: `https://bscscan.com/address/${address}`
    };
    return explorers[network];
  };

  if (loading) {
    return (
      <div className="bg-slate-800 rounded-xl p-12 shadow-lg border border-slate-700">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
          <span className="ml-4 text-slate-400">Loading tokens...</span>
        </div>
      </div>
    );
  }

  if (tokens.length === 0) {
    return (
      <div className="bg-slate-800 rounded-xl p-12 shadow-lg border border-slate-700">
        <div className="text-center text-slate-400">
          <p className="text-xl">No tokens found</p>
          <p className="mt-2">Waiting for new token deployments...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-xl shadow-lg border border-slate-700 overflow-hidden">
      <div className="p-6 border-b border-slate-700">
        <h2 className="text-2xl font-bold text-white">🪙 Recently Detected Tokens</h2>
        <p className="text-slate-400 mt-1">Real-time token deployments on ETH and BSC</p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-900">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                Token
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                Address
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                Network
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                Block
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                Supply
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                Risk
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                Detected
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700">
            {tokens.map((token) => {
              const risk = getRiskBadge(token.risk_score);
              return (
                <tr key={token.id} className="hover:bg-slate-700/50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="font-medium text-white">
                        {token.name || 'Unknown'}
                      </div>
                      <div className="text-sm text-slate-400">
                        {token.symbol || 'N/A'} • {token.decimals || '?'} decimals
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <code className="text-sm text-purple-300 bg-purple-900/20 px-2 py-1 rounded">
                      {truncateAddress(token.address)}
                    </code>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${getNetworkBadge(token.network)}`}>
                      {token.network}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                    {token.block_number.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                    {token.total_supply ? parseFloat(token.total_supply).toExponential(2) : 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${risk.color}`}>
                      {risk.label}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-400">
                    {formatDistanceToNow(new Date(token.timestamp), { addSuffix: true })}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <a
                      href={getExplorerUrl(token.network, token.address)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-purple-400 hover:text-purple-300 font-medium"
                    >
                      View →
                    </a>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      
      {/* Pagination */}
      <div className="px-6 py-4 border-t border-slate-700 flex items-center justify-between">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="px-4 py-2 bg-slate-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-600 transition-colors"
        >
          Previous
        </button>
        <span className="text-slate-400">Page {currentPage}</span>
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={tokens.length < 20}
          className="px-4 py-2 bg-slate-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-600 transition-colors"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default TokenTable;


