import React from 'react';
import AreYouSureDialog from "./dialogs/AreYouSureDialog";


class DeleteCollectionButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            modalOpen: false,
        }
        this.handleClick = this.handleClick.bind(this);
        this.handleNo = this.handleNo.bind(this);
        this.handleYes = this.handleYes.bind(this);
    }

    async handleYes() {
        this.setState({modalOpen: false});
        await window.collectionActions.submitCollectionAction("delete");
        window.collectionActions.redirectHome();
    }

    handleNo() { this.setState({modalOpen: false}); }

    handleClick() { this.setState({modalOpen: true}); }

    render() {
        let modal = null;
        if (this.state.modalOpen) modal =
                <AreYouSureDialog labelText="Are you sure? All notes in this collection will be deleted!"
                                  onYes={this.handleYes} onNo={this.handleNo}/>;
        return (
            <span>
                <button className="button is-danger" onClick={this.handleClick}>
                    <span className="icon"><i className="fas fa-book" /></span>
                    <span className="ml-2">Delete Collection</span>
                </button>
                {modal}
            </span>
        )
    }
}

export default DeleteCollectionButton;