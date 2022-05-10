import React from 'react';

export default function Header() {
    return(
        (<div className="month-name">
            <div className="left-arrow" onClick={() => props.monthChange("previous")}><h2>&#9668;</h2></div>
            <div className="month"></div>
            <h1>{props.monthName}</h1>
            <div className="right-arrow" onClick={() => props.monthChanger("next")}><h2>&#9658;</h2></div>
        </div>)
    );
}