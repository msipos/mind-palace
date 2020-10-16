import React from 'react';
import './NoteButton.css';
import {fetchPost} from "../utils";
import InputDialog from "./dialogs/InputDialog";

class NewCollectionButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            modalOpen: false,
        }
        this.handleClick = this.handleClick.bind(this);
        this.handleCancel = this.handleCancel.bind(this);
        this.handleOk = this.handleOk.bind(this);
    }

    handleOk(text) {
        this.setState({modalOpen: false});
        console.log(text);
    }

    handleCancel() { this.setState({modalOpen: false}); }

    handleClick() {
        this.setState({modalOpen: true});
        // fetchPost(this.props.urlSubmit, {action: this.props.action}).then(() => {
        //     window.location = this.props.urlRedirect;
        // });
        console.log("Hi!");
    }

    render() {
        let modal = null;
        if (this.state.modalOpen) modal = <span><InputDialog labelText="Enter collection name:" onOk={this.handleOk}
                                                             onCancel={this.handleCancel}/></span>;
        console.log(modal);
        return (
            <span>
                <button className="button is-primary" onClick={this.handleClick}>
                    <span className="icon"><i className="fas fa-book" /></span>
                    <span className="ml-2">New Collection</span>
                </button>
                {modal}
            </span>
        )
    }
}

export default NewCollectionButton;