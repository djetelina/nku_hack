import Head from 'next/head';
import { Container } from 'semantic-ui-react';


const Layout = (props) => (
    <Container>
        <Head>
            <link rel='stylesheet' href='//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.2/semantic.min.css' />
        </Head>
        {props.children}
    </Container>
);

export default Layout
