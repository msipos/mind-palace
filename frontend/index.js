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
import NoteActions from "./src/components/NoteActions";
import NewCollectionButton from "./src/components/NewCollectionButton";
import CollectionActions from "./src/components/CollectionActions";
import DeleteCollectionButton from "./src/components/DeleteCollectionButton";

// Various React components and pages
window.mpReact = {
    components: {
        NoteButton: NoteButton,
        NoteViewer: NoteViewer,
        Repeater: Repeater,
        NoteEditor: NoteEditor,
        NewCollectionButton: NewCollectionButton,
        DeleteCollectionButton: DeleteCollectionButton
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
    },
};

// Global variable that is used to send information to the backend, populated in the specific HTML pages.
window.actions = new NoteActions();
window.collectionActions = new CollectionActions();
