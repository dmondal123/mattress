import axios from "axios";
import { useState } from "react";
import { message } from "antd";
import { useNavigate } from "react-router-dom";
import useSignInAuth from "react-auth-kit/hooks/useSignIn";

import type { AxiosError, AxiosRequestConfig, AxiosResponse } from "axios";

const useSignIn = () => {
  const signIn = useSignInAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const login = (username: string, password: string) => {
    const config: AxiosRequestConfig = {
      baseURL: import.meta.env.VITE_APP_API_URL,
      url: "/auth/login",
      method: "POST",
      data: {
        username,
        password,
      },
    };

    axios(config)
      .then((res: AxiosResponse) => {
        const { token } = res.data;
        if (
          signIn({
            auth: {
              token,
            },
            userState: {
              username,
            },
          })
        ) {
          message.success("Successfully logged in!", 1.5);
          setTimeout(() => {
            navigate("/chat");
          }, 2000);
        }
      })
      .catch((e: AxiosError) => {
        if (e.response && e.response.data && e.response.data) {
          setError((e.response.data as { error: string }).error);
        } else {
          setError("Something went wrong while logging in.");
        }
      });
  };

  return { login, error };
};

export default useSignIn;
