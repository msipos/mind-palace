import React, {Component} from 'react';
import propTypes from "prop-types";
import './NoteMarkdownSectionEditor.css';

class NoteMarkdownSectionEditor extends Component {
    constructor(props) {
        super(props);

        this.onHiddenChange = this.onHiddenChange.bind(this);
        this.onTextChange = this.onTextChange.bind(this);
        this.onClickDelete = this.onClickDelete.bind(this);
    }

    onHiddenChange(event) {
        this.props.onChange({
            index: this.props.index,
            type: "markdown",
            text: this.props.text,
            hidden: event.target.checked
        });
    }

    onTextChange(event) {
        this.props.onChange({
            index: this.props.index,
            type: "markdown",
            text: event.target.value,
            hidden: this.props.hidden
        });
    }

    onClickDelete() {
        this.props.onDelete(this.props.index);
    }

    render() {
        return (
            <div className="NoteMarkdownSectionEditor">
                <div className="NoteMarkdownSectionEditor-Header is-clearfix">
                    <span className="is-pulled-left">Markdown Section</span>
                    <span className="is-pulled-right">
                        <label>
                          <input
                              type="checkbox"
                              value="hidden"
                              checked={this.props.hidden}
                              onChange={this.onHiddenChange}
                          />
                            Hidden
                        </label>
                        <a className="NoteMarkdownSectionEditor-Delete delete" onClick={this.onClickDelete}/>
                    </span>
                </div>
                <textarea className="textarea" rows={10} value={this.props.text} onChange={this.onTextChange}/>
            </div>
        );
    }
}

NoteMarkdownSectionEditor.propTypes = {
    index: propTypes.number,
    text: propTypes.string,
    hidden: propTypes.bool,
    onChange: propTypes.func,
    onDelete: propTypes.func
};

export default NoteMarkdownSectionEditor;