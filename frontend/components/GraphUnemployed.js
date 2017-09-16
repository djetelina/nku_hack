import React from 'react';
import PropTypes from 'prop-types';
import * as d3 from 'd3';
import {BarChart} from 'react-easy-chart';


import { Header } from 'semantic-ui-react';


class GraphUnemployed extends React.Component {
    renderGraph() {
        if (this.props.data) {
            return (
                <div>
                    <Header as='h4'>Nezaměstnanost</Header>
                    <div id="graph-unemployed" />
                    <BarChart
                        axisLabels={{x: 'Roky', y: 'Počet'}}
                        axes
                        grid
                        colorBars
                        width={800}
                        data={this.props.data}
                    />
                </div>
            );
        }

        return null;
    }

    render () {
        return (
            <div>
                {this.renderGraph()}
            </div>
        )
    }
}

GraphUnemployed.propTypes = {
    data: React.PropTypes.array,
};

export default GraphUnemployed;
