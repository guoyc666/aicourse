<template>
  <div :key="renderKey" :style="style">
    <Bubble
      :avatar="{
        icon: h(UserOutlined),
        style:
          props.role === 'assistant'
            ? avatarStyle.foo
            : props.role === 'user'
            ? avatarStyle.bar
            : avatarStyle.hide,
      }"
      :placement="props.role === 'user' ? 'end' : 'start'"
      :content="props.text"
      :messageRender="props.role === 'assistant' ? renderMarkdown : null"
      :loading="props.loading"
      :typing="props.typing"
      style="text-align: left"
    >
      <template #header>
        <div class="header-row">
          <div class="username">{{ props.username }}</div>
          <div class="time">{{ props.time }}</div>
        </div>
      </template>
      <template v-if="props.items && props.items.length" #footer>
        <div v-for="item in props.items" :key="item.fileid" class="item">
          <div class="item-name">
            <a :href="item.filepath">{{ item.filename }}</a>
          </div>
        </div>
      </template>
    </Bubble>
  </div>
</template>

<script setup>
import { Bubble } from "ant-design-x-vue";
import { UserOutlined } from "@ant-design/icons-vue";
import { Typography } from "ant-design-vue";
import { onWatcherCleanup, ref, watchEffect, h, watch } from "vue";
import markdownit from "markdown-it";

defineOptions({ name: "CustomBubble" });

const props = defineProps({
  role: { type: String, default: "user" },
  username: { type: String, default: "AI assistant" },
  time: { type: String, default: "12:34" },
  text: { type: String, default: "这是消息内容，可以是**加粗**或*斜体*等" },
  items: {
    type: Array,
    default: () => [
      { fileid: 1, filename: "文件1.pdf", filepath: "/files/file1.pdf" },
      { fileid: 2, filename: "图片2.png", filepath: "/files/image2.png" },
    ],
  },
  loading: { type: Boolean, default: false },
  typing: { type: Object, default: null },
  // { step: 1, interval: 100 }
});

const md = markdownit({ html: true, breaks: true });

const renderMarkdown = (content) =>
  h(Typography, null, {
    default: () => h("div", { innerHTML: md.render(content) }),
  });

const renderKey = ref(0);
if (props.role === "assistant") {
  watchEffect(() => {
    const id = setTimeout(() => {
      renderKey.value = renderKey.value + 1;
    }, props.text.length * 100 + 2000);
    onWatcherCleanup(() => {
      clearTimeout(id);
    });
  });
}

const style = {
  marginRight: props.role === "assistant" ? "50px" : "0",
  marginLeft: props.role === "user" ? "50px" : "0",
};
const avatarStyle = {
  foo: {
    color: "#f56a00",
    backgroundColor: "#fde3cf",
  },
  bar: {
    color: "#fff",
    backgroundColor: "#87d068",
  },
  hide: {
    visibility: "hidden",
  },
};

</script>

<style scoped>
.header-row {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}
.username {
  font-weight: 600;
  color: #111;
}
.time {
  font-size: 12px;
  color: #888;
  margin-left: auto; /* 将时间推到右侧 */
}

/* footer items 风格：更小、行内排列、无圆角、与上方更紧凑 */
.item {
  display: inline-block;
  margin-right: 6px;
  margin-bottom: 4px;
  margin-top: 0px;
}
.item-name a {
  display: inline-block;
  padding: 4px 6px; /* 更小的内边距 */
  font-size: 11px; /* 更小字体 */
  color: #333; /* 不要蓝色，使用中性文字色 */
  background: #fafafa; /* 轻微背景区分 */
  border: 1px solid #e6e6e6; /* 低对比边框 */
  border-radius: 0; /* 取消圆角 */
  text-decoration: none;
  line-height: 1;
}
.item-name a:hover {
  background: #f2f2f2;
  text-decoration: none;
}
</style>
