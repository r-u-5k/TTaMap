import { Container as MapDiv, NaverMap, useNavermaps } from 'react-naver-maps';

function MyMap() {
  const navermaps = useNavermaps();
  return (
    <MapDiv style={{ width: '100%', height: '600px' }}>
      <NaverMap
        defaultCenter={new navermaps.LatLng(37.5665, 126.9780)} // 서울의 위도와 경도
        defaultZoom={10} // 줌 레벨
      />
    </MapDiv>
  );
}

export default MyMap;
