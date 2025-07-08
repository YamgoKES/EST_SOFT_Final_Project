import React from 'react';
import best from '../assets/best.png';
import best2 from '../assets/best2.png';
import best3 from '../assets/best3.png';
import best4 from '../assets/best4.png';
import best5 from '../assets/best5.png';

const iconList = [ best, best2, best3, best4, best5]

function Recommendation({ items }) {
  return (
    <div className="recommand">
      <h3>You might like</h3>

      <div className="items">
        {items && items.length > 0 ? (
          items.map((item, idx) => (
            <div className="item-card" key={idx}>
              <img src={iconList[idx % iconList.length]} alt="icon" className="recommend-icon" />
              <p title={item.title} className="product-title">{item.title}</p>
              <a href={item.link} target="_blank" rel="noopener noreferrer" className="shop-now-link">
                Shop Now
              </a>
            </div>
          ))
        ) : (
          <p
              style={{
                marginLeft: '30px',
                color: '#333',
                fontWeight: 'bold',     // 글자 굵게
                textAlign: 'center',    // 텍스트 가운데 정렬
              }}
          >
              분석을 완료하면 여기에 추천 항목이 나타납니다.
          </p>
        )}
      </div>
    </div>
  );
}

export default Recommendation;