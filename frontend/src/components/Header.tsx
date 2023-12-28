import { createPortal } from 'react-dom';
import { Link } from 'react-router-dom';

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

import { useSelector } from 'react-redux';

export default function Header () {

    const tokenExists = localStorage.getItem('token') ? true : false;

    const loginStatus = useSelector((state: any) => state.user.status);

    let userButtons: JSX.Element;
    if (loginStatus == 'logout') {
        userButtons = (<>
            <Link to="login">
                <Button>
                    Login
                </Button>
            </Link>
            <Link to="sign-up">
                <Button>
                    Sign Up
                </Button>
            </Link>
        </>);
    } else {
        userButtons = (
            <Link to="me">
                <Button>logout</Button>
            </Link>
        );
    }

    return createPortal(
        <AppBar>
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    GSN
                </Typography>
                <Link to="posts">
                    <Button>
                        Posts
                    </Button>
                </Link>
                {userButtons}
            </Toolbar>
        </AppBar>
    , document.getElementById('header')!);
}