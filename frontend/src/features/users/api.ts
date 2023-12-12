import { IUserCreate } from "./types";

import { createData } from '../../app/api';

export function registerUser(user: IUserCreate) {
    return createData('users/create/', user);
}

export function login(email: string, password: string) {
    return createData('users/token/', {email, password});
}