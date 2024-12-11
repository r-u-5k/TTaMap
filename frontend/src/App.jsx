import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { NavermapsProvider } from 'react-naver-maps';
import LoadMap from "./components/MapComponent";

function App() {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBikeStations = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/station/data/all');
        const data = response.data;

        const stations = data.map((station) => ({
          id: station.stationId,
          name: station.stationName,
          lat: parseFloat(station.stationLatitude),
          lng: parseFloat(station.stationLongitude),
          availableBikes: station.parkingBikeTotCnt,
        }));

        setStations(stations);
        setLoading(false);
      } catch (error) {
        console.error('API 호출 중 오류 발생:', error);
        setLoading(false);
      }
    };

    fetchBikeStations();
  }, []);

  return (
      <div className='App'>
        <div className='black-nav bg-gray-800 p-4'>
          <h4 style={{ color: 'white', fontSize: '16px' }}>따맵</h4>
        </div>
        <div style={{ height: '600px', marginBottom: '20px' }}>
          <NavermapsProvider ncpClientId='hkatilxnt0'>
            <LoadMap stations={stations} />
          </NavermapsProvider>
        </div>
      </div>
  );
}

export default App;