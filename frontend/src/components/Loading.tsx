import React, { FC } from 'react';

const Loading: FC<{show: boolean}> = ({ show }) => {

    if (show) {
        return (<div className="loading loading-lg" 
          role="progressbar"></div>);
    }

    return <></>;
}

export default Loading;
