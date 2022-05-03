import React from 'react';

import DayTitles from './day-titles';
import DayWrapper from './days-wrapper';

export default function WeekWrapper(props) {
    console.log(props.monthData)
    const renderCalendarBox = () => {
        const calendarBoxArray = []

        for(let i=1; i <= props.monthData.start_day; i++) {
            const date = props.monthData.days_in_previous_month - props.monthData.start_day + i;
            calendarBoxArray.push(<DayWrapper key={`P-${i}`} date={date} overflow />)
        }

        for(let i=1; i <= props.monthData.days_in_month; i++) {
            calendarBoxArray.push(<DayWrapper key={`${props.monthData.id} - ${i}`} 
            date={i} month={props.monthData} />)
        }

        for(let i=1; i <= 42 - props.monthData.days_in_month - props.monthData.start_day; i++) {
            calendarBoxArray.push(<DayWrapper key={`N-${i}`} date={i} overflow />)
        }

        return calendarBoxArray
    }

    return(
        <div>
            <DayTitles />
            <div className="week-setup">
                {renderCalendarBox()}
            </div>
        </div>
    );
}