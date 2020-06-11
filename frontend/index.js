import React from 'react';
import ReactDOM from "react-dom";
import NoteButton from "./src/components/NoteButton";
import NoteViewer from "./src/components/NoteViewer";
import Repeater from "./src/components/Repeater";
import NoteEditor from "./src/components/note_editor/NoteEditor";
import NewEditNotePage from "./src/pages/NewEditNotePage";
import RepeatPage from "./src/pages/RepeatPage";
import './src/site.js';
import 'bulma/css/bulma.css';
import './src/site.css';

window.mpReact = {
    components: {
        NoteButton: NoteButton,
        NoteViewer: NoteViewer,
        Repeater: Repeater,
        NoteEditor: NoteEditor
    },
    pages: {
        NewEditNotePage: NewEditNotePage,
        RepeatPage: RepeatPage
    },
    mount: function (component, props, htmlId) {
        ReactDOM.render(
            React.createElement(component, props),
            document.getElementById(htmlId),
        )
    }
};

