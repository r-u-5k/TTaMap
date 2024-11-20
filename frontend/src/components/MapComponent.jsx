import React, { useState, useEffect, startTransition } from 'react';
import { Container as MapDiv, NaverMap, useNavermaps } from 'react-naver-maps';

function LoadMap() {
  const navermaps = useNavermaps();
  const [mapLoaded, setMapLoaded] = useState(false);

  useEffect(() => {
    startTransition(() => {
      setMapLoaded(true);
    });
  }, [navermaps]);

  if (!mapLoaded) {
    return <div>지도를 불러오는 중...</div>;
  }

  return (
    <MapDiv style={{ width: '100%', height: '600px' }}>
      <NaverMap
        defaultCenter={new navermaps.LatLng(37.5408, 127.0766)} // 서울 위도, 경도
        defaultZoom={16}
      />
    </MapDiv>
  );
}

export default LoadMap;
