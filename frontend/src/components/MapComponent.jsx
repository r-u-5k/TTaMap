/* global naver */
import React, { useEffect } from 'react';
const api_key = "Jik3kwz85G7Q08Aq0HRnUVStZz0mtWz0OgS%2B610Ykf8"

const MapComponent = () => {
    useEffect(() => {
        const initializeMap = () => {
            const mapOptions = {
                center: new naver.maps.LatLng(37.3595704, 127.105399),
                zoom: 10,
            };

            const map = new naver.maps.Map('map', mapOptions);

            const sx = 126.93737555322481;
            const sy = 37.55525165729346;
            const ex = 126.88265238619182;
            const ey = 37.481440035175375;

            const searchPubTransPathAJAX = () => {
                const xhr = new XMLHttpRequest();
                const url = `https://api.odsay.com/v1/api/searchPubTransPathT?SX=${sx}&SY=${sy}&EX=${ex}&EY=${ey}&apiKey=${api_key}`;
                xhr.open('GET', url, true);
                xhr.send();
                xhr.onreadystatechange = () => {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        callMapObjApiAJAX(response.result.path[0].info.mapObj);
                    }
                };
            };

            const callMapObjApiAJAX = (mapObj) => {
                const xhr = new XMLHttpRequest();
                const url = `https://api.odsay.com/v1/api/loadLane?mapObject=0:0@${mapObj}&apiKey=${api_key}`;
                xhr.open('GET', url, true);
                xhr.send();
                xhr.onreadystatechange = () => {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        const resultJsonData = JSON.parse(xhr.responseText);
                        drawNaverMarker(sx, sy); // 출발지 마커 표시
                        drawNaverMarker(ex, ey); // 도착지 마커 표시
                        drawNaverPolyLine(resultJsonData);

                        if (resultJsonData.result.boundary) {
                            const boundary = new naver.maps.LatLngBounds(
                                new naver.maps.LatLng(resultJsonData.result.boundary.top, resultJsonData.result.boundary.left),
                                new naver.maps.LatLng(resultJsonData.result.boundary.bottom, resultJsonData.result.boundary.right)
                            );
                            map.panToBounds(boundary);
                        }
                    }
                };
            };

            const drawNaverMarker = (x, y) => {
                new naver.maps.Marker({
                    position: new naver.maps.LatLng(y, x),
                    map,
                });
            };

            const drawNaverPolyLine = (data) => {
                data.result.lane.forEach((lane) => {
                    lane.section.forEach((section) => {
                        const lineArray = section.graphPos.map(
                            (pos) => new naver.maps.LatLng(pos.y, pos.x)
                        );
                        new naver.maps.Polyline({
                            map,
                            path: lineArray,
                            strokeWeight: 3,
                            strokeColor:
                                lane.type === 1 ? '#003499' : lane.type === 2 ? '#37b42d' : '#000000',
                        });
                    });
                });
            };

            searchPubTransPathAJAX();
        };

        if (window.naver) {
            initializeMap();
        } else {
            const script = document.createElement('script');
            script.src =
                'https://oapi.map.naver.com/openapi/v3/maps.js?ncpClientId=yz53tx4y0m';
            script.onload = initializeMap;
            document.head.appendChild(script);
        }
    }, []);

    return <div id="map" style={{ width: '100%', height: '400px' }} />;
};

export default MapComponent;
