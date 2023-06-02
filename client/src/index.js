import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import WelcomePage from './welcome_page';
import PortfolioForm from './portfolio_form';
import PortfolioSummary from './portfolio_summary';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <WelcomePage />,
  }, {
    path: "/form",
    element: <PortfolioForm />
  }, {
    path: "/summary",
    element: <PortfolioSummary />
  }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
