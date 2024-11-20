import { Container as MapDiv, NaverMap, useNavermaps } from 'react-naver-maps';

function MyMap() {
  const navermaps = useNavermaps();
  return (
    <MapDiv style={{ width: '100%', height: '600px' }}>
      <NaverMap
        defaultCenter={new navermaps.LatLng(37.540797, 127.076583)} // 위도, 경도
        defaultZoom={16} // 줌 레벨
      />
    </MapDiv>
  );
}

export default MyMap;
