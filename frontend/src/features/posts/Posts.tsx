import React, { useEffect, useState } from 'react';

const apiHost = process.env.API_HOST;

export function Posts() {

    const [posts, setPosts] = useState([]);

    useEffect(() => {

        const getPosts = async () => {
            try {

                const response = await fetch(`${apiHost}/posts`);
            
                if (!response.ok) {
                    console.error('Failed to fetch posts');
                    return
                }
    
                const postsData = await response.json();
    
                setPosts(postsData);   

            } catch (error) {
                console.log('Error fetching posts: ', error)
            }
        }

        getPosts();

    }, [])

    return (<>
        <h1>Posts</h1>
        <ul>
            {posts.map(post => (
                <li key={post.id}>
                    {post.content}
                </li>
            ))}
        </ul>
    </>);
}