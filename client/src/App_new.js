import React from 'react';
import { Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import ProviderSearch from './components/ProviderSearch';
import ProviderResults from './components/ProviderResults';

function App() {
  return (
    <div className="App">
      <header className="bg-primary text-white p-3">
        <h1>Medicare Provider Finder</h1>
      </header>
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<ProviderSearch />} />
          <Route path="/results" element={<ProviderResults />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
