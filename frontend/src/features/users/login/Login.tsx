import React, { FC, FormEvent, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { login as loginAction } from '../userSlice';

import { useDispatch } from 'react-redux';

import { login } from '../api';

import { TextField, Typography, Stack, Alert } from '@mui/material';
import LoadingButton from '@mui/lab/LoadingButton';

const Login: FC = () => {

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const emailRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);

    const [loading, setLoading] = useState<boolean>(false);
    const [errorEmail, setErrorEmail] = useState<boolean>(false);
    const [errorPassword, setErrorPassword] = useState<boolean>(false);
    const [loginError, setLoginError] = useState<boolean>(false);
    const [success, setSuccess] = useState<boolean>(false);

    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();

        const email = emailRef.current!.value.trim();
        const password = passwordRef.current!.value.trim();

        if (!email) {
            setErrorEmail(true);
            return;
        }

        if (!password) {
            setErrorPassword(true);
            return
        }

        try {

            setLoading(true);
            const response = await login(email, password);
            const responseData = await response.json();

            if (response.ok) {

                const token = responseData['token'];
            
                localStorage.setItem('token', token);

                setSuccess(true);
                dispatch(loginAction());
    
                setTimeout(() => {
                    navigate('/posts');
                }, 3000);

            } else {
                setLoginError(true);
                console.log(responseData);
            }

        } catch(error) {
            setLoginError(true);
            console.log('unexpected error login user', error);
        }

        setLoading(false);
    }

    return <>
        <Typography variant="h4" textAlign={"center"}>
            Login
        </Typography>
        {!success && (
        <form onSubmit={handleSubmit} noValidate autoComplete="off">
            <Stack spacing={2}>
                <TextField label="Email" 
                    inputRef={emailRef} 
                    error={errorEmail} 
                    helperText={errorEmail ? 'missing email' : ''} 
                    inputProps={{ 'data-testid': 'email-input' }}/>
                <TextField label="Password"
                    type='password'
                    inputRef={passwordRef}
                    error={errorPassword}
                    helperText={errorPassword ? 'missing password' : ''} 
                    inputProps={{ 'data-testid': 'password-input' }} />
                <LoadingButton variant='contained'
                    onClick={handleSubmit}
                    loading={loading}   
                    disabled={loading}
                    data-testid="submit-button">
                    Submit
                </LoadingButton>
                {loginError && (<div className="toast toast-error">
                    Login was not successful.
                </div>)}
            </Stack>
        </form>
        )}
        {success && (<Alert severity="success">
            Login was successful. Redirecting...
        </Alert>)}
    </>;
}

export default Login;