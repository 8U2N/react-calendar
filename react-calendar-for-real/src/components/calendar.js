import React, { Component } from 'react';

import Header from "./header";
import WeekWrapper from "./week-wrapper";
import Footer from "./footer";

export default class Calendar extends Component {
    constructor(props) {
        super(props);

        this.monthList = [
			"January",
			"February",
			"March",
			"April",
			"May",
			"June",
			"July",
			"August",
			"September",
			"October",
			"November",
			"December",
		];

        this.now = this.calculateDateData()

        this.state = {
            month: {},
            monthData: []
        };

        this.handleMonthChange = this.handleMonthChange.bind(this);

    }
    
    handleMonthChange(direction) {
        const currentMonthIndex = this.monthList.indexOf(this.state.month.name);
        const newMonthName = this.monthList[direction === "next" ? currentMonthIndex + 1 : currentMonthIndex -1];
        const newMonthData = this.state.monthData.filter(month => month.name === newMonthName)[0];
        this.setState({ month: newMonthData })
    }

    calculateDateData() {
        const now = new Date()
        const month = this.monthList[now.getMonth()]
        const year = now.getFullYear()
        return { month, year }
    }

    componentDidMount() {
        fetch('http://127.0.0.1:5000/month/get')
            .then(response => response.json())
            .then(data => 
                this.setState ({
                    monthData: data,
                    month: data.filter(month => 
                        month.name === this.now.month && 
                        month.year === this.now.year
                        )[0],
                })
            );
    }

    render() {
        return(
            <div className="calendar-container">
                <h3>REACTive Calendar coded by 8U2N</h3>
                <div className="header-wrapper">
                    <h2>&#127783;</h2><Header monthName={this.state.month.name} monthChanger={this.handleMonthChange} /><h2>&#127783;</h2>
                </div>
                <div className="week-wrapper">
                    <WeekWrapper monthData={this.state.month} />
                </div>
                <div className="footer-wrapper">
                    <Footer currentYear={this.state.month.year} />
                </div>
            </div>
        );
    };
}