interface IUser {
    first_name: string;
}

export interface IPost {
    id: string;
    content: string;
    image: string;
    author: IUser;
}