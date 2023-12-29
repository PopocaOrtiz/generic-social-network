import { render, fireEvent } from '@testing-library/react';

import Register from "./Register";

describe('<Users/Register>', () => {
    test('submit button is disabled', () => {

        const { findByTestId } = render(<Register />);

        const buttonElement = findByTestId('submit-button');

        fireEvent.click(buttonElement);
    });
});