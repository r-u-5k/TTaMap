function displayRoute(routeData, map) {
  if (!routeData || !routeData.steps) {
    console.error("Invalid route data:", routeData);
    alert("경로 데이터가 올바르지 않습니다.");
    return;
  }

  const steps = routeData.steps;

  steps.forEach((step, index) => {
    console.log(`Step ${index + 1}:`, step);

    // 경로 색상 및 스타일 설정
    let color;
    let content;
    switch (step.mode) {
      case "walk":
        color = "blue"; // 도보 경로는 파란색
        content = `<div style="color: blue;">도보 경로<br>거리: ${step.distance}m<br>시간: ${step.time}초</div>`;
        break;
      case "bike":
        color = "green"; // 자전거 경로는 초록색
        content = `<div style="color: green;">자전거 경로<br>출발: ${step.startBikeStation}<br>도착: ${step.endBikeStation}<br>거리: ${step.distance}m<br>시간: ${step.time}초</div>`;
        break;
      case "transit":
        color = "red"; // 대중교통 경로는 빨간색
        content = `<div style="color: red;">대중교통 경로<br>거리: ${step.distance}m<br>시간: ${step.time}초</div>`;
        break;
      default:
        color = "gray"; // 기본 색상
        content = `<div style="color: gray;">알 수 없는 경로</div>`;
    }

    // 경로를 지도에 표시
    if (step.mode === "bike" || step.mode === "walk") {
      const polylinePath = [
        new kakao.maps.LatLng(routeData.startLat, routeData.startLng),
        new kakao.maps.LatLng(routeData.endLat, routeData.endLng),
      ];

      const polyline = new kakao.maps.Polyline({
        map: map,
        path: polylinePath,
        strokeWeight: 5,
        strokeColor: color,
        strokeOpacity: 0.7,
        strokeStyle: "solid",
      });

      // 경로 위에 정보 창 추가
      const midIndex = Math.floor(polylinePath.length / 2);
      const midPoint = polylinePath[midIndex];
      const infowindow = new kakao.maps.InfoWindow({
        position: midPoint,
        content: content,
      });

      kakao.maps.event.addListener(polyline, "mouseover", () => {
        infowindow.open(map, midPoint);
      });

      kakao.maps.event.addListener(polyline, "mouseout", () => {
        infowindow.close();
      });
    }
  });
}
