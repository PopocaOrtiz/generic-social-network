import { fetchData, createData } from '../../app/api';

export function fetchPosts() {
    return fetchData(`posts/`);
}

export function createPost(post: {content: string, image_file: File | null}) {
    return createData(`posts/`, post);
}