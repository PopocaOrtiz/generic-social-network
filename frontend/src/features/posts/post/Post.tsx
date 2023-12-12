import { FC } from 'react';

import { IPost } from './../types';

const Post: FC<IPost> = (post) => {

    return <div className="card">
        <div className="card-header">
            <i className="icon icon-bookmark float-right"></i>
            <figure className="avatar mr-2">
                <img src={post.author.image} alt="Avatar LG" />    
            </figure>
            <div className="card-title h5 d-inline">
                {post.author.full_name}
                <span className="card-subtitle text-gray ml-2 h6">@{post.author.username}</span>
            </div>
        </div>
        {post.image && (
            <div className="card-image">
                <img src={post.image} className="p-centered" 
                    style={{maxHeight: '300px'}}    
                    alt={post.content} />
            </div>
        )}
        <div className="card-body">
            {post.content}
        </div>
        <div className="card-footer">
            
            <i className="icon icon-more-vert float-right ml-2"></i>
            <i className="icon icon-message float-right ml-2"></i>
            <i className="icon icon-flag float-right ml-2"></i>

            <button className="btn btn-sm mr-2">
                <i className="icon icon-arrow-up"></i> 8
            </button>
            <button className="btn btn-sm mr-2">
                <i className="icon icon-arrow-down"></i> 8
            </button>
        </div>
    </div>;
}

export default Post;