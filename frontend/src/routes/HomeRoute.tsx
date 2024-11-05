import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

import { Row, Col, Typography, Button, ConfigProvider } from "antd";

const { Title, Text } = Typography;
import LoginForm from "../components/ui/auth/Login";
import SignUpForm from "../components/ui/auth/Signup";

export default function Home() {
  const navigate = useNavigate();
  const location = useLocation();
  return (
    <>
      <Row
        gutter={16}
        className="h-[calc(100vh-120px)] flex items-center overflow-x-hidden"
      >
        <Col span={12} className="bg-white h-full" style={{ padding: 0 }}>
          {/* Center the content vertically */}
          <div className="flex flex-col justify-center h-full p-28">
            <Title level={2} className="text-3xl font-bold">
              Welcome To Your Mattress Finder
            </Title>
            <Text className="block text-lg mt-2">
              Easily discover the ideal mattress for your needs. Ask about
              mattress types, features, and personal preferences to find your
              perfect match.
            </Text>
            {location.pathname === "/" && (
              <div className="flex flex-col ">
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
                    size="large"
                    className="mt-5 rounded-full py-4 px-10 self-start border-none w-3/5"
                    onClick={() => {
                      navigate("/login");
                    }}
                  >
                    LOGIN
                  </Button>
                </ConfigProvider>
                <ConfigProvider
                  theme={{
                    token: {
                      /* here is your global tokens */
                      colorPrimary: "#000000",
                    },
                    components: {
                      Button: {
                        /* here is your component tokens */
                        defaultHoverBg: "#f4f4f5",
                      },
                    },
                  }}
                >
                  <Button
                    type="default"
                    size="large"
                    className="mt-5 rounded-full py-4 px-10 self-start border-[#52525bad] w-3/5"
                    onClick={() => {
                      navigate("/signup");
                    }}
                  >
                    SIGN UP
                  </Button>
                </ConfigProvider>
              </div>
            )}

            {location.pathname === "/login" && <LoginForm />}
            {location.pathname === "/signup" && <SignUpForm />}
          </div>
        </Col>

        <Col
          span={12}
          className="relative h-full overflow-hidden"
          style={{ padding: 0 }}
        >
          <img
            src="https://storage.googleapis.com/conversational_search_gcp_demo2_bucket/images/Nectar_Classic_12_Firm_Hybrid_Mattress/image_1.jpg"
            alt="Mattress"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
            className="w-full h-full"
          />
        </Col>
      </Row>
    </>
  );
}
