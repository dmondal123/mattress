"use client";
import { PlusOutlined } from "@ant-design/icons";
import { Button, Layout, ConfigProvider } from "antd";
import { useState } from "react";
import Sidebar from "./Sidebar";
import { Outlet, useLocation } from "react-router-dom";
import CustomHeader from "./Header";
import CustomFooter from "./Footer";
import useChatStore, {
  useProductStore,
  useProgressStore,
} from "../../store/chatStore";

const { Sider, Content } = Layout;

const BaseLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState<boolean>(true);
  const { clearChatObjects } = useChatStore();
  const { clearProductObjects } = useProductStore();
  const { resetProgress } = useProgressStore();
  const location = useLocation();

  return (
    <Layout style={{ height: "100vh" }}>
      <CustomHeader />

      <Layout>
        {location.pathname === "/chat" && (
          <ConfigProvider
            theme={{
              components: {
                Layout: {
                  /* here is your component tokens */
                },
              },
            }}
          >
            <Sider
              collapsible
              collapsed={collapsed}
              onCollapse={(value) => setCollapsed(value)}
              theme="light"
            >
              <Sidebar />

              <div className="flex flex-col mt-[70vh] justify-end items-center">
                <ConfigProvider
                  theme={{
                    token: {
                      colorPrimary: "#A52A2A",
                    },
                  }}
                >
                  <Button
                    type="primary"
                    size={collapsed ? "middle" : "small"}
                    className={`mb-2  border-none ${
                      collapsed ? "" : "rounded-full py-4 px-4"
                    }`}
                    icon={<PlusOutlined />}
                    iconPosition="end"
                    onClick={() => {
                      clearChatObjects();
                      clearProductObjects();
                      resetProgress();
                      window.location.reload();
                    }}
                  >
                    {collapsed ? "" : "Start New Chat"}
                  </Button>
                </ConfigProvider>
              </div>
            </Sider>
          </ConfigProvider>
        )}
        <Content style={{ overflow: "scroll" }}>
          <Outlet />
        </Content>
      </Layout>
      {location.pathname !== "/chat" && <CustomFooter />}
    </Layout>
  );
};

export default BaseLayout;
