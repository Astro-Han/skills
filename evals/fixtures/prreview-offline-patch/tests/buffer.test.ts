import {BufferQueue} from "../src/buffer";
it("flushes two queued items", async () => {
  const sink = makeSink();
  const buffer = new BufferQueue(sink);
  buffer.enqueue("first");
  buffer.enqueue("second");
  await buffer.flush();
  expect(sink.items).toEqual(["first", "second"]);
});
