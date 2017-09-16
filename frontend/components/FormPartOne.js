import React from 'react';
import { Icon, Input, Button, List, Header } from 'semantic-ui-react';

import constants from '../Constants';
import ChartBar from './ChartBar';
import ChartPie from './ChartPie';

const DATA_FETCH = [
    {
        uri: '/api/age-groups',
        prop: 'ageGroups',
    },
    {
        uri: '/api/unemployed',
        prop: 'unemployed',
    },
    {
        uri: '/api/death-causes',
        prop: 'deathCauses',
    },
    {
        uri: '/api/education',
        prop: 'education',
    },
    {
        uri: '/api/nationality',
        prop: 'nationality',
    },
    {
        uri: '/api/marital-status',
        prop: 'marital',
    },
    {
        uri: '/api/commuting',
        prop: 'commuting',
    },
];

const customCss = `
    .location-button:hover {
        border: 1px solid black;
    }
    .location-button {
        background-color: white;
        border: 1px solid white;
        padding-top: 4px;
        padding-bottom: 4px;
        border-radius: 8px;
    }
`;

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
            selectedLocality: null,
            unemployed: null,
            ageGroups: null,
            deathCauses: null,
            education: null,
            nationality: null,
            marital: null,
            commuting: null,
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
            unemployed: null,
            ageGroups: null,
            deathCauses: null,
            education: null,
            nationality: null,
            marital: null,
            commuting: null,
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
            this.setState({ firstPart: data.data, selectedLocality: null });
            console.log(data.data);
        })
        .catch(error);
    }

    handleGetAddressData(place) {
        this.setState({firstPart: null, selectedLocality: place});

        for (let i = 0; i < DATA_FETCH.length; i++) {
            fetch(`${constants.serverUri}${DATA_FETCH[i].uri}`, getInitForFetch(place))
                .then(middleFetch)
                .then((data) => {
                    this.setState({ [DATA_FETCH[i].prop]: data.data });
                    console.log(data);
                })
                .catch(error);
        }
    }

    renderStreets() {
        if (this.state.firstPart) {
            return this.state.firstPart.results.map((place, i) =>
                <List.Item key={i}>
                    <List.Icon name='marker' />
                    <List.Content>
                        <button
                            className="location-button"
                            onClick={this.handleGetAddressData.bind(this, place)}
                        >
                            {place['region_name']}&nbsp;&rarr;&nbsp;{place['district_name']}&nbsp;&rarr;&nbsp;{place['municipality_name']}
                        </button>
                    </List.Content>
                </List.Item>
            );
        } else {
            return null;
        }
    }

    renderSelectedLocality() {
        if (this.state.selectedLocality) {
            let place = this.state.selectedLocality;
            return (
                <div style={{marginBottom: 20}}>
                    <Header as='h4'>Data pro vybranou lokalitu:</Header>
                    <span
                        style={{fontSize: '1.5em'}}
                    >
                        {place['region_name']}&nbsp;&rarr;&nbsp;{place['district_name']}&nbsp;&rarr;&nbsp;{place['municipality_name']}
                    </span>
                </div>
            );
        } else {
            return "";
        }
    }

    render () {
        return (
            <div>
                <style>{customCss}</style>
                <form action="" onSubmit={this.handleSubmit}>
                    <Input icon='search' placeholder='Název ulice' value={this.state.street} onChange={this.handleChange}  />

                    <Button onClick={this.sendForm} style={{marginLeft: '1em'}} primary>Hledat</Button>
                    <Button onClick={this.handleReset} secondary>Zrušit</Button>
                </form>
                <List>{this.renderStreets()}</List>

                {this.renderSelectedLocality()}

                <ChartBar data={this.state.unemployed} />
                <ChartBar data={this.state.ageGroups} />
                <ChartBar data={this.state.deathCauses} legend={true} legendAsHref={true} />
                <ChartPie data={this.state.education} />
                <ChartPie data={this.state.nationality} />
                <ChartPie data={this.state.marital} />
                <ChartPie data={this.state.commuting} />
            </div>
        )
    }
}

export default FormPartOne
