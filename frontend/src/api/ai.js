import request from "./request";

export const createConversation = (data) => {
  return request.post("/ai/conversations", data);
};

export const getConversations = () => {
  return request.get("/ai/conversations");
}

export const deleteConversation = (conversationId) => {
  return request.delete(`/ai/conversations/${conversationId}`);
}

export const renameConversation = (conversationId, data) => {
  return request.put(`/ai/conversations/${conversationId}`, data);
}

export const getChatResponse = (convId, content) => {
  return fetch(
      `/ai/conversations/${convId}/messages`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_input: content
        }),
      }
    );
}

/**
 * 
 * @param {*} conversationId 
 * @returns [
  {
    "id": 0,
    "role": "string",
    "content": "string",
    "created_at": "2025-11-12T19:03:11.850Z",
    "rag_docs": [
      {
        "additionalProp1": {}
      }
    ]
  }
]
 */
export const getConversationMessages = (conversationId) => {
  return request.get(`/ai/conversations/${conversationId}/messages`);
}
