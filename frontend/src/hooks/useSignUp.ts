import axios from "axios";
import useSignIn from "react-auth-kit/hooks/useSignIn";
import { useNavigate } from "react-router-dom";
import { message } from "antd";

import type { AxiosRequestConfig, AxiosResponse } from "axios";

const useSignUp = () => {
  const signIn = useSignIn();
  const navigate = useNavigate();

  const signup = (
    fullName: string,
    username: string,
    email: string,
    password: string
  ) => {
    const config: AxiosRequestConfig = {
      baseURL: import.meta.env.VITE_APP_API_URL,
      url: "/auth/register",
      method: "POST",
      data: {
        fullName,
        username,
        email,
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
          message.success("Registered Successfully!");
          setTimeout(() => {
            navigate("/chat");
          }, 2000);
        }
      })
      .catch((e) => {
        message.error(e?.response?.data?.message || "An error occurred. Please try again.");
        throw e; 
      });
  };

  return { signup };
};

export default useSignUp;
