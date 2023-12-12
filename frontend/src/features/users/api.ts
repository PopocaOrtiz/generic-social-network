import { IUser } from "./types";

const apiHost = process.env.REACT_API_HOST;

export function registerUser(user: IUser) {
    const url = `${apiHost}/users/register`
    return fetch(url, {
        method: 'POST', 
        body: JSON.stringify(user),
        headers: {
            "Content-Type": "application/json"
        }
    })
}

export function login(email: string, password: string) {
    const url = `${apiHost}/users/token`;
    return fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            email, password
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
}