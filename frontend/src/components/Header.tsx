import { createPortal } from 'react-dom';

export default function Header () {
    return createPortal(<>
        <section className="navbar-section">
            <a href="/" className="navbar-brand mr-2">GSN</a>
            <a href="/posts" className="btn btn-link">Posts</a>
        </section>
    </>, document.getElementById('header')!);
}