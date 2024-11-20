import React, { useState } from 'react';

function TransitCardExpiration() {
  const [startDate, setStartDate] = useState('');
  const [expiryDate, setExpiryDate] = useState('');
  const [daysRemaining, setDaysRemaining] = useState(null);

  const calculateExpiryDate = (date) => {
    const start = new Date(date);
    const expiry = new Date(start);
    expiry.setDate(start.getDate() + 30);
    return expiry.toISOString().split('T')[0];
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
    <div style={{ padding: '20px' }}>
      <h2>기후동행카드 만료일 계산기</h2>
      <label htmlFor="start-date">사용 개시일:</label>
      <input
        type="date"
        id="start-date"
        value={startDate}
        onChange={handleStartDateChange}
        style={{ margin: '10px', padding: '5px' }}
      />
      {expiryDate && (
        <div>
          <p>기후동행카드 만료일: {expiryDate}</p>
          <p>
            만료일까지{` ${daysRemaining}일 남았습니다.`}
          </p>
        </div>
      )}
    </div>
  );
}

export default TransitCardExpiration;
