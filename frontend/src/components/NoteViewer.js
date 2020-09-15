import ejs from 'ejs/ejs.min';
import React from 'react';
import marked from 'marked';
import DOMPurify from 'dompurify';
import './NoteViewer.css';
import {cloneObject} from "../utils";

function _formatTime(t) {
    const d = new Date(t * 1000);
    return d.toLocaleString();
}

class NoteViewer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {revealed: []};

        this.handleReveal = this.handleReveal.bind(this);
    }

    handleReveal(idx) {
        let arr = cloneObject(this.state.revealed);
        if (arr.indexOf(idx) === -1) {
            arr.push(idx);
        }
        this.setState({
            revealed: arr
        })
    }

    _createHandler(i) {
        return () => this.handleReveal(i)
    }

    render() {
        let sections = [];
        let i = 0;
        for (const section of this.props.note.contents.sections) {
            let className = "box NoteViewer-Section";
            let appearHidden = false;
            if (section.hidden) {
                if (this.state.revealed.indexOf(i) === -1) {
                    className += " NoteViewer-Blur";
                    appearHidden = true;
                }
            }

            // EJS
            let text = section.text;
            if (text.indexOf("<%=")) {
                text = ejs.render(text, {time: new Date()});
            }

            // Markdown -> HTML, check for security too
            let html = marked(text);
            html = DOMPurify.sanitize(html);

            // Click handler
            let handleClick = null;
            if (appearHidden) {
                handleClick = this._createHandler(i);
            }

            sections.push(<div dangerouslySetInnerHTML={{__html: html}} className={className} key={i}
                               onClick={handleClick}/>);
            i += 1;
        }

        const note = this.props.note;

        // Assemble description
        let description = "Repeats ";
        if (note.repeat_policy.type === "none") {
            description += " <b>never.</b> ";
        } else if (note.repeat_policy.type === "hourly") {
            description += " <b>every " + note.repeat_policy.hours + " hour(s).</b> ";
        } else if (note.repeat_policy.type === "daily") {
            description += " <b>every " + note.repeat_policy.days
                + " day(s) in the " + note.repeat_policy.timeOfDay + ".</b> ";
        }
        if (note.learn_policy.type === "none") {
            description += "No learning policy."
        } else if (note.learn_policy.type === "exponential") {
            description += "Exponential learning policy."
        }

        // Note title
        let noteTitle = this.props.note.name.trim();
        if (noteTitle === "") {
            noteTitle = "Untitled";
        }

        return (
            <div>
                <h1 className="title NoteViewer-Title">{noteTitle}</h1>
                {sections}
                <div className="box NoteViewer-Section">
                    <p dangerouslySetInnerHTML={{__html: description}}/>
                    <p>Created: <b>{_formatTime(note.created_time)}</b></p>
                    <p>Last updated: <b>{_formatTime(note.updated_time)}</b></p>
                </div>
            </div>
        )
    }
}

export default NoteViewer;