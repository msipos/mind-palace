import React from 'react';
import './NoteViewerEditButton.css';
import AreYouSureDialog from "./dialogs/AreYouSureDialog";

class NoteViewerEditButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {showMenu: false, clickedArchive: false, clickedDelete: false};

        this.handleOpen = this.handleOpen.bind(this);
        this.handleDialogNo = this.handleDialogNo.bind(this);
        this.handleDialogYes = this.handleDialogYes.bind(this);
    }

    handleOpen() {
        this.setState({
            showMenu: !this.state.showMenu
        });
    }

    async handleDialogYes() {
        if (this.state.clickedArchive) {
            let action = "archive";
            if (this.props.archived) {
                action = "unarchive";
            }
            await window.actions.submitNoteAction(action);
            window.location.reload(true);
        } else if (this.state.clickedDelete) {
            await window.actions.submitNoteAction("delete");
            window.actions.redirectToListCollection();
        }
    }

    handleDialogNo() {
        this.setState({
            showMenu: false,
            clickedArchive: false,
            clickedDelete: false
        });
    }

    render() {
        // Is menu active?
        let outerClassName = "dropdown is-right";
        if (this.state.showMenu) outerClassName += " is-active";

        // Modal dialog
        let modalDialog = null;
        if (this.state.clickedArchive || this.state.clickedDelete) {
            modalDialog = <AreYouSureDialog onYes={this.handleDialogYes} onNo={this.handleDialogNo}/>;
        }

        let archiveText = "Archive";
        if (this.props.archived) {
            archiveText = "Unarchive";
        }

        return (
            <div className={outerClassName}>
                {modalDialog}
                <div className="NoteViewerEditButton-Trigger dropdown-trigger buttons has-addons">
                    <button className="button" onClick={() => {window.actions.redirectToNoteEdit()}}>Edit</button>
                    <button className="button" onClick={this.handleOpen}>
                        <span className="icon is-small">
                            <i className="fas fa-angle-down" aria-hidden="true"/>
                        </span>
                    </button>
                </div>
                <div className="NoteViewerEditButton-Dropdown dropdown-menu" id="dropdown-menu" role="menu">
                    <div className="dropdown-content">
                        <a className="dropdown-item" onClick={() => {this.setState({clickedArchive: true}); }}>
                            {archiveText}
                        </a>
                        <a className="dropdown-item has-text-danger"
                           onClick={() => {this.setState({clickedDelete: true}); }}>
                            Delete
                        </a>
                    </div>
                </div>
            </div>
        );
    }
}

export default NoteViewerEditButton;