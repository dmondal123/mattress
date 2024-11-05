import { Progress } from "antd";

export default function ChatProgress() {
  return (
    <div className="mb-6 pr-4">
      <p className="text-xl font-medium mb-2">Progress</p>
      <Progress percent={40} strokeColor="#D32F2F" />
    </div>
  );
}
