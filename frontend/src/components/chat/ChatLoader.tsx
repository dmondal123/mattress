import { Avatar } from "antd";
import { RobotOutlined } from "@ant-design/icons";
import BouncingDotsLoader from "../ui/BouncingDotsLoader";

const ChatLoader = () => {
  return (
    <div className="flex items-center mb-4">
      <Avatar
        icon={<RobotOutlined className="bg-transparent text-[#ac2b1f] p-2" />}
        className="mr-3 flex-shrink-0 mt-auto bg-white border"
      />
      <p
        style={{
          width: "fit-content",
          padding: "0.6rem 0.8rem",
          backgroundColor: "#8080804d",
          borderRadius: "10px 10px 10px 0",
          display: "flex",
          gap: "2px",
        }}
      >
        {/* <ThreeDots
          visible={true}
          height="10"
          width="50"
          color="black"
          radius="7"
          ariaLabel="three-dots-loading"
          wrapperStyle={{}}
          wrapperClass=""
        /> */}
        <BouncingDotsLoader />
      </p>
    </div>
  );
};

export default ChatLoader;
