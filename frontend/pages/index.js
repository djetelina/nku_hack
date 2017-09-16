import React from 'react';
import { bindActionCreators } from 'redux';
import withRedux from 'next-redux-wrapper';

import { initStore, startClock, addCount, serverRenderClock } from '../store';
import FormPartOne from '../components/FormPartOne';
import { Icon, Input } from 'semantic-ui-react'


class Counter extends React.Component {
    static getInitialProps ({ store, isServer }) {
        store.dispatch(serverRenderClock(isServer))
        store.dispatch(addCount())

        return { isServer }
    }

    componentDidMount () {
        this.timer = this.props.startClock()
    }

    componentWillUnmount () {
        clearInterval(this.timer)
    }

    render () {
        return (
            <div>
                <link rel='stylesheet' href='//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.2/semantic.min.css' />
                <script src="https://api.mapy.cz/loader.js"></script>
                <script type="text/javascript">Loader.load()</script>
                <FormPartOne />
            </div>
        )
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        addCount: bindActionCreators(addCount, dispatch),
        startClock: bindActionCreators(startClock, dispatch),
    }
};

export default withRedux(initStore, null, mapDispatchToProps)(Counter)
