import React from 'react';
import {BarChart, Legend} from 'react-easy-chart';


import { Header } from 'semantic-ui-react';


class ChartBar extends React.Component {

    renderGraph() {
        if (this.props.data) {
            return (
                <div>
                    <Header as='h4'>{this.props.data.title}</Header>
                    <BarChart
                        //axisLabels={{x: 'Věk', y: 'Počet'}}
                        axes
                        grid
                        colorBars
                        width={800}
                        data={this.props.data.data}
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

ChartBar.propTypes = {
    data: React.PropTypes.object,
};

export default ChartBar;
