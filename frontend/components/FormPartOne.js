import React from 'react';
import ReactDOM from 'react-dom';
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
    .pie-column {
        margin-right: 1em;
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

    componentDidMount() {
        window.onload = () => {
            let stred = SMap.Coords.fromWGS84(14.41, 50.08);
            this.map_component = new SMap(this._map_div, stred, 12);
            this.map_component.addDefaultLayer(SMap.DEF_BASE).enable();
            this.map_component.addDefaultControls();
            this.marker_layer = new SMap.Layer.Marker();
            this.map_component.addLayer(this.marker_layer).enable();

        };
    }

    changeMapPosition(addressString) {
        new SMap.Geocoder(addressString, (geocoder) => {
            if (!geocoder.getResults()[0].results.length) {
                return;
            }

            let vysledky = geocoder.getResults()[0].results;
            if (vysledky.length) {
                this.map_component.setCenter(vysledky[0].coords, false);
                let options = {};
                if (this.last_marker) {
                    // napred odebereme ten puvodni
                    this.marker_layer.removeMarker(this.last_marker);
                }
                this.last_marker = new SMap.Marker(vysledky[0].coords, "myMarker", options);
                this.marker_layer.addMarker(this.last_marker);
            }
        });
    }

    changeMapToPlace(place) {
        let fullName = [];
        let keys = ["street_name", "municipality_part_name", "municipality_name", "district_name"];
        keys.forEach((key) => {
           if (place.hasOwnProperty(key)) {
               fullName.push(place[key]);
           }
        });
        let address = fullName.join(", ");
        this.changeMapPosition(address);
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
        this.changeMapToPlace(place);

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

    renderCharts() {
        if (!this.state.selectedLocality) {
            return null;
        }

        return (
            <div>
                <ChartBar data={this.state.unemployed} />
                <ChartBar data={this.state.ageGroups} />
                <ChartBar data={this.state.deathCauses} legend={true} legendAsHref={true} />
                <div style={{ display: 'flex' }}>
                    <div className="pie-column">
                        <ChartPie data={this.state.education} />
                    </div>
                    <div className="pie-column">
                        <ChartPie data={this.state.nationality} />
                    </div>
                    <div className="pie-column">
                        <ChartPie data={this.state.marital} />
                    </div>
                </div>
                <ChartPie data={this.state.commuting} />
            </div>
        );
    }


    render () {
        return (
            <div>

                <script src="https://api.mapy.cz/loader.js"></script>
                <script type="text/javascript">Loader.load()</script>

                <style>{customCss}</style>
                <form action="" onSubmit={this.handleSubmit}>
                    <Input icon='search' placeholder='Název ulice' value={this.state.street} onChange={this.handleChange}  />

                    <Button onClick={this.sendForm} style={{marginLeft: '1em'}} primary>Hledat</Button>
                    <Button onClick={this.handleReset} secondary>Zrušit</Button>
                </form>
                <List>{this.renderStreets()}</List>

                {this.renderSelectedLocality()}
                <div id="m" ref={(c) => {this._map_div = c;}} style={{height:200, widht:'100%', marginTop: 10, marginBottom: 10}}></div>
                {this.renderCharts()}

            </div>
        )
    }
}

export default FormPartOne
