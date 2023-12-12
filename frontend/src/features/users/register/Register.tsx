import React, { useRef, FC, FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { IUserCreate } from '../types';
import { registerUser } from '../api';
import Loading from '../../../components/Loading';
import FormGroup from '../../../components/FormGroup';

const Register: FC = () => {

    const firstNameRef = useRef<HTMLInputElement>(null);
    const lastNameRef = useRef<HTMLInputElement>(null);
    const emailRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);

    const [loading, setLoading] = useState<boolean>(false);
    const [success, setSuccess] = useState<boolean>(false);
    const [error, setError] = useState<string>("");
    const [missingFields, setMissingFields] = useState<string[]>([]);
    const [errors, setErrors] = useState<IUserCreate>({
        first_name: '',
        last_name: '',
        email: '',
        password: ''
    });

    const navigate = useNavigate();
    

    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();

        const user: IUserCreate = {
            first_name: firstNameRef.current!.value.trim(),
            last_name: lastNameRef.current!.value.trim(),
            email: emailRef.current!.value.trim(),
            password: passwordRef.current!.value.trim()
        }

        const errors: any = {}

        if (!user.first_name) {
            errors['first_name'] = 'missing field';
        }
        if (!user.last_name) {
            errors['last_name'] = 'missing field';
        }
        if (!user.email) {
            errors['email'] = 'missing field';
        }
        if (!user.password) {
            errors['password'] = 'missing field';
        }

        if (Object.keys(errors).length) {
            setErrors(errors);
            return;
        }

        // todo: check for valid email

        setMissingFields(missingFields);
        if (missingFields.length) {
            return;
        }

        try {

            setLoading(true);
            const response = await registerUser(user);
            
            if (response.ok) {
                
                setSuccess(true);
                setTimeout(() => navigate('/login'), 3000);

            } else {
                const errors = await response.json();
                setErrors(errors);
            }

        } catch (error) {
            setError('unexpected error');
            console.log('unexpected error', error);
        }

        setLoading(false);
    }

    return <>
        <h2>Create an account</h2>
        {!success && (
        <form onSubmit={handleSubmit} className="form-group">
            <FormGroup error={errors.first_name}>
                <label htmlFor="first_name">First name:</label>
                <input type="text" ref={firstNameRef} />
            </FormGroup>
            <FormGroup error={errors.last_name}>
                <label htmlFor="lastName">Last name:</label>
                <input type="text" ref={lastNameRef}/>
            </FormGroup>
            <FormGroup error={errors.email}>
                <label htmlFor="lastName">e-mail:</label>
                <input type="text" ref={emailRef}/>
            </FormGroup>
            <FormGroup error={errors.password}>
                <label htmlFor="lastName">Password:</label>
                <input type="password" ref={passwordRef} pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"/>
            </FormGroup>
            <br />
            <FormGroup>
                <input type="submit" disabled={loading} className="float-right"/>
                <Loading show={loading}/>
            </FormGroup>
        </form>
        )}
        {success && (<div className="toast toast-success">
            Registration was successful. Redirecting...
        </div>)}
        {error && (<div className="toast toast-error">
            An error occurred.
        </div>)}
    </>;
};

export default Register;