import React from 'react';

function EmotionSummary({promptText}){
    if (!promptText) return <div className="emotion-summary"><p>Recommendation and Emotionsummary</p></div>;

    return (
        <div className="emotion-summary">
            {promptText.split('\n').map((line,idx)=>(
                <p key={idx}>{line}</p>
            ))}
        </div>
    );
}

export default EmotionSummary;