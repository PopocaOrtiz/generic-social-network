import { FC } from 'react';

import { IPost } from './../types';

const Post: FC<IPost> = (post) => {

    return <div className="card mb-2 mt-2">
        {post.image && (
            <div className="card-image">
                <img src={post.image} className="img-responsive" alt={post.content} />
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
    </div>;
}

export default Post;