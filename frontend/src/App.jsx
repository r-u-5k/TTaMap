import logo from './logo.svg';
import './App.css';
import { NavermapsProvider } from 'react-naver-maps';
import { Routes, Route, Link } from 'react-router-dom';
import React, { Suspense } from 'react';
import LoadMap from './components/MapComponent';
import CardExpiration from './components/CardComponent';

function Home() {
    return (
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <p>
              Edit <code>src/App.js</code> and save to reload.
            </p>
            <a
              className="App-link"
              href="https://reactjs.org"
              target="_blank"
              rel="noopener noreferrer"
            >
              Learn React
            </a>
          </header>
        </div>
      );
}

function App() {
  return (
    <NavermapsProvider ncpClientId='yz53tx4y0m'>
      <div style={{ margin: '20px' }}>
        <nav>
          {/* 네비게이션 메뉴 */}
          <ul>
            <li>
              <Link to='/'>홈</Link>
            </li>
            <li>
              <Link to='/map'>지도</Link>
            </li>
            <li>
              <Link to='/card'>카드</Link>
            </li>
          </ul>
        </nav>

        {/* 라우팅 설정 */}
        <Suspense fallback={<div>로딩 중...</div>}>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/map' element={<LoadMap />} />
            <Route path='/card' element={<CardExpiration />} />
          </Routes>
        </Suspense>
      </div>
    </NavermapsProvider>
  );
}

export default App;

