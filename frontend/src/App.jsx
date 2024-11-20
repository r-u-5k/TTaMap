import './App.css';
import { NavermapsProvider } from 'react-naver-maps';
import { Routes, Route, Link } from 'react-router-dom';
import React, { Suspense } from 'react';
import MyMap from './components/MapComponent';

function Home() {
  return <h1>Home Page</h1>;
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
          </ul>
        </nav>

        {/* 라우팅 설정 */}
        <Suspense fallback={<div>로딩 중...</div>}>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/map' element={<MyMap />} />
          </Routes>
        </Suspense>
      </div>
    </NavermapsProvider>
  );
}

export default App;

