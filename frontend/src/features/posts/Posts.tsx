import React, { useEffect, useState, FC } from 'react';

import { IPost } from './types';
import { fetchPosts } from './api';
import Post from './post/Post';
import Search from './../../components/Search';
import Loading from './../../components/Loading'
import PostForm from './post-form/PostForm';

const Posts: FC = () => {

    const [posts, setPosts] = useState<IPost[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [showPostForm, setShowPostForm] = useState<boolean>(false);
    const [suggestions, setSuggestions] = useState<Array<string>>([]);

    async function getPosts (){

        setLoading(true);

        try {
            const response = await fetchPosts();

            if (!response.ok) {
                throw Error('error fetching posts');
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

    const postCreateHandler = (post: IPost) => {
        setPosts(prevPosts => [post, ...prevPosts]);
        setShowPostForm(false);
    }

    const changedQuery = (query: string) => {
        console.log('searching for', query);
        setSuggestions(current => [...current, query]);
    }

    return (<>
        <h1>Posts</h1>
        <Search onChangeQuery={changedQuery} suggestions={suggestions}>
            {!showPostForm && <button onClick={() => setShowPostForm(true)} className="btn input-group-btn">
                <i className="icon icon-plus mr-2"></i>
                New post
            </button>}
        </Search>
        <br />
        <Loading show={loading} testid="loading-search-posts"/>
        {showPostForm && (<>
            <div className="card">
                <div className="card-body">
                    <PostForm onPostCreated={postCreateHandler} />
                </div>
            </div>
            <br />
        </>)}
        {posts.map(post => (<div key={post.id}>
            <Post {...post}/>
            <br />
        </div>))}
    </>);
}

export default Posts;
