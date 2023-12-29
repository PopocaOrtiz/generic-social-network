import { render, fireEvent, act } from '@testing-library/react';

import Login from './Login';

jest.mock('../api', () => ({
    login: jest.fn().mockResolvedValue({ json: () => {token: 't' }})
}));

jest.mock('react-redux', () => ({
    useDispatch: jest.fn().mockReturnValue(() => null)
}));

jest.mock('react-router-dom', () => ({
    useNavigate: jest.fn().mockReturnValue(() => null)
}));

describe('<Login />', () => {

    it('should display success message when login is successful', async () => {

        const { findByTestId } = render(<Login />);

        const emailInput = await findByTestId('email-input');
        const passwordInput = await findByTestId('password-input');
        const button = await findByTestId('submit-button');

        fireEvent.change(emailInput, { target: { value: 'e@m.a'}});
        fireEvent.change(passwordInput, { target: { value: 'p'}});

        await act(async() => {
            fireEvent.click(button);
        });

    });

});