import React from 'react';
import Mousetrap from 'mousetrap';
import './Repeater.css';

class Repeater extends React.Component {
    componentDidMount() {
        for (const c of this.props.choices) {
            Mousetrap.bind(String(c.key), () => {
                this.props.onChoice(c.payload)
            });
        }

        Mousetrap.bind('e', () => {
            this.props.onEdit();
        });
    }

    componentWillUnmount() {
        for (const c of this.props.choices) {
            Mousetrap.unbind(String(c.key));
        }

        Mousetrap.unbind('e');
    }

    render() {
        const buttons = [];
        const handleClick = this.props.onChoice;

        // Add edit button
        buttons.push(
            <button className="button" key={-1} onClick={() => this.props.onEdit()}>Edit (e)</button>
        );

        let idx = 0;
        for (const choice of this.props.choices) {
            idx += 1;
            const innerHTML = {
                __html: choice.htmlText
            }
            buttons.push(
                <button className="button" onClick={() => {
                    handleClick(choice.payload);
                }} key={idx}>
                    <span dangerouslySetInnerHTML={innerHTML}/>
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