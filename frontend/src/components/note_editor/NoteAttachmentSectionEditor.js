import React, {Component} from 'react';
import propTypes from "prop-types";
import './NoteAttachmentSectionEditor.css';
import Dropzone from 'react-dropzone';
import {fetchPostFile} from "../../utils";

class NoteAttachmentSectionEditor extends Component {
    constructor(props) {
        super(props);

        this.onHiddenChange = this.onHiddenChange.bind(this);
        this.onClickDelete = this.onClickDelete.bind(this);
    }

    onHiddenChange(event) {
        this.props.onChange({
            index: this.props.index,
            type: "attachment",
            hidden: event.target.checked
        });
    }

    onClickDelete() {
        this.props.onDelete(this.props.index);
    }

    async upload(acceptedFiles) {
        console.log(acceptedFiles);
        await fetchPostFile('/foo/bar', acceptedFiles[0]);
    }

    render() {
        return (
            <div className="NoteAttachmentSectionEditor">
                <div className="NoteMarkdownSectionEditor-Header is-clearfix">
                    <span className="is-pulled-left">Attachment Section</span>
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
                <Dropzone onDrop={acceptedFiles => this.upload(acceptedFiles)}>
                  {({getRootProps, getInputProps}) => (
                    <section>
                      <div {...getRootProps()}>
                        <input {...getInputProps()} />
                        <p className="NoteAttachmentSectionEditor-Uploader">Drag'n'drop some files here, or click to select files</p>
                      </div>
                    </section>
                  )}
                </Dropzone>
            </div>
        );
    }
}

NoteAttachmentSectionEditor.propTypes = {
    index: propTypes.number,
    hidden: propTypes.bool,
    onChange: propTypes.func,
    onDelete: propTypes.func
};

export default NoteAttachmentSectionEditor;