import React, {Component} from 'react';
import propTypes from "prop-types";
import './NoteLearningMetadataEditor.css';

let RADIO_NAME = 'NoteRepeatLearningRadio';
let NO_LEARNING = 'none';
let EXPONENTIAL_LEARNING = 'exponential';

class NoteLearningMetadataEditor extends Component {
    constructor(props) {
        super(props);

        this.handleInputChange = this.handleInputChange.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;

        if (target.value === NO_LEARNING) {
            this.props.onChange({"type": NO_LEARNING})
        } else if (target.value === EXPONENTIAL_LEARNING) {
            this.props.onChange({"type": EXPONENTIAL_LEARNING})
        }
    }

    render() {
        // Selected type
        const selected = this.props.learning.type;

        return (
            <div className="NoteLearningMetadataEditor">
                <div>Learning</div>
                <div>
                    <label>
                        <input type="radio"
                               name={RADIO_NAME}
                               value={NO_LEARNING}
                               checked={selected === NO_LEARNING}
                               onChange={this.handleInputChange}/>
                        Do not change repeat policy.
                    </label>
                </div>
                <div>
                    <label>
                        <input type="radio"
                               name={RADIO_NAME}
                               value={EXPONENTIAL_LEARNING}
                               checked={selected === EXPONENTIAL_LEARNING}
                               onChange={this.handleInputChange}
                        />
                        Exponential.
                    </label>
                </div>
            </div>
        );
    }
}


NoteLearningMetadataEditor.propTypes = {
    onChange: propTypes.func,
    learning: propTypes.object
};

export default NoteLearningMetadataEditor;