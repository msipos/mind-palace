import React from 'react';
import NoteEditor from "../components/note_editor/NoteEditor";
import {fetchPost} from "../utils";

class NewEditNotePage extends React.Component {
    constructor(props) {
        super(props);

        this.handleSave = this.handleSave.bind(this);
        this.handleCancel = this.handleCancel.bind(this);
    }

    handleSave(note) {
        fetchPost(this.props.urlSave, note).then((response) => {
            if (response.status >= 200 && response.status < 300) {
                window.location = this.props.urlSuccessRedirect;
            } else {
                console.error(response);
            }
        });
    }

    handleCancel() {
        window.location = this.props.urlCancel;
    }

    render() {
        return <NoteEditor initialNote={this.props.initialNote} onSave={this.handleSave} onCancel={this.handleCancel}/>;
    }
}

export default NewEditNotePage;