import Link from 'next/link';
import {Header} from 'semantic-ui-react';

const containerStyle = {
    marginTop: '1em',
    marginBottom: '1.5em'
};
const navigationStyle = {
    marginBottom: '3em',
};
const linkStyle = {
    marginRight: '1em',
};

const HeaderComp = () => (
    <div style={containerStyle}>
        <Header as='h3'>Kvalita místa pro život - Hackathon Prague projekt</Header>
    </div>
);

export default HeaderComp
