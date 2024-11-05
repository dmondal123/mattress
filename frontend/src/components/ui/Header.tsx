import { Layout } from "antd";

const { Header } = Layout;
import { Link } from "react-router-dom";

const CustomHeader = () => {
  return (
    <Header className="bg-[#AC2B1F] flex items-center px-8 h-14">
      <Link to="/">
        <h2
          className="text-white mb-0 text-lg font-bold"
          style={{ fontFamily: "Source Sans 3, sans-serif" }}
        >
          MattressFirm
        </h2>
      </Link>
    </Header>
  );
};

export default CustomHeader;
