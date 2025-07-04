import React from 'react';

function FeelControl() {
    return (
        <div className="feel-control">
            <h3>How do you want to feel?</h3>
            <div className="feel-buttons">
                <button className="express-btn" onClick={()=>setFeelMode('express')}>Express</button>
                <button className="calmdown-btn" onClick={()=>setFeelMode('calmdown')}>Calm down</button>
            </div>
        </div>
    );
}

export default FeelControl;