import ReactDOM from "react-dom";
import React from "react";
import NoteViewer from "../components/NoteViewer";

let note = {
    "name": "title goes here",
    "contents": {
        "objects": [
            {
                "type": "markdown",
                "contents": "Hello world...\n\nHow are you? I am **good**.",
                "hidden": false
            }
        ]
    },
    "metadata": {
        "repeating": {
            "type": "none"
        },
        "learning": {
            "type": "none"
        }
    }
};
ReactDOM.render(
    <NoteViewer note={note}/>,
    document.getElementById('app')
);