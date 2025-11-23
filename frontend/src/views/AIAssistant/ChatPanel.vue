<template>
  <contextHolder />
  <template v-if="!convId">
    <div class="welcome">
      <h2>
        {{
          new Date().getHours() < 6
            ? "凌晨好"
            : new Date().getHours() < 12
            ? "早上好"
            : new Date().getHours() < 14
            ? "中午好"
            : new Date().getHours() < 18
            ? "下午好"
            : "晚上好"
        }}, {{ userStore.user?.full_name || userStore.user?.username }}
      </h2>
      <div>欢迎使用聊天助手，开始一个对话以获得帮助。</div>
    </div>
  </template>
  <template v-else>
    <div class="title">
      <div class="conv_title">{{ convRef.title }}</div>
      <div class="conv_time">{{ convRef.time }}</div>
    </div>
    <div class="chat">
      <div class="msgs" ref="msgsRef">
        <CustomBubble
          v-for="m in convRef.messages"
          :key="m.id"
          :role="m.role"
          :username="m.username || (m.role === 'user' ? '你' : '助手')"
          :time="m.time"
          :text="m.content"
          :items="m.rag_docs"
          :loading="false"
        />
        <!-- 这样才能触发视图更新，不理解 -->
        <p v-show="false">{{ key }}</p>
      </div>

      <div class="sender">
        <Sender
          :value="in_text"
          :style="styles.sender"
          :loading="sending"
          @submit="onSubmit"
          @change="(value) => (in_text = value)"
        />
      </div></div
  ></template>
</template>

<script setup lang="ts">
import {
  ref,
  onMounted,
  watch,
  nextTick,
  computed,
  onBeforeUnmount,
} from "vue";
import { useRoute, useRouter } from "vue-router";
import { message } from "ant-design-vue";
import { Sender, XStream } from "ant-design-x-vue";
import CustomBubble from "./CustomBubble.vue";
import { getConversationMessages, getChatResponse } from "@/api/ai.js";
import { useUserStore } from "@/stores/user";
const userStore = useUserStore();
const [messageApi, contextHolder] = message.useMessage();

import { theme } from "ant-design-vue";
const { token } = theme.useToken();

const route = useRoute();
const convId = ref((route.params.conv_id as string | undefined) || undefined);
const router = useRouter();

type Msg = {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  time: string;
  rag_docs: any[];
  username?: string;
  __raw?: any;
};

const convRef = ref<{
  id?: string | undefined;
  title: string;
  time: string;
  messages: Msg[];
}>({ id: convId.value, title: "未命名会话", time: "", messages: [] });

const msgsRef = ref<HTMLElement | null>(null);
const loading = ref(false);
const sending = ref(false);
const in_text = ref("");
const key = ref(false);
const styles = {
  sender: {
    padding: "12px 16px",
    borderTop: "1px solid #eee",
  },
};

async function fetchMessages(id: string | undefined) {
  if (!id) {
    convRef.value.messages = [];
    return;
  }
  loading.value = true;
  try {
    const res = await getConversationMessages(id);
    if (res) {
      convRef.value.title = res.title || "未命名会话";
      convRef.value.time = new Date(res.created_at).toLocaleString() || "";
      convRef.value.messages = res.messages.map((it) => ({
        id: it.id ?? it._id ?? String(Math.random()),
        role: it.role ?? "assistant",
        content: it.content ?? it.message ?? "",
        time: it.created_at ? new Date(it.created_at).toLocaleString() : "",
        rag_docs: it.rag_docs ?? it.docs ?? [],
        username: it.role === "user" ? "你" : "助手",
        __raw: it,
      }));
      await nextTick();
      scrollToBottom();
    } else {
      convRef.value.messages = [];
    }
  } catch (err) {
    console.error("getConversationMessages error", err);
    messageApi.error("获取消息失败");
  } finally {
    loading.value = false;
  }
}

function scrollToBottom() {
  nextTick(() => {
    const el = msgsRef.value as HTMLElement | null;
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
  });
}

onMounted(() => {
  fetchMessages(convId.value);

  // 监听会话重命名事件，若当前会话被重命名则更新标题
  const onRenamed = (ev: Event) => {
    try {
      const detail = (ev as CustomEvent).detail;
      if (!detail) return;
      const { id, title } = detail;
      if (String(convId.value) === String(id)) {
        convRef.value.title = title ?? convRef.value.title;
      }
    } catch (e) {
      /* ignore */
    }
  };
  window.addEventListener("conversation-renamed", onRenamed);
  onBeforeUnmount(() => {
    window.removeEventListener("conversation-renamed", onRenamed);
  });
});

watch(
  () => route.params.conv_id,
  (v) => {
    convId.value = v as string | undefined;
    fetchMessages(convId.value);
  }
);

const onSubmit = async (value: string) => {
  if (!convId.value) {
    messageApi.warn("请先选择或创建会话");
    return;
  }
  sending.value = true;
  try {
    convRef.value.messages.push({
      id: `user-${Date.now()}`,
      role: "user",
      content: value,
      time: new Date().toLocaleString(),
      rag_docs: [],
      username: "你",
    });

    const response = await getChatResponse(convId.value, value);
    // 获取可读流
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    const ai_message = {
      id: `assistant-${Date.now()}`,
      role: "assistant",
      content: "",
      time: new Date().toLocaleString(),
      rag_docs: [],
      username: "助手",
    };
    convRef.value.messages.push(ai_message);
    scrollToBottom();
    // 逐步读取数据
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      // 逐行处理（SSE 可能一次返回多行）
      const linesArr = chunk.split("\n");
      for (const line of linesArr) {
        if (line.startsWith("data:")) {
          const dataStr = line.slice(5).trim();
          if (!dataStr) continue;
          // 判断是否为 JSON
          try {
            const data = JSON.parse(dataStr);
            const begin = data.begin ?? false;
            const done = data.done ?? false;
            if (begin) {
              const conv_id = data.conv_id ?? null;
              continue;
            }
            if (done) {
              ai_message.rag_docs = data.rag_docs ?? [];
              continue;
            }
            ai_message.content += data.content ?? "";
            key.value = !key.value;
            await nextTick();
            scrollToBottom();
          } catch {
            ai_message.content += dataStr;
            await nextTick();
          }
        }
      }
    }
  } catch (error) {
    console.error("Stream connection failed:", error);
    // 可以在这里添加错误处理，比如显示错误信息
  } finally {
    sending.value = false;
    in_text.value = "";
    scrollToBottom();
  }
};
</script>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  flex: 1;
  background-color: #ffffff;
  height: calc(100vh - 180px);
  padding: 20px;
  gap: 20px;
}
.msgs {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  max-height: calc(100vh - 180px);
  width: 100%;
  height: 100%;
}
.sender {
  height: 60px;
  width: 100%;
  flex-shrink: 0;
  margin-bottom: 10px;
}
.welcome {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 36px;
  gap: 10px;
  background-color: #ffffff;
}

.welcome h2 {
  font-size: 48px;
  color: #333;
  font-family: "楷体", "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans SC",
    "PingFang SC", "Microsoft YaHei", "WenQuanYi Micro Hei", Arial, sans-serif;
}

.welcome div {
  font-size: 16px;
  color: #666;
}

.title {
  display: flex;
  gap: 25px;
  align-items: baseline;
  background: linear-gradient(to bottom, #f2f3f5 0%, #ffffff 100%);
  padding: 10px;
}

.conv_title {
  font-size: 20px;
  font-weight: 600;
  color: #111;
}

.conv_time {
  font-size: 14px;
  color: #999;
}
</style>
