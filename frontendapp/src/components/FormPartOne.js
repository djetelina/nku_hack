import React from 'react';
import { Icon, Input, Button, List, Header, Grid } from 'semantic-ui-react';

import constants from '../Constants';
import ChartBar from './ChartBar';
import ChartPie from './ChartPie';
import HeaderComp from './Header';
import FooterComp from './Footer';

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
    {
        uri: '/api/to_survive',
        prop: 'toSurvive',
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
        margin-right: 1.6em;
    }
    
    hr {
        margin-bottom: 2em;
        margin-top: 2em;
        border solid 2px gray;
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
            street: '',
            firstPart: null,
            selectedLocality: null,
            unemployed: null,
            ageGroups: null,
            deathCauses: null,
            education: null,
            nationality: null,
            marital: null,
            commuting: null,
            toSurvive: null,
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleReset = this.handleReset.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleGetAddressData = this.handleGetAddressData.bind(this);
    }

    componentDidMount() {
        /* eslint-disable */
        let stred = SMap.Coords.fromWGS84(14.41, 50.08);
        this.map_component = new SMap(this._map_div, stred, 12);
        this.map_component.addDefaultLayer(SMap.DEF_BASE).enable();
        this.map_component.addDefaultControls();
        this.marker_layer = new window.SMap.Layer.Marker();
        this.map_component.addLayer(this.marker_layer).enable();
         console.log("map component SET!!!");
        /* eslint-enable */

    }

    changeMapPosition(addressString) {
        /* eslint-disable */
        new SMap.Geocoder(addressString, (geocoder) => {
            if (!geocoder.getResults()[0].results.length) {
                return;
            }

            let results = geocoder.getResults()[0].results;
            if (results.length) {
                this.map_component.setCenter(results[0].coords, false);
                let options = {};
                if (this.last_marker) {
                    // napred odebereme ten puvodni
                    this.marker_layer.removeMarker(this.last_marker);
                }
                this.last_marker = new SMap.Marker(results[0].coords, "myMarker", options);
                this.marker_layer.addMarker(this.last_marker);
            }
        });
        /* eslint-enable */
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
            toSurvive: null,
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
                    <List.Content>
                        <button
                            className="location-button"
                            onClick={this.handleGetAddressData.bind(this, place)}
                        >
                            {place['region_name']}&nbsp;&rarr;&nbsp;{place['district_name']}&nbsp;&rarr;&nbsp;{place['municipality_name']}
                            {(place.street_name) ? <span>&nbsp;&rarr;&nbsp;{place.street_name}</span> : ""}
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
                <div style={{marginBottom: '3em'}}>
                    <Header as='h4'>Přehled ppro vybrané místo:</Header>
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
                <hr />
                <ChartBar data={this.state.unemployed} />
                <hr />
                <ChartBar data={this.state.ageGroups} />
                <hr />
                <ChartBar data={this.state.deathCauses} legend={true} legendAsHref={true} />
                <hr />
                <div style={{ display: 'flex', flexWrap: 'wrap' }}>
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
                <hr />
                <ChartPie data={this.state.commuting} />
                {this.state.toSurvive &&
                <div style={{position: "relative", width: "50%"}}>
                    <div style={{position: "absolute", right: 0, bottom: 0}}>
                        <h2>
                            {this.state.toSurvive.data[0]['value'] > this.state.toSurvive.data[1]['value'] ? "Muži" : "Ženy"}
                            &nbsp;žijí dele o &nbsp;
                            {
                                Math.abs(
                                    parseFloat(
                                        this.state.toSurvive.data[0]['value'] -
                                        this.state.toSurvive.data[1]['value']
                                    ).toFixed(2)
                                )
                            } let
                        </h2>
                    </div>
                    <ChartPie data={this.state.toSurvive}/>
                </div>
                }
            </div>
        );
    }


    render () {
        return (
            <div>
                <div style={{position: 'absolute', top: 0, bottom: 0, left: 0}}>

                    <div id="m" ref={(c) => {this._map_div = c;}} style={{height: '100%', width: 300}}></div>
                </div>
                <div style={{position: 'absolute', top: 0, bottom: 0, left: 300, right: 0, overflow: 'scroll', paddingLeft: 20}}>
                    <HeaderComp />
                    <style>{customCss}</style>
                    <form action="" onSubmit={this.handleSubmit}>
                        <Input icon='search' placeholder='Název ulice' value={this.state.street} onChange={this.handleChange}  />

                        <Button onClick={this.sendForm} style={{marginLeft: '1em'}} primary>Hledat</Button>
                        <Button onClick={this.handleReset} secondary>Zrušit</Button>
                    </form>
                    <List>{this.renderStreets()}</List>

                    {this.renderSelectedLocality()}
                    {this.renderCharts()}

                    <FooterComp />
                </div>
            </div>
        )
    }
}

export default FormPartOne
