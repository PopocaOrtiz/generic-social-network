import { useEffect, useState, FC, useCallback } from 'react';

import { Fab, LinearProgress, Typography, TextField, Autocomplete, Alert } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';

import { IPost } from './types';
import { fetchPosts } from './api';
import Post from './post/Post';
import PostForm from './post-form/PostForm';

const Posts: FC = () => {

    const [posts, setPosts] = useState<IPost[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [showPostForm, setShowPostForm] = useState<boolean>(false);
    const [suggestions, setSuggestions] = useState<Array<string>>([]);
    const [error, setError] = useState<string>();

    const [searchQuery, setSearchQuery] = useState<string>('');

    const getPosts = useCallback(async (query?: string) => {

        setLoading(true);
        setError('');

        try {
            const response = await fetchPosts(query);

            if (!response.ok) {
                throw Error('error fetching posts');
            }
    
            const responseData = await response.json();
    
            setPosts(responseData);   
        } catch (error) {
            setError('error fetching posts');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        getPosts();
    }, [])

    const postCreateHandler = (post: IPost) => {
        setPosts(prevPosts => [post, ...prevPosts]);
        setShowPostForm(false);
    }

    const onChangeHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
        getPosts(event.target.value.trim());
    }

    return (<>
        <Typography variant="h4">Posts</Typography>
        <Fab aria-label="add-post" 
            color="primary"
            sx={{ position: 'absolute', bottom: 16, right: 16 }}
            onClick={() => setShowPostForm(true)}>
            <AddIcon />
        </Fab>
        <TextField label="search posts"
            placeholder="search by content, author, etc.."
            fullWidth
            value={searchQuery}
            onChange={onChangeHandler}
            variant="standard"
            margin="normal"
            inputProps={{ "data-testid": "search-posts-input" }}
            />
        <br />
        {loading && <LinearProgress />}
        {error && <Alert severity="error">{error}</Alert>}
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
