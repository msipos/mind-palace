import ReactDOM from "react-dom";
import React from "react";
import Repeater from "../components/Repeater";

let choices = [
    {
        htmlText: '<span>Repeat in <b>12</b> days</span>',
        payload: 12
    },
    {
        htmlText: '<span>Repeat in <b>24</b> days</span>',
        payload: 24
    },
    {
        htmlText: '<span>Repeat in <b>36</b> days</span>',
        payload: 36
    },
    {
        htmlText: '<span>Repeat in <b>48</b> days</span>',
        payload: 48
    },
];

function handleChoice(choice) {
    console.log(choice);
}

ReactDOM.render(
    <Repeater choices={choices} onChoice={handleChoice}/>,
    document.getElementById('app')
);