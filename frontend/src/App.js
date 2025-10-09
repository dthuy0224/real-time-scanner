import React, { useState, useEffect } from 'react';
import { getNewTokens, getStats } from './services/api';
import TokenTable from './components/TokenTable';
import StatsCards from './components/StatsCards';
import ChartSection from './components/ChartSection';
import Header from './components/Header';
import NetworkFilter from './components/NetworkFilter';

function App() {
  const [tokens, setTokens] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedNetwork, setSelectedNetwork] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [tokensData, statsData] = await Promise.all([
        getNewTokens(currentPage, 20, selectedNetwork, true),
        getStats()
      ]);
      
      setTokens(tokensData);
      setStats(statsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    
    return () => clearInterval(interval);
  }, [currentPage, selectedNetwork]);

  return (
    <div className="min-h-screen bg-slate-900">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        {stats && <StatsCards stats={stats} />}
        
        {/* Network Filter */}
        <NetworkFilter 
          selectedNetwork={selectedNetwork} 
          onNetworkChange={setSelectedNetwork} 
        />
        
        {/* Chart Section */}
        {stats && <ChartSection stats={stats} />}
        
        {/* Token Table */}
        <TokenTable 
          tokens={tokens} 
          loading={loading}
          currentPage={currentPage}
          onPageChange={setCurrentPage}
        />
      </main>
      
      <footer className="bg-slate-800 border-t border-slate-700 py-6 mt-12">
        <div className="container mx-auto px-4 text-center text-slate-400">
          <p>RealTime Token Scanner - Tracking ETH & BSC tokens</p>
        </div>
      </footer>
    </div>
  );
}

export default App;


