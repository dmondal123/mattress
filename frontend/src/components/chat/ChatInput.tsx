import { Input, Button, Tooltip, Divider, ConfigProvider } from "antd";
import { StopOutlined, SendOutlined } from "@ant-design/icons";
import {
  useState,
  ChangeEvent,
  KeyboardEvent,
  Dispatch,
  SetStateAction,
} from "react";
import useChatStore, {
  useProductStore,
  useProgressStore,
} from "../../store/chatStore";

const mattressData: string[] = [
  "Memory",
  "Foam",
  "Mattress",
  "Memory",
  "Foam",
  "Mattress",
  "Spring",
  "Mattress",
  "Hybrid",
  "Mattress",
  "Latex",
  "Mattress",
  "Orthopedic",
  "Mattress",
  "Cooling",
  "Gel",
  "Mattress",
  "Pillow",
  "Top",
  "Mattress",
  "Medium",
  "Euro",
  "Pillow",
  "Top",
  "Mattress",
  "Medium",
  "Mattress",
  "Slumber",
  "Cushion",
  "Firm",
  "Mattress",
  "Extra",
  "Firm",
  "Mattress",
  "Plush",
  "Mattress",
  "Firm",
  "Euro",
  "Pillow",
  "Top",
  "Mattress",
  "Medium",
  "Firm",
  "Cooling",
  "Hybrid",
  "Mattress",
  "Firm",
  "Euro",
  "Pillow",
  "Top",
  "Mattress",
  "Nurture",
  "Night",
  "Plush",
  "Mattress",
  "Oasis",
  "Sleep",
  "Pillow",
  "Top",
  "Mattress",
  "Cushion",
  "Firm",
  "Memory",
  "Foam",
  "Mattress",
  "Plush",
  "Euro",
  "Pillow",
  "Top",
  "Mattress",
  "Pillow",
  "Top",
  "Mattress",
  "Adjustable",
  "Firmness",
  "Mattress",
  "Ultimate",
  "Comfort",
  "Memory",
  "Foam",
  "Mattress",
  "Breathable",
  "Gel",
  "Memory",
  "Foam",
  "Mattress",
  "Eco-Friendly",
  "Natural",
  "Latex",
  "Mattress",
  "Luxury",
  "Plush",
  "Mattress",
  "Comfort",
  "Support",
  "Hybrid",
  "Mattress",
  "Therapeutic",
  "Back",
  "Support",
  "Mattress",
  "Ultra",
  "Soft",
  "Pillow",
  "Top",
  "Mattress",
  "Orthopedic",
  "Support",
  "Mattress",
  "Gel-Infused",
  "Memory",
  "Foam",
  "Mattress",
  "Bamboo",
  "Charcoal",
  "Memory",
  "Foam",
  "Mattress",
  "Soft",
  "Euro",
  "Pillow",
  "Top",
  "Mattress",
  "Reversible",
  "Dual-Sided",
  "Mattress",
  "High-Profile",
  "Memory",
  "Foam",
  "Mattress",
  "Cooling",
  "Support",
  "Gel",
  "Mattress",
  "Classic",
  "Innerspring",
  "Mattress",
  "Customizable",
  "Firmness",
  "Mattress",
  "Allergy-Free",
  "Memory",
  "Foam",
  "Mattress",
  "Contour",
  "Support",
  "Mattress",
  "Budget-Friendly",
  "Memory",
  "Foam",
  "Mattress",
  "Tencel",
  "Lyocell",
  "Mattress",
  "Zero",
  "Motion",
  "Transfer",
  "Mattress",
  "Latex",
  "Comfort",
  "Mattress",
  "Sleep",
  "Science",
  "Hybrid",
  "Mattress",
  "Reinforced",
  "Edge",
  "Support",
  "Mattress",
  "Double-Sided",
  "Pillow",
  "Top",
  "Mattress",
  "Orthopedic",
  "Gel",
  "Mattress",
  "Firm",
  "Support",
  "Memory",
  "Foam",
  "Mattress",
  "High-Performance",
  "Cooling",
  "Mattress",
  "Ergonomic",
  "Sleep",
  "System",
  "Mattress",
  "Ultra",
  "Luxe",
  "Pillow",
  "Top",
  "Mattress",
  "Pet-Friendly",
  "Mattress",
  "Smart",
  "Sleep",
  "Technology",
  "Mattress",
  "Luxury",
  "Cooling",
  "Gel",
  "Mattress",
  "Eco-Conscious",
  "Innerspring",
  "Mattress",
  "Plush",
  "Memory",
  "Foam",
  "Mattress",
  "Luxury",
  "Euro",
  "Top",
  "Mattress",
  "Ventilated",
  "Memory",
  "Foam",
  "Mattress",
  "Adaptable",
  "Comfort",
  "Mattress",
  "Quilted",
  "Top",
  "Memory",
  "Foam",
  "Mattress",
  "Layered",
  "Support",
  "Mattress",
  "Cooling",
  "Comfort",
  "Mattress",
  "Deep",
  "Sleep",
  "Hybrid",
  "Mattress",
  "Enhanced",
  "Durability",
  "Mattress",
  "Firm",
  "Support",
  "Euro",
  "Pillow",
  "Top",
  "Mattress",
  "Soft",
  "Touch",
  "Memory",
  "Foam",
  "Mattress",
  "Reinforced",
  "Support",
  "Core",
  "Mattress",
  "Gentle",
  "Sleep",
  "Hybrid",
  "Mattress",
  "Pressure",
  "Relief",
  "Mattress",
  "Ultimate",
  "Sleep",
  "Experience",
  "Mattress",
];

type ChatInputProps = {
  handleSendMessage: (message: string) => void;
  setLoading: Dispatch<SetStateAction<boolean>>;
};

const ChatInput: React.FC<ChatInputProps> = ({
  handleSendMessage,
  setLoading,
}: ChatInputProps) => {
  const { clearChatObjects } = useChatStore();
  const { clearProductObjects } = useProductStore();
  const { resetProgress } = useProgressStore();
  const [message, setMessage] = useState<string>("");
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const userInput = e.target.value;
    setMessage(userInput);
    if (userInput) {
      const matches = mattressData.filter((item) =>
        item.toLowerCase().startsWith(userInput.toLowerCase())
      );
      setSuggestions(matches);
    } else {
      setSuggestions([]);
    }
  };
  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (suggestions.length && (e.key === "Tab" || e.key === "ArrowRight")) {
      e.preventDefault(); // Prevent default Tab behavior
      const lastWordIndex = message.lastIndexOf(" ") + 1; // Find the start index of the last word
      const newMessage = message.slice(0, lastWordIndex) + suggestions[0]; // Create new message with the suggestion
      setMessage(newMessage); // Update the message
      setSuggestions([]); // Clear suggestions
    }
  };
  const displaySuggestion =
    suggestions.length && message ? suggestions[0].slice(message.length) : "";
  // Calculate width of the input text
  const calculateTextWidth = (text: string) => {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    if (context) {
      context.font = "14px inherit"; // Match font size and family to input
      return context.measureText(text).width;
    }
    return 0; // Fallback in case context is null
  };
  const inputTextWidth = calculateTextWidth(message); // Width of the typed text
  // Adjust the positioning of the suggestion
  const suggestionPosition = inputTextWidth + 26;

  return (
    <div className="flex items-center border border-stone-400 rounded-full px-4 py-2 bg-white absolute bottom-0 backdrop-blur-lg w-full left-0 z-1000">
      <Input
        className="ml-2 flex-1 border-none focus:ring-0 focus:outline-none"
        autoComplete="off"
        name="message"
        placeholder="How can I help you?"
        value={message}
        onKeyDown={handleKeyDown}
        onChange={handleInputChange}
        onPressEnter={() => {
          handleSendMessage(message);
          setMessage("");
        }}
        style={{ position: "relative" }}
      />

      {displaySuggestion && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: `${suggestionPosition}px`, // Use the calculated position
            transform: "translateY(-50%)", // Vertically center the suggestion
            display: "flex",
            alignItems: "center",
            color: "#ccc", // Shaded text color
            pointerEvents: "none",
            fontFamily: "inherit",
            fontSize: "16px",
            whiteSpace: "nowrap",
          }}
        >
          <span style={{ visibility: "hidden" }}>{message}</span>
          <span style={{ opacity: 0.5 }}>{displaySuggestion}</span>
        </div>
      )}

      <Tooltip title="Clear Chat">
        <ConfigProvider
          theme={{
            token: {
              /* here is your global tokens */
              colorPrimary: "#A2332A",
            },
          }}
        >
          <Button
            icon={<StopOutlined />}
            shape="circle"
            className="border-none text-gray-400 ml-2 bg-transparent shadow-none cu"
            onClick={() => {
              setLoading(false);
              clearChatObjects();
              clearProductObjects();
              resetProgress();
              setMessage("");
            }}
          />
        </ConfigProvider>
      </Tooltip>
      <Divider type="vertical" />

      {/* Send Button */}
      <ConfigProvider
        theme={{
          token: {
            /* here is your global tokens */
            colorPrimary: "#A2332A",
          },
        }}
      >
        <Button
          icon={<SendOutlined />}
          shape="circle"
          type="primary"
          className="ml-2 border-none cursor-pointer"
          onClick={() => {
            handleSendMessage(message);
            setMessage("");
          }}
        />
      </ConfigProvider>
    </div>
  );
};

export default ChatInput;
