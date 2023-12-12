export interface IUser {
    full_name: string;
    email: string;
    username: string;
    image: string;
}

export interface IUserCreate {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
}