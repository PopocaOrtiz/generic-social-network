import React, { FC } from 'react';

const Search: FC = () => {
    return <section className="navbar-section">
        <div className="input-group input-inline">
            <input className="form-input" type="text" placeholder="search" />
            <button className="btn btn-primary input-group-btn">Search</button>
        </div>
    </section>;
}

export default Search;