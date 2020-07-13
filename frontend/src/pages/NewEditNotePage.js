import React from 'react';
import NoteEditor from "../components/note_editor/NoteEditor";
import {fetchPost} from "../utils";

class NewEditNotePage extends React.Component {
    constructor(props) {
        super(props);

        this.handleSave = this.handleSave.bind(this);
        this.handleCancel = this.handleCancel.bind(this);
    }

    async handleSave(note) {
        let response = await fetchPost(this.props.urlSave, note);
        if (response.status >= 200 && response.status < 300) {
            if (this.props.isNew) {
                let contents = await response.json();
                window.location = contents.note_url;
            } else {
                window.location = this.props.urlSuccessRedirect;
            }
        } else {
            console.error(response);
        }
    }

    handleCancel() {
        window.location = this.props.urlCancel;
    }

    render() {
        return <NoteEditor initialNote={this.props.initialNote} onSave={this.handleSave} onCancel={this.handleCancel}
                           isNew={this.props.isNew} urlDelete={this.props.urlDelete}
                           urlDeleteRedirect={this.props.urlDeleteRedirect}/>;
    }
}

export default NewEditNotePage;