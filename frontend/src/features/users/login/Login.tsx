import React, { FC, FormEvent, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { login } from '../api';
import Loading from '../../../components/Loading';
import FormGroup from '../../../components/FormGroup';

const Login: FC = () => {

    const emailRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);

    const [loading, setLoading] = useState<boolean>(false);
    const [errorEmail, setErrorEmail] = useState<boolean>(false);
    const [errorPassword, setErrorPassword] = useState<boolean>(false);
    const [loginError, setLoginError] = useState<boolean>(false);
    const [success, setSuccess] = useState<boolean>(false);

    const navigate = useNavigate();

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
        <h2>Login</h2>
        {!success && (
        <form onSubmit={handleSubmit} className="form-group">
            <FormGroup error={errorEmail ? 'missing email' : ''}>
                <label htmlFor="email">Email</label>
                <input type="email" ref={emailRef}/>
            </FormGroup>
            <FormGroup error={errorPassword ? 'missing password' : ''}>
                <label htmlFor="password">Password</label>
                <input type="password" ref={passwordRef}/>
            </FormGroup>
            <div className="divider"></div>
            <FormGroup>
                <input type="submit" disabled={loading} className='float-right'/>
                <div className="clearfix"></div>
                <Loading show={loading} />
            </FormGroup>
            {loginError && (<div className="toast toast-error">
                Login was not successful.
            </div>)}
        </form>
        )}
        {success && (<div className="toast toast-success">
            Login was successful. Redirecting...
        </div>)}
    </>;
}

export default Login;