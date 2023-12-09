import React, { useEffect, useState, FC } from 'react';

import { IPost } from './types';
import Post from './post/Post';
import Search from './../../components/Search';
import Loading from './../../components/Loading'

const apiHost = process.env.REACT_APP_API_HOST;

const Posts: FC = () => {

    const [posts, setPosts] = useState<IPost[]>([]);
    const [loading, setLoading] = useState<boolean>(false);


    async function getPosts (){

        setLoading(true);

        try {
            const response = await fetch(`${apiHost}posts/`);

            if (!response.ok) {
                throw('error fetching posts');
            }
    
            const responseData = await response.json();
    
            setPosts(responseData);   
        } catch (error) {
            // throw (error);
            console.log('error fetching posts', error);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        getPosts();
    }, [])

    const clickHandler = () => {
        getPosts();
    }

    return (<>
        <h1>Posts</h1>
        <Search />
        <Loading show={loading} />
        <div className="columns">
            <div className="column">
                {posts.map(post => <Post {...post} key={post.id} />)}
            </div>
        </div>
    </>);
}

export default Posts;