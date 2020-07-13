import React from 'react';
import {Modal} from 'react-bulma-components';
import './NoteButton.css';
import {fetchPost} from "../utils";

class NoteButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {modalOpen: false};

        this.handleNo = this.handleNo.bind(this);
        this.handleYes = this.handleYes.bind(this);
    }

    handleYes() {
        this.setState({modalOpen: false});
        fetchPost(this.props.urlSubmit, {action: this.props.action}).then(() => {
            window.location = this.props.urlRedirect;
        });
    }

    handleNo() {
        this.setState({modalOpen: false});
    }

    render() {
        let className = "button";
        if (this.props.buttonClass) {
            className += " " + this.props.buttonClass;
        }

        return (
            <span>
                <button className={className}
                        onClick={() => this.setState({modalOpen: true})}>{this.props.buttonText}</button>
                <Modal show={this.state.modalOpen} onClose={this.handleNo}>
                    <div className="modal-content box">
                        <p>Are you sure?</p>
                        <div className="NoteButton-Buttons">
                            <button className="button is-primary" onClick={this.handleYes}>Yes</button>
                            <button className="button" onClick={this.handleNo}>No</button>
                        </div>
                    </div>
                </Modal>
            </span>
        )
    }
}

export default NoteButton;