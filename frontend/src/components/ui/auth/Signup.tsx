import { useState } from "react";
import {
  Form,
  Input,
  Button,
  Space,
  message,
  Spin,
  ConfigProvider,
} from "antd";
import {
  UserOutlined,
  LockOutlined,
  IdcardOutlined,
  MailOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import useSignUp from "../../../hooks/useSignUp";

const SignUpForm = () => {
  const [fullName, setFullName] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { signup } = useSignUp();

  const handleSubmit = (values: any) => {
    if (
      !values.username ||
      !values.email ||
      !values.password ||
      !values.fullName
    ) {
      message.error("Please fill in all fields");
      return;
    }
    setLoading(true);
    signup(fullName, username, email, password);
    setLoading(false);
    message.success("Sign Up Successfull!");
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
        name="signup"
        onFinish={handleSubmit}
        layout="vertical"
        initialValues={{ remember: true }}
      >
        <Form.Item
          name="fullName"
          rules={[{ required: true, message: "Please input your Full Name!" }]}
        >
          <Input
            prefix={<IdcardOutlined className="mr-2" />}
            placeholder="Full Name"
            className="p-2"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </Form.Item>
        <Form.Item
          name="username"
          rules={[{ required: true, message: "Please input your Username!" }]}
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
          name="email"
          rules={[
            { required: true, message: "Please input your email!" },
            { type: "email", message: "Please enter a valid email!" },
          ]}
        >
          <Input
            prefix={<MailOutlined className="mr-2" />}
            placeholder="Email"
            className="p-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
              {loading ? <Spin /> : "SIGN UP"}
            </Button>
          </ConfigProvider>
        </Form.Item>
      </Form>
      <div style={{ textAlign: "center" }}>
        <p className="text-base font-normal">
          Already have an account?{" "}
          <a
            className="text-[#ac2b1fde] underline hover:text-[#ac2b1fa3] active:text-[#A52A2A]"
            onClick={() => {
              navigate("/login");
            }}
          >
            Sign in
          </a>
        </p>
      </div>
    </Space>
  );
};

export default SignUpForm;
