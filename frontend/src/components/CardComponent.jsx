import React, {useState} from 'react';

function CardExpiration() {
  const [startDate, setStartDate] = useState('');
  const [expiryDate, setExpiryDate] = useState('');
  const [daysRemaining, setDaysRemaining] = useState(null);

  // 날짜 계산 함수
  const calculateExpiryDate = (date) => {
    const start = new Date(date);
    const expiry = new Date(start);
    expiry.setDate(start.getDate() + 30); // 30일 추가
    return expiry.toISOString().split('T')[0]; // YYYY-MM-DD 포맷
  };

  const calculateDaysRemaining = (expiryDate) => {
    const today = new Date();
    const expiry = new Date(expiryDate);
    const difference = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24)); // 밀리초를 일 단위로 변환
    return difference;
  };

  const handleStartDateChange = (e) => {
    const inputDate = e.target.value;
    setStartDate(inputDate);

    if (inputDate) {
      const calculatedExpiryDate = calculateExpiryDate(inputDate);
      setExpiryDate(calculatedExpiryDate);

      const daysLeft = calculateDaysRemaining(calculatedExpiryDate);
      setDaysRemaining(daysLeft);
    } else {
      setExpiryDate('');
      setDaysRemaining(null);
    }
  };

  return (
      <div style={{padding: '20px', fontFamily: 'Arial, sans-serif'}}>
        <h2>교통카드 만료일 계산기</h2>
        <label htmlFor="start-date">사용 개시일:</label>
        <input
            type="date"
            id="start-date"
            value={startDate}
            onChange={handleStartDateChange}
            style={{margin: '10px', padding: '5px'}}
        />
        {expiryDate && (
            <div>
              <p>교통카드 만료일: <strong>{expiryDate}</strong></p>
              <p>
                만료일까지 남은 일수:{" "}
                <strong>
                  {daysRemaining > 0
                      ? `${daysRemaining}일 남았습니다.`
                      : daysRemaining === 0
                          ? "오늘 만료됩니다!"
                          : "만료되었습니다."}
                </strong>
              </p>
            </div>
        )}
      </div>
  );
}

export default CardExpiration;
