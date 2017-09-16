import React from 'react';
import {Header} from 'semantic-ui-react';

const containerStyle = {
    marginTop: '10em',
    marginBottom: '1.5em',
    position: 'fixed',
    right: 100,
    bottom: 0,
    zIndex: 999,
};

const FooterComp = () => (
    <div style={containerStyle}>
        Vzniklo v rámci hacktathonu NKU.
    </div>
);

export default FooterComp;
