import React from 'react';
import NoteViewer from "../components/NoteViewer";
import Repeater from "../components/Repeater";
import './RepeatPage.css';
import {fetchPost} from "../utils";

// import {fetchPost} from "../utils";

class RepeatPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            condition: 'loading'
        }

        this.handleChoice = this.handleChoice.bind(this);
        setTimeout(() => this.getRepeats(), 0);
    }

    // TODO: Rewrite as async
    getRepeats() {
        this.setState({condition: 'loading'});
        fetch(this.props.urlRepeat).then((response) => {
            return response.json()
        }).then((data) => {
            this.setState({
                condition: 'loaded',
                choices: data.choices,
                activeNote: data.active_note,
                numActiveNotes: data.num_active_notes
            })
            window.actions.urlListCollection = data.urls.url_list_collection;
            window.actions.urlNoteAction = data.urls.url_note_action;
            window.actions.urlNoteEdit = data.urls.url_note_edit;
        });
    }

    // TODO: Rewrite as async
    handleChoice(choice) {
        fetchPost(this.props.urlRepeat, {
            note_id: this.state.activeNote.note_id,
            choice: choice
        }).then(() => {
            this.getRepeats();
        })
    }

    render() {
        if (this.state.condition === 'loading') {
            return <Repeater label="Loading..." />;
        }

        if (this.state.numActiveNotes === 0) {
            return <Repeater label="All done!" />;
        }

        const note_viewer = <NoteViewer note={this.state.activeNote}/>;
        const choices = [];
        for (const choice of this.state.choices) {
            choices.push({
                key: choice.choice_index,
                htmlText: choice.choice_html,
                payload: choice
            });
        }
        const label = this.state.numActiveNotes + " active notes.  Click to learn them."
        const repeater = <Repeater label={label} choices={choices} onChoice={this.handleChoice}/>;

        return <div>
            <div>{repeater}</div>
            <div className="RepeatPage-Note">{note_viewer}</div>
        </div>;
    }
}

export default RepeatPage;