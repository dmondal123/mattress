import axios from "axios";
import { MutableRefObject, useEffect, useRef, useState } from "react";
import useChatStore, { useProductStore } from "../store/chatStore";
import { Layout, Splitter, Divider, ConfigProvider } from "antd";
import ChatSection from "../components/chat/ChatSection";
// import ChatProgress from "../components/chat/ChatProgress";
import ConnectChat from "../components/chat/ConnectChat";
import ProductRecommendations from "../components/chat/ProductRecommendations";

import { ChatMessage } from "../types/ChatMessage";
import { ChatMessageSendType } from "../types/ChatMessageSendType";
import { ChatMessageReceiveType } from "../types/ChatMessageReceiveType";
import { ProductType } from "../types/ProductType";
// import { ProductType } from "../types/ProductType";

const { Content } = Layout;

interface FinalOutputResponse {
  data?: any; // Replace `any` with the expected response data structure
  error?: string;
}

const Chat: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const websocket: MutableRefObject<WebSocket | null> = useRef<WebSocket>(null);
  const { sessionId, addChatObject } = useChatStore();
  const { addProductObject } = useProductStore();
  const [sizes, setSizes] = useState<(number | string)[]>(["70%", "30%"]);

  const handleSendMessage = (inputMessageArg: string) => {
    const inputMessage = inputMessageArg.slice();
    inputMessage.trim();
    if (inputMessage.trim() === "") {
      alert("Please enter a valid message!");
      return;
    }
    setTimeout(() => {
      setLoading(true);
    }, 500);
    const newChatMessage: ChatMessage = {
      sender: { name: "User" },
      timestamp: new Date().toISOString(),
      body: inputMessage,
      displayUserName: "User",
    };
    const newChatMessageSend: ChatMessageSendType = {
      message: inputMessage,
    };
    addChatObject(newChatMessage);
    websocket.current?.send(JSON.stringify(newChatMessageSend));
  };

  async function getFinalOutput(
    sessionId: string
  ): Promise<FinalOutputResponse> {
    try {
      const response = await axios.get<FinalOutputResponse>(
        `${import.meta.env.VITE_APP_API_URL}final_output`,
        {
          params: {
            session_id: sessionId,
          },
        }
      );
      console.log("Final Response Data:", response.data);
      return response.data;
    } catch (error: any) {
      console.error(
        "Error fetching final output:",
        error.response ? error.response.data : error.message
      );
      return { error: error.message };
    }
  }

  useEffect(() => {
    if (websocket.current !== null) {
      websocket.current.onmessage = (event: WebSocketEventMap["message"]) => {
        const handleMessage = async () => {
          setLoading(false);
          console.log("Chat response: ", event.data);
          const response = JSON.parse(event.data);

          const newReceivedMessage: ChatMessageReceiveType = {
            message: response.messages[0].text,
            displayUserName: "Mattress AI",
            options: response?.options,
          };
          const newChatMessage: ChatMessage = {
            body: newReceivedMessage.message,
            sender: { name: "MattressAI" },
            timestamp: Date.now().toString(),
            displayUserName: "MattressAI",
            options: response.options,
          };

          console.log("SESSIONID:", sessionId);

          addChatObject(newChatMessage);

          // Check if there are links before calling getFinalOutput
          if (
            response.messages[0].links &&
            response.messages[0].links.length > 0
          ) {
            try {
              const finalOutput = (await getFinalOutput(sessionId)).data;
              const newProduct: ProductType = {
                name: finalOutput.name,
                images: finalOutput.images,
                size: finalOutput.size,
                comfort: finalOutput.comfort,
                best_for: finalOutput.best_for,
                mattress_type: finalOutput.mattress_type,
                cooling_technology: finalOutput.cooling_technology,
                motion_separation: finalOutput.motion_separation,
                pressure_relief: finalOutput.pressure_relief,
                support: finalOutput.support,
                adjustable_base_friendly: finalOutput.adjustable_base_friendly,
                breathable: finalOutput.breathable,

                num_reviews: finalOutput.num_reviews,
                current_price: finalOutput.current_price,
                rating: finalOutput.rating,
                mattress_in_a_box: finalOutput.mattress_in_a_box,
                height: finalOutput.height,
              };
              addProductObject(newProduct);
              console.log("Final Output:", finalOutput);
            } catch (error) {
              console.error("Error during final output API call:", error);
            }
          }
        };

        handleMessage();
      };
    }
  }, [sessionId]);

  return (
    <div className="bg-[#f3f5ff] p-4 rounded-sm h-full">
      <ConnectChat websocket={websocket} />
      <Layout className="h-full py-4 pl-6 pr-2 rounded-sm bg-white mb-4">
        <h1 className="text-2xl font-bold text-black mb-3">
          Discover Your Ideal Mattress
        </h1>
        <p className="text-gray-600 mb-0">
          We're here to help you find exactly what you need.
        </p>
        <Content className="flex mt-4">
          <Splitter onResize={setSizes}>
            <Splitter.Panel size={sizes[0]} min="30%" max="70%">
              <div className="relative mr-6 h-full overflow-hidden">
                <ConfigProvider
                  theme={{
                    token: {
                      colorText: "#666F8D",
                      fontSize: 12,
                    },
                  }}
                >
                  <Divider style={{ marginTop: "0.2rem" }}>
                    Today 4:32 PM
                  </Divider>
                </ConfigProvider>

                <ChatSection
                  handleSendMessage={handleSendMessage}
                  loading={loading}
                  setLoading={setLoading}
                />
              </div>
            </Splitter.Panel>
            <Splitter.Panel size={sizes[1]}>
              <div className="pl-8 h-full overflow-hidden">
                {/* <ChatProgress /> */}
                <ProductRecommendations />
              </div>
            </Splitter.Panel>
          </Splitter>
        </Content>
      </Layout>
      {/* <div className="bg-[#EED5D2] py-4 px-6 flex justify-end border-t border-t-[#D9D9D9]">
        <div className="space-x-4">
          <ConfigProvider
            theme={{
              token: {
                colorPrimary: "#A52A2A",
              },
            }}
          >
            <Button
              className="border-black text-black rounded-full"
              icon={<CloseOutlined />}
              iconPosition="end"
            >
              Cancel
            </Button>
          </ConfigProvider>

          <ConfigProvider
            theme={{
              token: {
                colorPrimary: "#A52A2A",
              },
            }}
          >
            <Button
              type="primary"
              className="rounded-full"
              icon={<ArrowRightOutlined />}
              iconPosition="end"
            >
              Continue
            </Button>
          </ConfigProvider>
        </div>
      </div> */}
    </div>
  );
};

export default Chat;
