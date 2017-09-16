import React from 'react';
import PropTypes from 'prop-types';
import * as d3 from 'd3';
import {BarChart} from 'react-easy-chart';


import { Header } from 'semantic-ui-react';


class GraphAgeGroup extends React.Component {

    renderGraph() {
        if (this.props.data) {
            return (
                <div>
                    <Header as='h4'>Věk obyvatelstva okresku</Header>
                    <BarChart
                        axisLabels={{x: 'Věk', y: 'Počet'}}
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

GraphAgeGroup.propTypes = {
    data: React.PropTypes.array,
};

export default GraphAgeGroup;
