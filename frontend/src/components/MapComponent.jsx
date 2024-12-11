import {Container as MapDiv, Marker, NaverMap} from 'react-naver-maps';
import React from "react";

function LoadMap({stations}) {
  return (
      <MapDiv style={{width: '100%', height: '100%'}}>
        <NaverMap
            style={{width: '100%', height: '100%'}}
            defaultCenter={{lat: 37.541828, lng: 127.076800}}
            defaultZoom={14}
        >
          {stations.map((station) => (
              <Marker
                  key={station.id}
                  position={{lat: station.lat, lng: station.lng}}
                  onClick={() => alert(`${station.name}\n사용 가능 자전거: ${station.availableBikes}`)}
              />
          ))}
        </NaverMap>
      </MapDiv>
  );
}

export default LoadMap;