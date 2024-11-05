import { Dispatch, SetStateAction, useRef, useEffect } from "react";
import useChatStore from "../../store/chatStore";
import { Typewriter } from "react-simple-typewriter";
import { Card, Avatar, Button, Divider, ConfigProvider } from "antd";
import { UserOutlined, RobotOutlined } from "@ant-design/icons";

import ChatInput from "./ChatInput";
import ChatLoader from "./ChatLoader";

type ChatSectionProps = {
  loading: boolean;
  handleSendMessage: (message: string) => void;
  setLoading: Dispatch<SetStateAction<boolean>>;
};

const ChatSection: React.FC<ChatSectionProps> = ({
  loading,
  handleSendMessage,
  setLoading,
}: ChatSectionProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);
  const { chatObjects } = useChatStore();

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [chatObjects, loading]);

  const listChatMessages: JSX.Element[] = chatObjects.map((object, index) => {
    if (typeof object === "object" && object.displayUserName === "User") {
      return (
        <UserMessage
          key={index}
          sender={object.displayUserName}
          time={new Date().toLocaleString("en-US", {
            hour: "numeric",
            minute: "numeric",
            hour12: true,
          })}
          message={object.body}
        />
      );
    } else {
      return (
        <MattressAIMessage
          sender="MattressAI"
          time={new Date().toLocaleString("en-US", {
            hour: "numeric",
            minute: "numeric",
            hour12: true,
          })}
          message={typeof object === "object" ? object.body : ""}
          buttons={typeof object === "object" ? object.options : null}
        />
      );
    }
  });
  return (
    <div className="flex flex-col h-[96%]">
      <div
        className="flex-grow flex flex-col items-start w-full space-y-4 px-2 h-full overflow-y-auto transition-all scrollbar-custom"
        ref={scrollRef}
      >
        {listChatMessages}
        {loading && <ChatLoader />}
        <div className="pt-8 pb-4 px-0"></div>
      </div>

      <div className="sticky bottom-0 bg-white p-4 shadow-lg">
        <ChatInput
          handleSendMessage={handleSendMessage}
          setLoading={setLoading}
        />
      </div>
    </div>
  );
};

function MattressAIMessage({ sender, time, message, buttons }: any) {
  return (
    <div className="flex items-start self-start w-2/3">
      <Avatar
        icon={<RobotOutlined className="bg-transparent text-[#ac2b1f]" />}
        className="mr-1 flex-shrink-0 mt-auto bg-white border"
      />
      <ConfigProvider
        theme={{
          token: {
            paddingLG: 12,
          },
        }}
      >
        <Card className=" bg-[#8080804d] rounded-tl-xl rounded-tr-xl rounded-bl-none rounded-br-xl pl-2">
          <div className="flex gap-2">
            <div className="flex flex-col items-start">
              <div className="flex items-center gap-1 mb-2">
                <span className="font-medium text-sm text-[#19213D]">
                  {sender}
                </span>
                <Divider type="vertical" />
                <span className="text-[#666F8D] text-xs">{time}</span>
              </div>
              <div className="flex flex-col items-start">
                {/* Typewriter effect without cursor */}
                <Typewriter
                  words={[message]}
                  loop={1}
                  typeSpeed={20}
                  deleteSpeed={0}
                  cursor={false} // Disable cursor
                />

                {buttons && (
                  <div className="mt-2 flex flex-col self-start">
                    {buttons.map((btn: string, idx: number) => (
                      <ConfigProvider key={idx}>
                        <Button
                          color="default"
                          className="mb-2 border border-[#AC2B1F] rounded-full py-2 px-4 text-black hover:text-black"
                          onClick={() => {}}
                        >
                          {btn}
                        </Button>
                      </ConfigProvider>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </Card>
      </ConfigProvider>
    </div>
  );
}

function UserMessage({ sender, time, message }: any) {
  return (
    <div className="flex items-start self-end">
      <div className="bg-[#ac2b1f4c] p-4 rounded-tl-xl rounded-tr-xl rounded-bl-xl rounded-br-none">
        <div className="flex items-center gap-1">
          <span className="font-bold">{sender}</span>
          <Divider type="vertical" />
          <span className=" text-xs ">{time}</span>
        </div>
        <p className="mb-0">{message}</p>
      </div>
      <Avatar
        icon={<UserOutlined className="text-black" />}
        className="ml-1 self-end bg-white"
      />
    </div>
  );
}

export default ChatSection;
