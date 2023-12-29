import { render, screen, fireEvent, waitForElementToBeRemoved } from '@testing-library/react';

import Posts from './Posts';
import * as api from './api';

describe('<Posts />', () => {
  test('renders Posts component', async () => {

    render(<Posts />);

    const heading = screen.getByRole('heading');
    expect(heading).toBeInTheDocument();

    const addButton = screen.getByLabelText('add-post');
    expect(addButton).toBeInTheDocument();

    const loading = screen.getByRole("progressbar");
    expect(loading).toBeInTheDocument();

    const errorMessage = await screen.findByText(/error fetching posts/);

    expect(errorMessage).toBeInTheDocument();
  });

  test('shows the new post form', async () => {
    render(<Posts />);
    const addButton = screen.getByLabelText('add-post');
    fireEvent.click(addButton);

    const formElement = await screen.findByRole('heading', {level: 5});
    expect(formElement).toBeInTheDocument();
  });

  test('searches posts', async () => {

    const { findByTestId } = render(<Posts />);
    const inputElement = await findByTestId('search-posts-input');

    api.fetchPosts = jest.fn(() => Promise.resolve([]));

    fireEvent.change(inputElement, { target: { value: 'test'}});

    await waitForElementToBeRemoved(screen.getByRole('progressbar'));

    expect(api.fetchPosts).toHaveBeenCalledWith('test');

  });
});
