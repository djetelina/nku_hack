import React from 'react';
import {PieChart, Legend} from 'react-easy-chart';


import { Header } from 'semantic-ui-react';


class ChartPie extends React.Component {

    renderGraph() {
        if (this.props.data) {
            return (
                <div>
                    <Header as='h4'>{this.props.data.title}</Header>
                    <div style={{marginBottom: '1.5em'}}>
                        <PieChart
                            size={250}
                            data={this.props.data.data}
                        />
                    </div>
                    <Legend data={this.props.data.data} dataId={'key'} />
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
