import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface LoginState {
    status: 'login' | 'logout'
}

const initialState: LoginState = {
    status: 'logout'
}

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        login: (state) => {
            state.status = 'login';
        },
        logout: (state) => {
            state.status = 'logout';
        }
    }
})

export const { login, logout } = userSlice.actions;
export default userSlice.reducer;