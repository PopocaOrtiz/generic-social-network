import React, { useEffect, useState } from 'react';

import { IPost } from './types';

const apiHost = process.env.REACT_APP_API_HOST;

export function Posts() {

    const [posts, setPosts] = useState<IPost[]>([]);
    const [loading, setLoading] = useState<boolean>(false);


    async function getPosts (){

        setLoading(true);

        try {
            const response = await fetch(`${apiHost}/posts/`);

            if (!response.ok) {
                throw('error fetching posts');
            }
    
            const responseData = await response.json();
    
            setPosts(responseData);   
        } catch (error) {
            throw (error);
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
        <section className="navbar-section float-right">
            <div className="input-group input-inline">
                <input className="form-input" type="text" placeholder="search" />
                <button className="btn btn-primary input-group-btn">Search</button>
            </div>
        </section>
        <h1>
            Posts
        </h1>
        {loading && <div className="loading loading-lg"></div>}
        <div className="columns">
            <div className="column col-7 col-mx-auto">
                {posts.map(post => (
                    <div className="card mb-2 mt-2" key={post.id}>
                        {post.image && (
                            <div className="card-image">
                                <img src={post.image} className="img-responsive" />
                            </div>
                        )}
                        <div className="card-header">
                            <div className="card-title h5">{post.author.first_name}</div>
                        </div>
                        <div className="card-body">
                            {post.content}
                        </div>
                        <div className="card-footer">
                            <button className="btn btn-primary">react</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    </>);
}