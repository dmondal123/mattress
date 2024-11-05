import { Layout, Row, Col, Typography, Divider } from "antd";

const { Footer } = Layout;
const { Text } = Typography;

import GDlogo from "../../assets/icons/GDlogo.svg";

const CustomFooter = () => {
  return (
    <Footer className="bg-[#F8F7F5] px-8 py-5 fixed bottom-0 w-full h-16 border-t border-gray-300">
      <Row justify="space-between" align="middle" className="font-fira-sans">
        <Col>
          <Row align="middle" gutter={10}>
            <Col>
              <img
                src={GDlogo}
                alt="GDLogo"
                width={25}
                height={25}
                style={{ width: "25px", height: "25px" }}
              />
            </Col>
            <Col>
              <Text className="text-base font-medium">Grid Dynamics</Text>
            </Col>
          </Row>
        </Col>
        <Col>
          <Row align="middle" gutter={16}>
            <Col>
              <a href="#" className="text-sm text-gray-500">
                Help & Feedback
              </a>
            </Col>
            <Col>
              <Divider type="vertical" className="h-6 border-gray-300" />
            </Col>
            <Col>
              <Text className="text-sm text-gray-500">
                © Grid Dynamics 2024
              </Text>
            </Col>
          </Row>
        </Col>
      </Row>
    </Footer>
  );
};

export default CustomFooter;
