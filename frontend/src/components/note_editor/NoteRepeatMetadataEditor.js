import React, {Component} from 'react';
import propTypes from "prop-types";
import './NoteRepeatMetadataEditor.css';

let RADIO_NAME = 'NoteRepeatMetadataRadio';
let NO_REPEATING = 'none';
let HOURLY_REPEATING = 'hourly';
let DAILY_REPEATING = 'daily';

const ME_RADIO_NAME = 'NoteRepeatMetadataMERadio';
const ME_MORNING = 'morning';
const ME_EVENING = 'evening';

class NoteRepeatMetadataEditor extends Component {
    constructor(props) {
        super(props);

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleMeInputChange = this.handleMeInputChange.bind(this);
        this.handleHoursInputChange = this.handleHoursInputChange.bind(this);
        this.handleDaysInputChange = this.handleDaysInputChange.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;
        const newRepeating = this.props.repeating;
        if (target.value === NO_REPEATING) {
            newRepeating.type = NO_REPEATING;
        } else if (target.value === HOURLY_REPEATING) {
            newRepeating.type = HOURLY_REPEATING;
        } else if (target.value === DAILY_REPEATING) {
            newRepeating.type = DAILY_REPEATING;
        }
        this.props.onChange(newRepeating);
    }

    handleMeInputChange(event) {
        const target = event.target;
        const newRepeating = this.props.repeating;
        if (target.value === ME_MORNING) {
            newRepeating.timeOfDay = ME_MORNING;
        } else if (target.value === ME_EVENING) {
            newRepeating.timeOfDay = ME_EVENING;
        }
        this.props.onChange(newRepeating);
    }

    handleHoursInputChange(event) {
        const newRepeating = this.props.repeating;
        try {
            newRepeating.hours = parseInt(event.target.value, 10);
            this.props.onChange(newRepeating);
        } catch {
            // Nothing here
        }
    }

    handleDaysInputChange(event) {
        const newRepeating = this.props.repeating;
        try {
            newRepeating.days = parseInt(event.target.value, 10);
            this.props.onChange(newRepeating);
        } catch {
            // Nothing here
        }
    }

    render() {
        // Selected type
        const repeating = this.props.repeating;
        const selected = repeating.type;

        // Hours input
        const is_hours_disabled = (selected !== HOURLY_REPEATING);
        const hours_input = <input value={String(repeating.hours)}
                                   disabled={is_hours_disabled}
                                   type="number" onChange={this.handleHoursInputChange}/>;

        // Days input
        const is_days_disabled = (selected !== DAILY_REPEATING);
        const days_input = <input value={String(repeating.days)}
                                  disabled={is_days_disabled}
                                  type="number" onChange={this.handleDaysInputChange}/>;

        const meSelected = repeating.timeOfDay;

        return (
            <div className="NoteRepeatMetadataEditor">
                <div>Repeating</div>
                <div>
                    <label>
                        <input type="radio"
                               name={RADIO_NAME}
                               value={NO_REPEATING}
                               checked={selected === NO_REPEATING}
                               onChange={this.handleInputChange}/>
                        Do not repeat
                    </label>
                </div>
                <div>
                    <label>
                        <input type="radio"
                               name={RADIO_NAME}
                               value={HOURLY_REPEATING}
                               checked={selected === HOURLY_REPEATING}
                               onChange={this.handleInputChange}
                        />
                        Repeat every {hours_input} hour(s)
                    </label>
                </div>
                <div>
                    <label>
                        <input type="radio"
                               name={RADIO_NAME}
                               value={DAILY_REPEATING}
                               checked={selected === DAILY_REPEATING}
                               onChange={this.handleInputChange}
                        />
                        Repeat every {days_input} day(s)
                    </label>
                </div>
                <div className="NoteRepeatMetadataEditor-Nested">
                    <label>
                        <input type="radio"
                               name={ME_RADIO_NAME}
                               value={ME_MORNING}
                               checked={meSelected === ME_MORNING}
                               onChange={this.handleMeInputChange}
                               disabled={selected !== DAILY_REPEATING}
                        />
                        in the morning
                    </label>
                </div>
                <div className="NoteRepeatMetadataEditor-Nested">
                    <label>
                        <input type="radio"
                               name={ME_RADIO_NAME}
                               value={ME_EVENING}
                               checked={meSelected === ME_EVENING}
                               onChange={this.handleMeInputChange}
                               disabled={selected !== DAILY_REPEATING}
                        />
                        in the evening
                    </label>
                </div>
            </div>
        );
    }
}

NoteRepeatMetadataEditor.propTypes = {
    onChange: propTypes.func,
    repeating: propTypes.object
};

export default NoteRepeatMetadataEditor;