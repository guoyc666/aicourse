<template>
  <contextHolder />
  <div class="chat">
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
          }}
        </h2>
        <div>欢迎使用聊天助手，开始一个对话以获得帮助。</div>
      </div>
    </template>
    <template v-else>
      <div class="msgs" ref="msgsRef">
        <CustomBubble
          v-for="m in messages"
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
        /></div
    ></template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, computed } from "vue";
import { useRoute } from "vue-router";
import { message } from "ant-design-vue";
import { Sender, XStream } from "ant-design-x-vue";
import CustomBubble from "./CustomBubble.vue";
import { getConversationMessages, getChatResponse } from "@/api/ai.js";
import request from "@/api/request.js";
const [messageApi, contextHolder] = message.useMessage();

import { theme } from "ant-design-vue";
const { token } = theme.useToken();

const route = useRoute();
const convId = ref((route.params.conv_id as string | undefined) || undefined);

const messages = ref([]);
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
    messages.value = [];
    return;
  }
  loading.value = true;
  try {
    const res = await getConversationMessages(id);
    if (res && res.data && Array.isArray(res.data)) {
      messages.value = res.data.map((it) => ({
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
      messages.value = [];
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
    messages.value.push({
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
    messages.value.push(ai_message);
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
  padding: 50px 80px;
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
}
.welcome {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 36px;
  gap: 10px;
}

.welcome div {
  font-size: 16px;
  color: #666;
}
</style>
