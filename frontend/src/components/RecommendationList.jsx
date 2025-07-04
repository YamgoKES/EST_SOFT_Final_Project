import React from 'react';

function Recommendation(){
  
  return(
    <> 
      <div className="recommand">
      <h3>You might like</h3>

      <div className="items">
        {[...Array(5)].map((_, index) => (
          <div className="item-card" key={index}>
            <img src="이미지경로" alt="non-image" />
            <p>상품명</p>
            <span>shop now</span>
          </div>
        ))}
      </div>
    </div>
  </> 
    );
}

export default Recommendation;