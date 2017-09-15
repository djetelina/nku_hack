import Head from 'next/head';
import Link from 'next/link';

import { Modal, Header, Button, List } from 'semantic-ui-react';

const containerStyle = {
    marginTop: '3em',
};
const navigationStyle = {
    marginBottom: '3em',
};
const linkStyle = {
    marginRight: '1em',
};

const HeaderComp = () => (
    <div style={containerStyle}>
        <Head>
            <link rel='stylesheet' href='//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.2/semantic.min.css' />
        </Head>
        <Header as='h3'>Kvalita místa pro život - Hackathon Prague projekt</Header>
        <div style={navigationStyle}>
            <Link href="/">
                <a style={linkStyle}>Home</a>
            </Link>&nbsp;
            <Link href="/about">
                <a style={linkStyle}>O týmu</a>
            </Link>
        </div>
    </div>
);

export default HeaderComp
