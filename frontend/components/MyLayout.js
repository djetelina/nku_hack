import Header from './Header';

import { Container } from 'semantic-ui-react';


const Layout = (props) => (
    <Container>
        <Header />
        {props.children}
    </Container>
);

export default Layout
