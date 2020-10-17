import React from 'react';
import {Modal} from 'react-bulma-components';

class AreYouSureDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {modalOpen: true};

        this.handleNo = this.handleNo.bind(this);
        this.handleYes = this.handleYes.bind(this);
    }

    handleYes() {
        this.setState({modalOpen: false});
        this.props.onYes();
    }

    handleNo() {
        this.setState({modalOpen: false});
        this.props.onNo();
    }

    render() {
        let description = "Are you sure?";
        if (this.props.labelText) {
            description = this.props.labelText;
        }
        
        return (
            <Modal show={this.state.modalOpen} onClose={this.handleNo}>
                <div className="modal-content box">
                    <p>{description}</p>
                    <div className="NoteButton-Buttons">
                        <button className="button is-primary" onClick={this.handleYes}>Yes</button>
                        <button className="button" onClick={this.handleNo}>No</button>
                    </div>
                </div>
            </Modal>
        )
    }
}

export default AreYouSureDialog;