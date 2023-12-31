import { render, act, waitFor, screen } from '@testing-library/react';

import Posts from './Posts';
import { IPost } from './types';

describe('posts are rendered', () => {

    beforeEach(() => {
    })

    afterEach(() => {
    })

    it('should render posts', async () => {

        const post: IPost = {
            id: '1',
            content: 'post content',
            image: 'url',
            author: {
                full_name: 'test',
                email: 'test@mail.com',
                username: '',
                image: ''
            }
        };

        const assetsFetchMock = () => Promise.resolve({
            ok: true,
            json: async () => [post]
        } as Response);

        jest.spyOn(global, "fetch").mockImplementation(assetsFetchMock);

        await act(()=> {
            render(<Posts />);
        });
        
        await waitFor(() => {
            expect(screen.getByText!('Posts')).toBeInTheDocument();
            expect(screen.getByText!('post content')).toBeInTheDocument();
        });

        jest.restoreAllMocks();
    })
})