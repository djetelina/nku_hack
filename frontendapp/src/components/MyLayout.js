import Head from 'next/head';
import { Container } from 'semantic-ui-react';


const Layout = (props) => (
    <div>
        <link rel='stylesheet' href='//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.2/semantic.min.css' />
        {props.children}
    </div>
);

export default Layout
