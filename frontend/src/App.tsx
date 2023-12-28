import React from 'react';
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';

import './App.css';

import Posts from './features/posts/Posts';
import Header from './components/Header';
import UsersSignUp from './features/users/register/Register';
import Login from './features/users/login/Login';

import { Container, Box } from '@mui/material';

const router = createBrowserRouter([
  {
    path: '',
    element: <>
      <Header />
      <Container component="main" maxWidth="sm">
        <Box
            sx={{
              marginTop: 10,
            }}
          >
          <Outlet />
        </Box>
      </Container>
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
