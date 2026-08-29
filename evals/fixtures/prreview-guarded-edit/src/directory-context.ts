export function prepareDirectoryContext(message, listing) {
  return {...message, displayText: message.text, text: `${message.text}\n\n${listing}`};
}
