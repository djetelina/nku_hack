import React from 'react';
import {PieChart, Legend} from 'react-easy-chart';


import { Header } from 'semantic-ui-react';


class ChartPie extends React.Component {

    renderGraph() {
        if (this.props.data) {
            return (
                <div>
                    <Header as='h4'>{this.props.data.title}</Header>
                    <PieChart
                        size={300}
                        data={this.props.data.data}
                    />
                    <Legend data={this.props.data.data} dataId={'key'} config={{}} />
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

ChartPie.propTypes = {
    data: React.PropTypes.object,
};

export default ChartPie;
/**
 * Created by tomaspavlacky on 9/16/17.
 */
