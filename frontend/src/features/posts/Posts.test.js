import { render, screen, fireEvent } from '@testing-library/react';

import Posts from './Posts';

describe('<Posts />', () => {
  test('renders Posts component', () => {

    render(<Posts />);

    const h1Element = screen.getByText(/Posts/i);
    const buttonElement = screen.getByText(/New post/i);
    const loading = screen.getByRole("progressbar");

    expect(h1Element).toBeInTheDocument();
    expect(buttonElement).toBeInTheDocument();
    expect(loading).toBeInTheDocument();
  });

  test('shows the new post form', () => {
    render(<Posts />);
    const buttonElement = screen.getByText(/New post/i);
    fireEvent.click(buttonElement);

    const formElement = screen.getByText(/New post/i);
    expect(formElement).toBeInTheDocument();
  });

  test('searches posts', () => {
    const { findByTestId } = render(<Posts />);

    const inputElement = screen.getByRole("textbox");
    const buttonElement = screen.getByRole("button", {name: /search/i});

    fireEvent.change(inputElement, {target: {value: "Hello"}});
    fireEvent.click(buttonElement);

    const loading = getByTestId("loadin-search-posts"); 
    expect(loading).toBeInTheDocument();
  });
});
