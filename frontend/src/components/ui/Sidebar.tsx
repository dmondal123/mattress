import { useState } from "react";
import {
  MessageOutlined,
  LogoutOutlined,
} from "@ant-design/icons";
import { Menu, MenuProps, ConfigProvider, Modal } from "antd";
import { useNavigate } from "react-router-dom";
import useSignOut from "react-auth-kit/hooks/useSignOut";

type MenuItem = Required<MenuProps>["items"][number];

function getItem(
  label: React.ReactNode,
  key: React.Key,
  icon?: React.ReactNode,
  children?: MenuItem[]
): MenuItem {
  return {
    key,
    icon,
    children,
    label,
  } as MenuItem;
}

const items: MenuItem[] = [
  getItem(
    <span className="font-semibold">Main Chat</span>,
    "/chat",
    <MessageOutlined />
  ),
  // getItem(
  //   <span className="font-semibold">Chat History</span>,
  //   "/chat-history",
  //   <HistoryOutlined />,
  //   [
  //     getItem("Chat 1", "/chat-1"),
  //     getItem("Chat 2", "/chat-2"),
  //     getItem("Chat 3", "/chat-3"),
  //   ]
  // ),
  getItem(
    <span className="font-semibold">Sign Out</span>,
    "/signout",
    <LogoutOutlined />
  ),
];

const Sidebar: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const signOut = useSignOut();
  const navigate = useNavigate();
  const handleMenuSelect: MenuProps["onSelect"] = ({ key }) => {
    if (key === "/signout") {
      setIsModalOpen(true);
    } else navigate(key);
  };

  return (
    <>
      <ConfigProvider
        theme={{
          components: {
            Menu: {
              /* here is your component tokens */
              itemSelectedBg: "#AC2B1F33",
              itemSelectedColor: "#000",
              itemActiveBg: "#AC2B1F33",
            },
          },
        }}
      >
        <Menu
          className="mt-2"
          defaultSelectedKeys={["/chat"]}
          mode="inline"
          theme="light"
          items={items}
          onSelect={handleMenuSelect}
        />
      </ConfigProvider>
      <Modal
        title="Are you sure you want to Sign Out?"
        open={isModalOpen}
        closeIcon={null}
        okText="Sign Out"
        onOk={() => {
          signOut();
          navigate("/login");
          setIsModalOpen(false);
        }}
        onCancel={() => {
          setIsModalOpen(false);
        }}
        okButtonProps={{
          style: {
            backgroundColor: "#A52A2A", // OK button background color
            color: "#fff", // OK button text color
          },
          onMouseEnter: (e) =>
            (e.currentTarget.style.backgroundColor = "#d04949"),
          onMouseLeave: (e) =>
            (e.currentTarget.style.backgroundColor = "#A52A2A"),
        }}
      ></Modal>
    </>
  );
};

export default Sidebar;
