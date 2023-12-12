import React, { FC, ReactNode } from 'react';

const Search: FC<{children: ReactNode}> = ({ children }) => {
    return <div className="input-group">
        {children}
        <input className="form-input" type="text" placeholder="search posts" />
        <button className="btn btn-primary input-group-btn">
            <i className="icon icon-search mr-2"></i>
            Search
        </button>
    </div>;
}

export default Search;