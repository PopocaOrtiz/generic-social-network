import React from 'react';
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';

import './App.css';

import Posts from './features/posts/Posts';
import Header from './components/Header';
import UsersSignUp from './features/users/register/Register';
import Login from './features/users/login/Login';

const router = createBrowserRouter([
  {
    path: '',
    element: <>
      <Header />
      <Outlet />
    </>,
    children: [
      {
        path: 'posts',
        element: <Posts />
      },
      {
        path: 'sign-up',
        element: <UsersSignUp />
      }
      ,
      {
        path: 'login',
        element: <Login />
      }
    ]
  }
]);

function App() {
  return (<RouterProvider router={router} />);
}

export default App;
