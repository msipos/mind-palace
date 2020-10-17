import React from 'react';
import './NoteButton.css';
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

    async handleOk(text) {
        this.setState({modalOpen: false});
        let response = await window.collectionActions.submitNewCollection(text);
        let data = await response.json();
        window.location = data['collection_url'];
    }

    handleCancel() { this.setState({modalOpen: false}); }

    handleClick() {
        this.setState({modalOpen: true});
    }

    render() {
        let modal = null;
        if (this.state.modalOpen) modal = <span><InputDialog labelText="Enter collection name:" onOk={this.handleOk}
                                                             onCancel={this.handleCancel}/></span>;
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