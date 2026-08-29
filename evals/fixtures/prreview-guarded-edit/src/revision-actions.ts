import {reviseBeforeTurn} from "./session-manager";

export function beginEditUserMessage(message) {
  if (message.displayText && message.displayText !== message.text) {
    return {ok: false, reason: "expanded context cannot be edited and resent"};
  }
  return reviseBeforeTurn(message.id);
}
