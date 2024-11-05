import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Form,
  Input,
  Button,
  Space,
  message,
  Spin,
  ConfigProvider,
  Typography,
} from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import useSignIn from "../../../hooks/useSignIn";

const LoginForm = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { login, error } = useSignIn();
  const [form] = Form.useForm();

  const handleSubmit = (values: any) => {
    if (!values.username || !values.password) {
      message.error("Please fill in all fields");
      return;
    }
    setLoading(true);
    login(username, password);
    setLoading(false);
  };

  return (
    <Space
      direction="vertical"
      size="middle"
      style={{ width: "70%" }}
      className="mt-5"
    >
      <Form
        form={form}
        name="login"
        onFinish={handleSubmit}
        layout="vertical"
        initialValues={{ remember: true }}
      >
        <Form.Item
          name="username"
          rules={[{ required: true, message: "Please input your username!" }]}
        >
          <Input
            prefix={<UserOutlined className="mr-2" />}
            placeholder="Username"
            className="p-2"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[{ required: true, message: "Please input your password!" }]}
        >
          <Input.Password
            prefix={<LockOutlined className="mr-2" />}
            placeholder="Password"
            className="p-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Item>
        <Form.Item>
          <ConfigProvider
            theme={{
              token: {
                /* here is your global tokens */
                colorPrimary: "#A52A2A",
              },
            }}
          >
            <Button
              type="primary"
              htmlType="submit"
              block
              loading={loading}
              size="large"
              className="mt-2 rounded-full py-4 px-10 self-start border-none w-full"
            >
              {loading ? <Spin /> : "LOG IN"}
            </Button>
          </ConfigProvider>
          {error && (
            <Typography.Paragraph
              type="danger"
              style={{
                width: "100%",
                margin: "0.5rem 0",
                textAlign: "center",
              }}
            >
              {error.toString()}
            </Typography.Paragraph>
          )}
        </Form.Item>
      </Form>
      <div style={{ textAlign: "center" }}>
        <p className="text-base font-normal">
          Don't have an account?{" "}
          <a
            className="text-[#ac2b1fde] underline hover:text-[#ac2b1fa3] active:text-[#A52A2A]"
            onClick={() => {
              navigate("/signup");
            }}
          >
            Sign up
          </a>
        </p>
      </div>
    </Space>
  );
};

export default LoginForm;
