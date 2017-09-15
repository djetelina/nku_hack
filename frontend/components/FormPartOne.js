import React from 'react';
import { Icon, Input, Button, List } from 'semantic-ui-react';

import constants from '../Constants';

const buttonStyle = {
    border: 'none',
    background: 'white',
};

class FormPartOne extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            street: 'horymírova',
            firstPart: null,
            unemployed: null,
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleReset = this.handleReset.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleGetAddressData = this.handleGetAddressData.bind(this);
    }

    handleReset(event) {
        this.setState({street: '', firstPart: null, unemployed: ''});
    }

    handleChange(event) {
        this.setState({street: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        fetch(`${constants.serverUri}/api/suggest-locality?query=${this.state.street.trim()}`)
        .then((response) => {
            return response.json();
        })
        .then(data => {
            this.setState({ firstPart: data.data });
            console.log(data.data);
        })
    }

    handleGetAddressData(place) {

        //fetch(`${constants.serverUri}/api/suggest-locality?query=${this.state.street.trim()}`, )
    }

    renderStreets() {
        if (this.state.firstPart) {
            return this.state.firstPart.results.map((place, i) =>
                <List.Item key={i}>
                    <List.Icon name='marker' />
                    <List.Content>
                        <button
                                onClick={this.handleGetAddressData.bind(this, place)}
                                style={buttonStyle}
                        >
                            {place['district_name']}, {place['region_name']}
                        </button>
                    </List.Content>
                </List.Item>
            );
        } else {
            return null;
        }
    }

    render () {
        return (
            <div>
                <form action="" onSubmit={this.handleSubmit}>
                    <Input icon='search' placeholder='Název ulice' value={this.state.street} onChange={this.handleChange}  />

                    <Button onClick={this.sendForm} style={{marginLeft: '1em'}} primary>Hledat</Button>
                    <Button onClick={this.handleReset} secondary>Zrušit</Button>
                </form>
                 <List>{this.renderStreets()}</List>
            </div>
        )
    }
}

export default FormPartOne
