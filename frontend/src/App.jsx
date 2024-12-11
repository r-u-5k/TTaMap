import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {NavermapsProvider} from 'react-naver-maps';
import LoadMap from "./components/MapComponent";


function App() {
  const [loading, setLoading] = useState(true);

  return (
    <div className='App'>
      <div className='black-nav bg-gray-800 p-4'>
        <h4 style={{ color: 'white', fontSize: '16px' }}>따맵</h4>
      </div>
      <div className='bg-blue-500 text-white p-4 rounded my-4'>
        {loading ? '대여소 정보를 불러오는 중...' : '자전거 대여소를 검색하세요!'}
      </div>
      <div style={{ height: '500px', marginBottom: '20px' }}>
        <NavermapsProvider ncpClientId='hkatilxnt0'>
          <LoadMap />
        </NavermapsProvider>
      </div>
    </div>
  );
}

export default App;
