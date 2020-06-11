import React, {Component} from 'react';
import propTypes from "prop-types";
import NoteLearningMetadataEditor from "./NoteLearningMetadataEditor";
import NoteRepeatMetadataEditor from "./NoteRepeatMetadataEditor";
import NoteMarkdownSectionEditor from "./NoteMarkdownSectionEditor";
import './NoteEditor.css';
import {cloneObject} from "../../utils";

class NoteEditor extends Component {
    constructor(props) {
        super(props);

        // We slightly change the shape of the note because we must keep additional state while React is running.
        this.state = {
            name: props.initialNote.name,
            contents: {
                lock: props.initialNote.contents.lock || false,
                sections: [],
            },
            repeating: this.repeatingMetadataToDense(props.initialNote.repeat_policy),
            learning: cloneObject(props.initialNote.learn_policy)
        };

        // Keep track of sections using index.
        let i = 0;
        for (const section of props.initialNote.contents.sections) {
            const clonedSection = cloneObject(section);
            clonedSection.index = i;
            this.state.contents.sections.push(clonedSection);
            i += 1
        }

        this.handleSectionChange = this.handleSectionChange.bind(this);
        this.handleSectionDelete = this.handleSectionDelete.bind(this);
        this.handleClickNewMarkdown = this.handleClickNewMarkdown.bind(this);
        this.handleRepeatingChange = this.handleRepeatingChange.bind(this);
        this.handleLearningChange = this.handleLearningChange.bind(this);
        this.handleChangeName = this.handleChangeName.bind(this);
        this.handleClickSave = this.handleClickSave.bind(this);
        this.handleClickCancel = this.handleClickCancel.bind(this);
    }

    repeatingMetadataToDense(repeating) {
        // Makes sure the metadata.repeating is "dense" because of React state.
        let dense = cloneObject(repeating);
        if (!dense.hours) {
            dense.hours = 24;
        }
        if (!dense.days) {
            dense.days = 1;
        }
        if (!dense.timeOfDay) {
            dense.timeOfDay = 'morning';
        }
        return dense;
    }

    handleRepeatingChange(newRepeating) {
        this.setState({repeating: newRepeating});
    }

    handleLearningChange(newLearning) {
        this.setState({learning: newLearning});
    }

    handleChangeName(event) {
        this.setState({name: event.target.value});
    }

    findSectionIndex(index) {
        const contents = this.state.contents;
        for (let i = 0; i < contents.sections.length; i++) {
            const section = contents.sections[i];
            if (section.index === index) {
                return i;
            }
        }
    }

    handleSectionDelete(index) {
        const contents = cloneObject(this.state.contents);
        const i = this.findSectionIndex(index);
        contents.sections.splice(i, 1);
        this.setState({contents: contents});
    }

    handleSectionChange(newSection) {
        const contents = cloneObject(this.state.contents);
        const i = this.findSectionIndex(newSection.index);
        contents.sections[i] = newSection;
        this.setState({contents: contents});
    }

    handleClickNewMarkdown() {
        const contents = cloneObject(this.state.contents);
        let i = 0; // Calculate index
        if (contents.sections.length > 0) {
            i = contents.sections[contents.sections.length - 1].index + 1;
        }
        contents.sections.push({
            "type": "markdown",
            "text": "",
            "hidden": true,
            "index": i,
        });
        this.setState({contents: contents});
    }

    handleClickSave() {
        const note = {
            name: this.state.name,
            contents: this.state.contents,
            repeat_policy: {},
            learn_policy: this.state.learning
        }

        // Repeating needs special work
        note.repeat_policy.type = this.state.repeating.type;
        if (this.state.repeating.type === "hourly") {
            note.repeat_policy.hours = this.state.repeating.hours;
        } else if (this.state.repeating.type === "daily") {
            note.repeat_policy.days = this.state.repeating.days;
            note.repeat_policy.timeOfDay = this.state.repeating.timeOfDay;
        }

        this.props.onSave(note);
    }

    handleClickCancel() {
        this.props.onCancel();
    }

    render() {
        // Section editors
        const editors = [];
        for (const section of this.state.contents.sections) {
            editors.push(<NoteMarkdownSectionEditor index={section.index} text={section.text}
                                                    hidden={section.hidden} onChange={this.handleSectionChange}
                                                    onDelete={this.handleSectionDelete}
                                                    key={section.index}/>);
        }

        return (
            <div className="NoteEditor">
                <div className="columns">
                    <div className="column is-narrow">
                        <div className="NoteEditor-Padded">
                            <button className="button NoteEditor-Save is-primary"
                                    onClick={this.handleClickSave}>Save
                            </button>
                            <button className="button" onClick={this.handleClickCancel}>Cancel</button>
                        </div>
                    </div>
                </div>
                <div className="columns">
                    <div className="column">
                        <div className="NoteEditor-Padded">
                            <label>
                                Name
                                <input className="input" type="text" name="name" value={this.state.name}
                                       onChange={this.handleChangeName}/>
                            </label>

                        </div>
                    </div>
                </div>
                <div className="columns">
                    <div className="column">
                        {editors}
                    </div>
                </div>
                <div className="columns is-centered">
                    <div className="column is-narrow NoteEditor-ButtonBar">
                        <button className="button" onClick={this.handleClickNewMarkdown}>New Markdown</button>
                    </div>
                </div>
                <div className="columns">
                    <div className="column">
                        <NoteRepeatMetadataEditor repeating={this.state.repeating}
                                                  onChange={this.handleRepeatingChange}/>
                    </div>
                    <div className="column">
                        <NoteLearningMetadataEditor learning={this.state.learning}
                                                    onChange={this.handleLearningChange}/>
                    </div>
                </div>
            </div>
        );
    }
}

NoteEditor.propTypes = {
    initialNote: propTypes.object,
    onSave: propTypes.func,
    onCancel: propTypes.func
};

export default NoteEditor;