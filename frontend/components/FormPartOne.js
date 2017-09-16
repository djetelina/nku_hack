import React from 'react';
import { Icon, Input, Button, List } from 'semantic-ui-react';

import constants from '../Constants';
import GraphUnemployed from './GraphUnemployed';
import GraphAgeGroup from './GraphAgeGroup';

const buttonStyle = {
    border: 'none',
    background: 'white',
};

function middleFetch (response) {
    return response.json();
}

function error (e) {
    console.log(e);
}

function getInitForFetch(data) {
    return {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'text/plain',
        },
        body: JSON.stringify(data),
        mode: 'cors',
    };
}

class FormPartOne extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            street: 'vlašimská',
            firstPart: null,
            unemployed: null,
            ageGroups: null,
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleReset = this.handleReset.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleGetAddressData = this.handleGetAddressData.bind(this);
    }

    handleReset(event) {
        this.setState({
            street: '',
            firstPart: null,
            unemployed: '',
            ageGroups: null,
        });
    }

    handleChange(event) {
        this.setState({street: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        const data = { query: this.state.street.trim()};
        fetch(`${constants.serverUri}/api/suggest-locality`, getInitForFetch(data))
        .then(middleFetch)
        .then(data => {
            this.setState({ firstPart: data.data });
            console.log(data.data);
        })
        .catch(error);
    }

    handleGetAddressData(place) {
        fetch(`${constants.serverUri}/api/age-groups`, getInitForFetch(place))
                .then(middleFetch)
                .then((data) => {
                    this.setState({ ageGroups: data.data });
                    console.log('Druhy dotaz pro data do grafu');
                    console.log(data);
                })
                .catch(error);
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
                <GraphUnemployed />
                <GraphAgeGroup data={this.state.ageGroups}/>
            </div>
        )
    }
}

export default FormPartOne
