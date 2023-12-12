import React from 'react';
import { render, fireEvent, act } from '@testing-library/react';

import PostForm from './PostForm';
import * as apiPosts from '../api';
import { IPost } from '../types';

describe('test form create post', () => {
    it('should execute function on success', async () => {
        
        const mockData: IPost = {
            id: '1',
            content: 'post content',
            image: 'url',
            author: {
                full_name: 'test_user',
                email: 'test@mail.com',
                image: '',
                username: '',
            }
        }

        const mockPostCreatedHandler = jest.fn();

        jest.spyOn(apiPosts, 'createPost').mockResolvedValue({
            ok: true,
            json: jest.fn().mockResolvedValue(mockData)
        } as any);

        let component: any;
        act(() => {
            component = render(<PostForm onPostCreated={mockPostCreatedHandler} />);  
        })

        const { findByTestId } = component;
        
        const submit = await findByTestId('submit');

        await act(async () => {

            fireEvent.click(submit);
            
            await new Promise(resolve => setTimeout(resolve, 0));
            
            expect(apiPosts.createPost).toHaveBeenCalled();
            expect(mockPostCreatedHandler).toHaveBeenCalledWith(mockData);
        })
    })
})