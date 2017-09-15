import React from 'react';
import PropTypes from 'prop-types';



import { Header } from 'semantic-ui-react';


class GraphUnemployed extends React.Component {

    constructor(props) {
        super(props);
        debugger;
    }

    renderGraph() {
        if (this.props.data) {
            return (
                <div>
                    <Header as='h4'>Nezaměstnanost</Header>


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

GraphUnemployed.defaultProps = {
    data: [
      { x: 10, y: 20 },
      { x: 12, y: 20 },
      { x: 30, y: 30, color: '#f00' },
      { x: 40, y: 40 }
    ],
};

GraphUnemployed.propTypes = {
    data: React.PropTypes.array,
};

export default GraphUnemployed;
