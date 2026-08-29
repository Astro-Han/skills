export function reviseBeforeTurn(messageId) {
  return {draftFrom: messageId, messages: historyBefore(messageId)};
}
