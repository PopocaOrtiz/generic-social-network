import { IUser } from '../users/types';

export interface IPost {
    id: string;
    content: string;
    image: string;
    author: IUser;
}