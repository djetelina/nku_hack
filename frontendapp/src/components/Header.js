import React from 'react';
import {Header} from 'semantic-ui-react';

const containerStyle = {
    marginTop: '1em',
    marginBottom: '1.5em'
};

const HeaderComp = () => (
    <div style={containerStyle}>
        <Header as='h2'>Informace o místě</Header>
    </div>
);

export default HeaderComp
