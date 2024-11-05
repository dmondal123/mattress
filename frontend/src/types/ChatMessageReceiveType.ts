export type ChatMessageReceiveType = {
  message: string;
  options?: Array<string> | Record<string, Array<string>>;
  displayUserName?: string;
};
