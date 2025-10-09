import React from 'react';

const Header = () => {
  return (
    <header className="gradient-bg shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">
              🔍 RealTime Token Scanner
            </h1>
            <p className="text-purple-200 mt-1">
              Track newly deployed tokens on Ethereum & Binance Smart Chain
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-white text-sm font-medium">Live</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;


