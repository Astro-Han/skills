import {BufferQueue} from "./buffer";

export async function closeProducer(buffer: BufferQueue) {
  await buffer.flush();
}
