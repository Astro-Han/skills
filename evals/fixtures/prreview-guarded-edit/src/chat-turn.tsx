import {beginEditUserMessage} from "./revision-actions";

export function ChatTurn({turn}) {
  const canEdit = !turn.attachments?.length && !turn.quote;
  return canEdit ? <button onClick={() => beginEditUserMessage(turn.user)}>Edit</button> : null;
}
