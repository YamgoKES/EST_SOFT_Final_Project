import React from 'react';

function ResultBox({result}) {
    return (
        <div className="results">
            <h3>Results</h3>
            {result ? (
                <>
                <p className="info-line">
                    <strong>Age :</strong>
                    <span>{result.age}</span>
                </p>
                <p className='info-line'>
                    <strong>Gender :</strong>
                    <span>{result.gender}</span>
                </p>
                <p className='info-line'>
                    <strong>Emotion :</strong>
                    <span>{result.emotion}</span>
                </p>
                </>
            ) : (
                <p>분석결과가 없습니다.</p>
            )}
        </div>
    );
}

export default ResultBox;

