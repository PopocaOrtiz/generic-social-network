import React, { FC, FormEvent, useRef, useState } from 'react';

import { login } from '../api';
import Loading from '../../../components/Loading';

const Login: FC = () => {

    const emailRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);

    const [loading, setLoading] = useState<boolean>(false);
    const [errorEmail, setErrorEmail] = useState<boolean>(false);
    const [errorPassword, setErrorPassword] = useState<boolean>(false);
    const [loginError, setLoginError] = useState<boolean>(false);

    const handleSubmit = async (event: FormEvent) {
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

            if (response.ok) {
                setLoginError(true);
                return;
            }

            const data = await response.json();
            const token = data['token'];
            
            localStorage.setItem('token', token);
        } catch(error) {
            // 
            console.log('unexpected error login user', error);
        }
    }

    return <>
        <form onSubmit={handleSubmit}>
            <p>
                <label htmlFor="email">e-mail:</label>
                <input type="text" ref={emailRef}/>
                {errorEmail && <label>error in the email</label>}
            </p>
            <p>
                <label htmlFor="password">password:</label>
                <input type="password" ref={passwordRef}/>
                {errorPassword && <label>error in password</label>}
            </p>
            <p>
                <input type="submit" disabled={loading}/>
                <Loading show={loading} />
                {loginError && <label>incorrect credentials</label>}
            </p>
        </form>
    </>;
}

export default Login;