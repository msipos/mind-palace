import React from 'react';
import {Modal} from 'react-bulma-components';


class InputDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            modalOpen: true,
            text: props.initialText || ""
        };

        this.handleCancel = this.handleCancel.bind(this);
        this.handleOk = this.handleOk.bind(this);
        this.handleTextChange = this.handleTextChange.bind(this);
    }

    handleOk() {
        this.setState({modalOpen: false});
        this.props.onOk(this.state.text);
    }

    handleCancel() {
        this.setState({modalOpen: false});
        this.props.onCancel();
    }

    handleTextChange(event) {
        this.setState({text: event.target.value})
    }

    render() {
        let description = null;
        if (this.props.labelText) {
            description = <p>{this.props.labelText}</p>;
        }

        return (
            <Modal show={this.state.modalOpen} onClose={this.handleCancel}>
                <div className="modal-content box">
                    {description}
                    <input type="text" value={this.state.text} onChange={this.handleTextChange} autoFocus={true}/>
                    <div className="NoteButton-Buttons">
                        <button className="button is-primary" onClick={this.handleOk}>Ok</button>
                        <button className="button" onClick={this.handleCancel}>Cancel</button>
                    </div>
                </div>
            </Modal>
        )
    }
}

export default InputDialog;