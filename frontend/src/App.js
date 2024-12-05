import React, { useState, useEffect } from 'react';
import axios from 'axios';
import L from 'leaflet';
import bikeIconImg from './assets/bike.jpg';
import { Container as MapDiv, Marker, InfoWindow, NavermapsProvider, NaverMap, useNavermaps } from 'react-naver-maps';


function App() {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);

  // 커스텀 아이콘 정의
  const bikeIcon = new L.Icon({
    iconUrl: bikeIconImg,
    iconSize: [20, 20],
    iconAnchor: [20, 40],
    popupAnchor: [0, -40],
  });

  // API 호출 함수
  const fetchBikeStations = async () => {
    const API_KEY = '707043564a6d696e37304273454c61'; // 발급받은 API 키 입력
    const baseURL = `http://openapi.seoul.go.kr:8088/${API_KEY}/json/bikeList`;

    try {
      // 1차 호출 (1~1000)
      const response1 = await axios.get(`${baseURL}/1/1000/`);
      const data1 = response1.data.rentBikeStatus.row;

      // 2차 호출 (1001~1471)
      const response2 = await axios.get(`${baseURL}/1001/1471/`);
      const data2 = response2.data.rentBikeStatus.row;

      // 데이터 병합
      const mergedData = [...data1, ...data2].map((station) => ({
        id: station.stationId,
        name: station.stationName,
        lat: parseFloat(station.stationLatitude),
        lng: parseFloat(station.stationLongitude),
        availableBikes: station.parkingBikeTotCnt,
      }));

      // 상태 업데이트
      setStations(mergedData);
      setLoading(false);
    } catch (error) {
      console.error('API 호출 중 오류 발생:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBikeStations();
  }, []);

  return (
    <div className='App'>
      <div className='black-nav bg-gray-800 p-4'>
        <h4 style={{ color: 'white', fontSize: '16px' }}>따맵</h4>
      </div>
      <div className='bg-blue-500 text-white p-4 rounded my-4'>
        {loading ? '대여소 정보를 불러오는 중...' : '자전거 대여소를 검색하세요!'}
      </div>
      <div style={{ height: '500px', marginBottom: '20px' }}>
        <NavermapsProvider ncpClientId='yz53tx4y0m'>
          <MapDiv style={{ width: '100%', height: '600px' }}>
            <NaverMap
              style={{ width: '100%', height: '100%' }}
              defaultCenter={{ lat: 37.5665, lng: 126.978 }}
              defaultZoom={13}
            >
              {stations.map((station) => (
                <Marker
                  key={station.id}
                  position={{ lat: station.lat, lng: station.lng }}
                  onClick={() => alert(`${station.name}\n사용 가능 자전거: ${station.availableBikes}`)}
                />
              ))}
            </NaverMap>
          </MapDiv>
        </NavermapsProvider>
      </div>
    </div>
  );
}

export default App;
