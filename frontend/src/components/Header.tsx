import { createPortal } from 'react-dom';
import { Link } from 'react-router-dom';

export default function Header () {

    const tokenExists = localStorage.getItem('token') ? true : false;

    return createPortal(<>
        <section className="navbar-section">
            <a href="/" className="navbar-brand mr-2">GSN</a>
            <Link to="posts" className="btn btn-link">Posts</Link>
        </section>
        {!tokenExists && (
            <section className="navbar-section">
                <Link to="login" className="btn btn-link">Login</Link>
                <div className="divider-vert" data-content="OR"></div>
                <Link to="sign-up" className="btn btn-link">Sign Up</Link>
            </section>
        )}
        {tokenExists && (
            <section className="navbar-section">
                <Link to="me" className="btn btn-link">logout</Link>
            </section>
        )}
    </>, document.getElementById('header')!);
}