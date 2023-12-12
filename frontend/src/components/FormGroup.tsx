import React, { FC, ReactElement, ReactNode, cloneElement } from 'react';

interface Props {
    children: ReactNode;
    error?: string;
}

const FormGroup: FC<Props> = ({ error = '', children }): ReactElement => {

    const mappedChildren = React.Children.map(children, child => {

        if (!React.isValidElement(child)) {
            return child;
        }

        let newClassName = child.props.className ? child.props.className : '';

        if (child.type === 'label') {
            return cloneElement(child, { className: newClassName + ' form-label' } as any)
        }

        if  (child.props.type === 'submit') {
            return cloneElement(child, { className: newClassName + ' btn'} as any)
        } else if  (child.type === 'input' || child.type === 'textarea') {
            return cloneElement(child, { className: newClassName + ' form-input'} as any)
        }

        if (child.type === 'span') {
            return cloneElement(child, { className: newClassName + ' form-input-hint'} as any)
        }

        return child;
    });

    return (
        <div className={`form-group ${error ? 'has-error' : ''}`}>
            {mappedChildren}
            {error && <span className="form-input-hint">{error}</span>}
        </div>
    );
}

export default FormGroup;