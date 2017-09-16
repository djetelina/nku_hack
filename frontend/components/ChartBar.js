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

    renderTextInLegend(text, i) {
        if (this.props.legendAsHref) {
            return (
                <a
                    rel="noopener noreferrer"
                    target="_blank"
                    href={`https://search.seznam.cz/?q=${text}`}
                >
                    {i + 1}. {text}
                </a>
            );
        } else {
            return <span>{text}</span>
        }
    }

    renderArrLegend() {
        return this.props.data.data.map((item, i) => {
            return (
                <div key={i}>
                    <span style={{background: item.color, ...legendBulletStyle}}></span>
                    <span>
                        {this.renderTextInLegend(item.x, i)}
                    </span>
                </div>
            )
        });
    }

    renderLegend() {
        if (this.props.legend && this.props.data) {
            return (
                <div style={{marginBottom: '2em'}}>
                    {this.renderArrLegend()}
                </div>
            );
        }

        return null;
    }

    getDataForGraph() {
        if (this.props.legend) {
            return this.props.data.data.map((item, i) => {return {y: item.y, color: item.color, x: i + 1}});
        } else {
            return this.props.data.data;
        }
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
                        data={this.getDataForGraph()}
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
                {this.renderLegend()}
            </div>
        )
    }
}

ChartBar.defaultProps = {
    legend: false,
    legendAsHref: false,
};

ChartBar.propTypes = {
    data: React.PropTypes.object,
    legend: React.PropTypes.bool,
    legendAsHref: React.PropTypes.bool,
};

export default ChartBar;
