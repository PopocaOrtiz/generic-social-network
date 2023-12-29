import { fetchData, createData } from '../../app/api';

export function fetchPosts(query?: string) {
    let endpoint = `posts/`

    if (query) {
        endpoint += `?search=${query}`
    }

    return fetchData(endpoint);
}

export function createPost(post: {content: string, image_file: File | null}) {
    return createData(`posts/`, post);
}