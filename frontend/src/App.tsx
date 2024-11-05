import RequireAuth from "@auth-kit/react-router/RequireAuth";
import AuthProvider from "react-auth-kit/AuthProvider";
import createStore from "react-auth-kit/createStore";
import { RouterProvider, createBrowserRouter } from "react-router-dom";

import BaseLayout from "./components/ui/Layout";
import Home from "./routes/HomeRoute";
import Chat from "./routes/ChatRoute";

import "./App.css";

const PrivateRoute: React.FC<{ Component: React.ElementType }> = ({
  Component,
}) => {
  return (
    <RequireAuth fallbackPath="/login">
      <Component />
    </RequireAuth>
  );
};

const store = createStore({
  authName: "_auth",
  authType: "cookie",
  cookieDomain: window.location.hostname,
  cookieSecure: true,
});

const router = createBrowserRouter([
  {
    element: <BaseLayout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/login",
        element: <Home />,
      },
      {
        path: "/signup",
        element: <Home />,
      },
      {
        path: "/chat",
        element: <PrivateRoute Component={Chat} />,
      },
    ],
  },
]);

const App = () => {
  return (
    <AuthProvider store={store}>
      <RouterProvider router={router} />
    </AuthProvider>
  );
};

export default App;
