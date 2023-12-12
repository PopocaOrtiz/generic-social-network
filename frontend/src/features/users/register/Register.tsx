import React, { useRef, FC, FormEvent, useState } from 'react';

import { IUser } from '../types';
import { registerUser } from '../api';
import Loading from '../../../components/Loading';

const Register: FC = () => {

    const firstNameRef = useRef<HTMLInputElement>(null);
    const lastNameRef = useRef<HTMLInputElement>(null);
    const emailRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);

    const [loading, setLoading] = useState<boolean>(false);
    const [success, setSuccess] = useState<boolean>(false);
    const [missingFields, setMissingFields] = useState<string[]>([]);

    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();

        const user: IUser = {
            first_name: firstNameRef.current!.value.trim(),
            last_name: lastNameRef.current!.value.trim(),
            email: emailRef.current!.value.trim(),
            password: passwordRef.current!.value.trim()
        }

        const missingFields = [];
        if (!user.first_name.trim()) {
            missingFields.push('first_name');
        }
        if (!user.last_name) {
            missingFields.push('last_name');
        }
        if (!user.email) {
            missingFields.push('email');
        }
        if (!user.password) {
            missingFields.push('password');
        }

        // todo: check for valid email

        setMissingFields(missingFields);
        if (missingFields.length) {
            return;
        }
        
        console.log(user);

        try {

            setLoading(true);
            const response = await registerUser(user);
            
            if (!response.ok) {
                // todo: display input with errors
                const errors = await response.json();
                console.log('error registering user', errors);
                return;
            }

            setSuccess(true);

        } catch (error) {
            // todo: display error
            console.log('error registering user');
        }

        setLoading(false);
    }

    return <>
        <h1>Register new user</h1>
        <form onSubmit={handleSubmit}>
            <p>
                <label htmlFor="first_name">First name:</label>
                <input type="text" ref={firstNameRef}/>
                {missingFields.indexOf('first_name') && <label>missing first name</label>}
            </p>
            <p>
                <label htmlFor="lastName">Last name:</label>
                <input type="text" ref={lastNameRef}/>
                {missingFields.indexOf('last_name') && <label>missing first name</label>}
            </p>
            <p>
                <label htmlFor="email">e-mail:</label>
                <input type="email" ref={emailRef}/>
                {missingFields.indexOf('email') && <label>missing first name</label>}
            </p>
            <p>
                <label htmlFor="password">Password:</label>
                <input type="password" ref={passwordRef}/>
                {missingFields.indexOf('password') && <label>missing first name</label>}
                {/* todo: component to show password complexity */}
            </p>
            <p>
                <input type="submit" disabled={loading}/>
                <Loading show={loading}/>
            </p>
        </form>
    </>;
};

export default Register;