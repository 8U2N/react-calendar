import React from 'react';

export default function Header(props) {
    return(
        <div>
            <h1>{props.monthName}</h1>
        </div>
    );
}