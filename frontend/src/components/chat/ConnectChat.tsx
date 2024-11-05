import { message } from "antd";
import { MutableRefObject, useEffect } from "react";
import useChatStore from "../../store/chatStore";
import { v4 as uuidv4 } from "uuid";

interface ConnectChatProps {
  websocket: MutableRefObject<WebSocket | null>;
}

const ConnectChat: React.FC<ConnectChatProps> = ({
  websocket,
}: ConnectChatProps) => {
  const URL = import.meta.env.VITE_APP_API_URL?.replaceAll(/^.*\/\//g, "ws://");
  const [messageApi, contextHolder] = message.useMessage();
  const { addSession } = useChatStore();
  let retries = 2;

  const connectingMessage = () => {
    messageApi.loading({
      type: "loading",
      content: "Connecting...",
      duration: 0,
      key: "updatable",
    });
  };

  const connectedMessage = () => {
    messageApi.success({
      type: "success",
      content: "Ready to Chat",
      duration: 3,
      key: "updatable",
    });
  };

  const connectionFailedMessage = () => {
    messageApi.error({
      type: "error",
      content: "Connection failed",
      duration: 3,
      onClose: handleRetryConnection,
      key: "updatable",
    });
  };

  const retryConnectionMessage = () => {
    messageApi.loading({
      type: "loading",
      content: "Reconnecting",
      duration: 6,
      onClose: connectionFailedMessage,
      key: "updatable",
    });
  };

  const handleRetryConnection = () => {
    if (--retries === 0) return;
    const sessionId = uuidv4();
    addSession(sessionId);
    websocket.current = new WebSocket(`${URL}ws?sessionId=${sessionId}`);
    retryConnectionMessage();
  };

  useEffect(() => {
    const sessionId = uuidv4();
    addSession(sessionId);
    connectingMessage();
    websocket.current = new WebSocket(`${URL}ws?sessionId=${sessionId}`);
  }, [websocket]);

  useEffect(() => {
    if (websocket.current !== null) {
      websocket.current.onopen = () => {
        setTimeout(() => connectedMessage(), 100);
      };
    }
    if (websocket.current !== null) {
      websocket.current.onclose = () => {
        connectionFailedMessage();
      };
    }
  }, [websocket]);

  return <>{contextHolder}</>;
};

export default ConnectChat;
