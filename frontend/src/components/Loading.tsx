import React, { FC } from 'react';

const Loading: FC<{show: boolean}> = ({ show, testid }) => {

    if (show) {
        return (<div className="loading loading-lg" 
          role="progressbar" 
          data-testid={testid}></div>);
    }

    return <></>;
}

export default Loading;
