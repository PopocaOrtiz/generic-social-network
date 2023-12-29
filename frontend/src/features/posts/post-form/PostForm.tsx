import React, { FC, FormEvent, useEffect, useRef, useState } from 'react';

import { Typography } from '@mui/material';

import { createPost } from '../api';
import { IPost } from '../types';
import Loading from '../../../components/Loading';
import FormGroup from '../../../components/FormGroup';

const messages = [
    'write something meaningful...',
    'how are you feeling today...'
];

interface Props {
    onPostCreated: (post: IPost) => void
}

const PostForm: FC<Props> = ({ onPostCreated }) => {

    const contentInputRef = useRef<HTMLTextAreaElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const [loading, setLoading] = useState<boolean>(false);
    const [message, setMessage] = useState<string>('');

    useEffect(() => {
        if (contentInputRef.current) {
            contentInputRef.current.focus();
        }
    }, []);

    const submitHandler = async (e: FormEvent) => {
        e.preventDefault();

        const files = fileInputRef.current!.files;
        const data = {
            content: contentInputRef.current!.value,
            image_file: files && files.length ? files[0] : null,
        }

        try {
            setLoading(true);
            setMessage('');
            const response = await createPost(data);
            const responseData = await response.json();

            if (response.ok) {
                onPostCreated(responseData);
            } else {
                setMessage(responseData['error']);
                console.log('errors creating post', responseData);
            }

        } catch (error: any) {
            setMessage(error.toString());
            console.log('unexpected error', error);
        }

        setLoading(false);
    }

    const contentPlaceHolder = messages[Math.floor(Math.random() * messages.length)];

    return <>
        <Typography variant="h5">New post</Typography>
        <form onSubmit={submitHandler} data-testid='post-form'>
            <FormGroup>
                <label htmlFor="content">Conent</label>
                <textarea ref={contentInputRef} placeholder={contentPlaceHolder} name="content"></textarea>
            </FormGroup>
            <FormGroup>
                <label htmlFor="image">Image:</label>
                <input type="file" ref={fileInputRef} />
            </FormGroup>
            <FormGroup>
                <input type="submit" data-testid='submit' className='float-right' disabled={loading} />
                {message && <span>{message}</span>}
            </FormGroup>
            <Loading show={loading} />
        </form>
    </>;
}

export default PostForm;