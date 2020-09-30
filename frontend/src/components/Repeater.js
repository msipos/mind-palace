import React from 'react';
import Mousetrap from 'mousetrap';
import './Repeater.css';

class Repeater extends React.Component {
    componentDidMount() {
        if (!this.props.choices) return;
        for (const c of this.props.choices) {
            Mousetrap.bind(String(c.payload.keyboard_shortcut), () => {
                this.props.onChoice(c.payload)
            });
        }
    }

    componentWillUnmount() {
        if (!this.props.choices) return;
        for (const c of this.props.choices) {
            Mousetrap.unbind(String(c.key));
        }
    }

    render() {
        if (!this.props.choices) {
            return (
                <div className="Repeater">
                    <div className="Repeater-Label">
                        {this.props.label}
                    </div>
                </div>
            );
        }

        const buttons = [];
        const handleClick = this.props.onChoice;

        let idx = 0;
        for (const choice of this.props.choices) {
            idx += 1;
            const innerHTML = {
                __html: choice.htmlText
            }
            buttons.push(
                <button className="Repeater-Button button" onClick={() => {
                    handleClick(choice.payload);
                }} key={idx}>
                    <span dangerouslySetInnerHTML={innerHTML}/>
                    <div className="Repeater-Button-Keyboard">
                        <span className="fas fa-keyboard Repeater-Button-Keyboard-Shortcut" />
                        {choice.payload.keyboard_shortcut}
                    </div>
                </button>
            );
        }

        return (
            <div className="Repeater">
                <div className="Repeater-Label">
                    {this.props.label}
                </div>
                <div className="Repeater-ButtonBar">
                    {buttons}
                </div>
            </div>
        );
    }
}

export default Repeater;