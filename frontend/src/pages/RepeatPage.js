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
        this.handleEdit = this.handleEdit.bind(this);
        setTimeout(() => this.getRepeats(), 0);
    }

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
        });
    }

    handleChoice(choice) {
        fetchPost(this.props.urlRepeat, {
            note_id: this.state.activeNote.note_id,
            choice: choice
        }).then(() => {
            this.getRepeats();
        })
    }

    handleEdit() {
        window.location = this.props.urlEditPrefix + this.state.activeNote.note_id + this.props.urlEditPostfix;
    }

    render() {
        if (this.state.condition === 'loading') {
            return <div>Loading...</div>;
        }

        if (this.state.numActiveNotes === 0) {
            return <div>All done!</div>
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
        const label = this.state.numActiveNotes + " active notes."
        const repeater = <Repeater label={label} choices={choices} onChoice={this.handleChoice}
                                   onEdit={this.handleEdit}/>;

        return <div>
            <div>{repeater}</div>
            <div className="RepeatPage-Note">{note_viewer}</div>
        </div>;
    }
}

export default RepeatPage;