import React, { FC, ReactNode, useEffect, useState } from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

interface ISearchProps {
    children: React.ReactNode;
    onChangeQuery: (query: string) => void;
    suggestions: Array<React.ReactNode>;
}

const Search: FC<ISearchProps> = ({ children, onChangeQuery, suggestions }) => {

    const [query, setQuery] = useState<string>('');

    useEffect(() => {
        const timeout = setTimeout(() => {
            onChangeQuery(query);
        }, 300)

        return () => clearTimeout(timeout);
    }, [query])

    const changeHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
        setQuery(event.target.value);
    }

    return (
        <>
            <Autocomplete freeSolo
                options={suggestions}
                renderInput={(params) => (
                    <TextField {...params}
                        label="search posts"
                        variant="standard"
                        margin="normal"
                        fullWidth
                        value={query}
                        onChange={changeHandler}
                    ></TextField>
            )}/>
        </>
    );
}

export default Search;
