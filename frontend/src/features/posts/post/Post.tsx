import { FC } from 'react';

import { IPost } from './../types';

import { Card, CardHeader, CardMedia, CardContent, CardActions, Avatar, Typography } from '@mui/material';
import { red } from '@mui/material/colors';

const Post: FC<IPost> = (post) => {

    return (
        <Card>
            <CardHeader avatar={<Avatar sx={{ bgcolor: red[500] }} src={post.author.image} alt="Avatar LG"/>}
                title={post.author.full_name}
                subheader={"@" + post.author.username} />
                {/* todo: bookmark icon */}
            {post.image && (
                <CardMedia component="img"
                    image={post.image}
                    alt={post.content} />
            )}
            <CardContent>
                <Typography variant="body2" color="text.secondary">
                    {post.content}
                </Typography>
            </CardContent>
            <CardActions>
                <i className="icon icon-more-vert float-right ml-2"></i>
                <i className="icon icon-message float-right ml-2"></i>
                <i className="icon icon-flag float-right ml-2"></i>
                <button className="btn btn-sm mr-2">
                    <i className="icon icon-arrow-up"></i> 8
                </button>
                <button className="btn btn-sm mr-2">
                    <i className="icon icon-arrow-down"></i> 8
                </button>
            </CardActions>
        </Card>
    );
}

export default Post;