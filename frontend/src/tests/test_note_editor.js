import ReactDOM from "react-dom";
import React from "react";
import NoteEditor from "../components/note_editor/NoteEditor";

let note = {
    "name": "title goes here",
    "contents": {
        "objects": [
            {
                "type": "markdown",
                "contents": "...",
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

function onSave(note) {
    console.log(note);
}

function onCancel() {
    console.log('canceled')
}

ReactDOM.render(
    <NoteEditor initialNote={note} onSave={onSave} onCancel={onCancel}/>,
    document.getElementById('app')
);