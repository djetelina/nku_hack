import React from 'react';
import {BarChart, Legend} from 'react-easy-chart';


import { Header } from 'semantic-ui-react';


const legendBulletStyle = {
    width: '12px',
    height: '12px',
    display: 'inline-block',
    borderRadius: '13px',
    marginRight: '1em',
};

class ChartBar extends React.Component {

    renderLegend() {
        if (this.props.legend && this.props.data) {
            return this.props.data.data.map((item, key) => {
                return (
                    <div key={key}>
                        <span style={{background: item.color, ...legendBulletStyle}}></span>
                        <span>{item.x}</span>
                    </div>
                )
            });
        }

        return null;
    }

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
                    {this.renderLegend()}
                </div>
            );
        }

        return null;
    }

    render () {
        return (
            <div>
                {this.renderGraph()}
                {this.renderLegend()}
            </div>
        )
    }
}

ChartBar.defaultProps = {
    legend: false,
};

ChartBar.propTypes = {
    data: React.PropTypes.object,
    legend: React.PropTypes.boolean,
};

export default ChartBar;
