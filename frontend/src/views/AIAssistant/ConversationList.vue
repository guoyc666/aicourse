<template>
  <contextHolder />
  <div :style="styles.menu">
    <div :style="styles.logo">
      <img
        src="https://mdn.alipayobjects.com/huamei_iwk9zp/afts/img/A*eco6RrQhxbMAAAAAAAAAAAAADgCCAQ/original"
        draggable="false"
        alt="logo"
        :style="styles['logo-img']"
      />
      <span :style="styles['logo-span']">AI-assistant</span>
    </div>
    <Button type="link" :style="styles.addBtn" @click="onAddConversation">
      <PlusOutlined />
      新对话
    </Button>
    <Conversations
      default-active-key="item1"
      :menu="menuConfig"
      :items="items"
      :style="styles.conversations"
      :active-key="activeKey"
      @active-change="onConversationClick"
    />
  </div>
</template>

<script setup lang="ts">
import {
  DeleteOutlined,
  PlusOutlined,
  EditOutlined,
} from "@ant-design/icons-vue";
import {
  theme,
  message,
  Modal,
  Input,
  Button,
  Typography,
} from "ant-design-vue";
const [messageApi, contextHolder] = message.useMessage();
const { token } = theme.useToken();

import { Conversations, type ConversationsProps } from "ant-design-x-vue";
import { computed, h, ref, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
const router = useRouter();
const route = useRoute();
const convId = ref((route.params.conv_id as string | undefined) || undefined);
watch(
  () => route.params.conv_id,
  (v) => {
    convId.value = v as string | undefined;
    activeKey.value = convId.value || null;
  }
);
import {
  createConversation,
  getConversations,
  deleteConversation,
  renameConversation,
} from "@/api/ai.js";

defineOptions({ name: "AXConversationsWithMenuSetup" });

const items = ref<ConversationsProps["items"]>([]);
const activeKey = ref<string>(null);
const loading = ref(false);

// 从后端拉取会话列表
const fetchConversations = async () => {
  loading.value = true;
  try {
    const res = await getConversations();
    if (res) {
      items.value = res.map((it) => ({
        key: it.id,
        label: it.title || "新对话",
      }));
    } else {
      items.value = [];
    }
  } catch (err) {
    message.error("获取会话失败");
  } finally {
    loading.value = false;
  }
};

// 初始加载
onMounted(() => {
  fetchConversations();
  activeKey.value = convId.value || null;
});

const menuConfig: ConversationsProps["menu"] = (conversation) => ({
  items: [
    {
      label: "重命名",
      key: "rename",
      icon: h(EditOutlined),
    },
    {
      label: "删除",
      key: "delete",
      icon: h(DeleteOutlined),
      danger: true,
    },
  ],
  onClick: (menuInfo) => {
    // messageApi.info(`Click ${conversation.key} - ${menuInfo.key}`);
    const idx = items.value.findIndex((i) => i.key === conversation.key);
    if (menuInfo.key === "delete") {
      // 调用后端删除接口
      (async () => {
        try {
          await deleteConversation(conversation.key);
          // 在本地移除或标记
          if (idx !== -1) {
            items.value.splice(idx, 1);
          }

          // 如果删除的是当前打开的会话，则从路由中移除 conv_id
          try {
            if (String(conversation.key) === String(convId.value)) {
              const base = route.path.replace(/\/$/, "");
              const trimmed =
                typeof route.params.conv_id !== "undefined"
                  ? base.replace(new RegExp(`/${route.params.conv_id}$`), "")
                  : base;
              // 导航到不带 conv_id 的路径
              router.push(trimmed).catch(() => {});
            }
          } catch (e) {
            console.warn('remove convId from route failed', e);
          }

          messageApi.success("删除成功");
        } catch (err) {
          console.error("deleteConversation error", err);
          messageApi.error("删除失败");
        }
      })();
    } else if (menuInfo.key === "rename") {
      // 获取当前纯文本标题作为默认值
      const currentTitle =
        items.value[idx]?.title ??
        (typeof conversation.label === "string" ? conversation.label : "");
      const inputValue = ref(String(currentTitle));
      Modal.confirm({
        title: "重命名会话",
        content: h(Input, {
          value: inputValue.value,
          "onUpdate:value": (val: string) => (inputValue.value = val),
          autofocus: true,
        }),
        okText: "确定",
        cancelText: "取消",
        onOk: async () => {
          try {
            await renameConversation(conversation.key, {
              title: inputValue.value,
            });
            if (idx !== -1) {
              // 更新 title 和 label（label 使用 Typography.Text VNode）
              items.value[idx] = {
                ...items.value[idx],
                label: inputValue.value,
              };
            }

            // 通知其他组件（例如 ChatPanel）该会话已重命名
            try {
              window.dispatchEvent(
                new CustomEvent('conversation-renamed', {
                  detail: { id: String(conversation.key), title: inputValue.value },
                })
              );
            } catch (e) {
              console.warn('dispatch conversation-renamed failed', e);
            }

            messageApi.success("重命名成功");
          } catch (err) {
            console.error("renameConversation error", err);
            messageApi.error("重命名失败");
          }
        },
      });
    }
  },
});

const pushWithConvId = (id: string | number) => {
  const base = route.path.replace(/\/$/, "");
  const trimmed =
    typeof route.params.conv_id !== "undefined"
      ? base.replace(new RegExp(`/${route.params.conv_id}$`), "")
      : base;
  router.push(`${trimmed}/${id}`).catch(() => {});
};

watch(
  () => route.params.conv_id,
  (v) => {
    convId.value = v as string | undefined;
    activeKey.value = convId.value || null;
  }
);

const onAddConversation = async () => {
  try {
    const res = await createConversation({ title: "新对话" });
    if (res) {
      // 插入到最前面并激活
      items.value.unshift({
        key: res.id,
        label: res.title || "新对话",
        disabled: false,
      });
      activeKey.value = res.id;
      pushWithConvId(res.id);
      messageApi.success("创建成功");
    } else {
      messageApi.error("创建失败");
    }
  } catch (err) {
    console.error("createConversation error", err);
    messageApi.error("创建失败");
  }
};

const onConversationClick: ConversationsProps["onActiveChange"] = (key) => {
  console.log(111);
  activeKey.value = key;
  pushWithConvId(key);
  messageApi.success(`切换到会话 ${key}`);
};

const styles = {
  addBtn: {
    background: "#1677ff0f",
    border: "1px solid #1677ff34",
    width: "calc(100% - 24px)",
    margin: "0 12px 24px 12px",
  },
  conversations: {
    padding: "0 12px",
    flex: 1,
    overflowY: "auto",
    "text-align": "left",
  },
  menu: {
    background: `${token.value.colorBgLayout}80`,
    width: "280px",
    height: "100%",
    display: "flex",
    "flex-direction": "column",
  },
  logo: {
    display: "flex",
    height: "72px",
    "align-items": "center",
    "justify-content": "start",
    padding: "0 24px",
    "box-sizing": "border-box",
  },
  "logo-span": {
    display: "inline-block",
    margin: "0 8px",
    "font-weight": "bold",
    color: token.value.colorText,
    "font-size": "16px",
  },
  "logo-img": {
    width: "24px",
    height: "24px",
    display: "inline-block",
  },
};
</script>
