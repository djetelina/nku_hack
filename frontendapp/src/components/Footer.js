import React from 'react';
import {Header} from 'semantic-ui-react';

const containerStyle = {
    marginTop: '10em',
    marginBottom: '1.5em',
    position: 'fixed',
    right: 100,
    bottom: 0,
    zIndex: 999,
};

class FooterComp extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            showDetail: false,
        };
    }

    toggleDetail() {
        this.setState({
           showDetail: !this.state.showDetail
        });
    }

    renderDetail() {
        if (!this.state.showDetail) return null;
        return (
            <div style={{border: 'solid 2px gray', borderRadius: 8, padding: 6, background: '#EEEEEE'}}>
                Výslovně to zprasili tito:
                <ul>
                    <li>Daňhel Ňuff Prezzl</li>
                    <li>Vitezslaw Čumáček Lacsina</li>
                    <li>Týnek Kostík Kalinowski</li>
                    <li>Tomislav Topa Pawlaczki</li>
                    <li>Daffid Jetel Jethellina</li>
                </ul>
            </div>
        );
    }

    render() {
        return (
            <div style={containerStyle}>
                {this.renderDetail()}
                <span onClick={this.toggleDetail.bind(this)} style={{cursor: 'pointer'}}>Vzniklo pod vlivem spánkového deficitu na hackathonu NKU.</span>
            </div>
        );
    }
}

export default FooterComp;
