import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { immer } from "zustand/middleware/immer";

import { ChatMessage } from "../types/ChatMessage";
import { ProductType } from "../types/ProductType";

type ChatState = {
  chatObjects: Array<ChatMessage | string>;
  sessionId: string;
};
type ChatActions = {
  addChatObject: (chatObject: ChatMessage | string) => void;
  clearChatObjects: () => void;
  addSession: (session: string) => void;
};

type ProductState = {
  productObjects: Array<ProductType | string>;
};
type ProductActions = {
  addProductObject: (productObject: ProductType | string) => void;
  clearProductObjects: () => void;
};

type ProgressState = {
  mattressType: boolean;
  features: boolean;
  sleepPreferences: boolean;
  budget: boolean;
  size: boolean;
  brand: boolean;
  progressValue: number;
};
type ProgressActions = {
  setField: (
    field: keyof Omit<ProgressState, "progressValue">,
    value: boolean
  ) => void;
  calculateProgress: () => void;
  resetProgress: () => void;
};

const useChatStore = create<ChatState & ChatActions>()(
  persist(
    immer((set) => ({
      chatObjects: [],
      sessionId: "",

      addChatObject: (chatObject: ChatMessage | string) => {
        set((state) => {
          state.chatObjects.push(chatObject);
        });
      },

      clearChatObjects: () => {
        set((state) => {
          state.chatObjects = [];
        });
      },
      addSession: (session: string) => {
        set((state) => {
          state.sessionId = session;
        });
      },
    })),
    {
      name: "chatMessages",
      storage: createJSONStorage(() => localStorage),
    }
  )
);

export const useProductStore = create<ProductState & ProductActions>()(
  persist(
    immer((set) => ({
      productObjects: [],

      addProductObject: (productObject: ProductType | string) => {
        set((state) => {
          state.productObjects.push(productObject);
        });
      },

      clearProductObjects: () => {
        set((state) => {
          state.productObjects = [];
        });
      },
    })),
    {
      name: "products",
      storage: createJSONStorage(() => localStorage),
    }
  )
);

export const useProgressStore = create<ProgressState & ProgressActions>()(
  persist(
    immer((set, get) => ({
      mattressType: false,
      features: false,
      sleepPreferences: false,
      budget: false,
      size: false,
      brand: false,
      progressValue: 0,

      setField: (field, value) => {
        set((state) => {
          state[field] = value;
        });
        get().calculateProgress();
      },

      calculateProgress: () => {
        const state = get();
        const fields = [
          state.mattressType,
          state.features,
          state.sleepPreferences,
          state.budget,
          state.size,
          state.brand,
        ];
        const trueCount = fields.filter((field) => field === true).length;
        const progress = (trueCount / fields.length) * 100;
        set((state) => {
          state.progressValue = progress;
        });
      },
      resetProgress: () => {
        set((state) => {
          state.mattressType = false;
          state.features = false;
          state.sleepPreferences = false;
          state.budget = false;
          state.size = false;
          state.brand = false;
          state.progressValue = 0;
        });
      },
    })),
    {
      name: "progress",
      storage: createJSONStorage(() => localStorage),
    }
  )
);

export default useChatStore;
