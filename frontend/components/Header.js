import Link from 'next/link';
import {Header} from 'semantic-ui-react';

const containerStyle = {
    marginTop: '1em',
    marginBottom: '1.5em'
};

const HeaderComp = () => (
    <div style={containerStyle}>
        <Header as='h3'>Informace o místě</Header>
    </div>
);

export default HeaderComp
