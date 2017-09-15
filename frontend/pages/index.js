import React from 'react';
import { bindActionCreators } from 'redux';
import withRedux from 'next-redux-wrapper';

import { initStore, startClock, addCount, serverRenderClock } from '../store';
import Layout from '../components/MyLayout.js';
import FormPartOne from '../components/FormPartOne';
import { Icon, Input } from 'semantic-ui-react'

//import logo from '../static/logo.png';


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
            <Layout>
                <FormPartOne />
            </Layout>
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
