export class BufferQueue {
  private pending: string[] = [];

  constructor(private sink: {write(items: string[]): Promise<void>}) {}

  enqueue(item: string) {
    this.pending.push(item);
  }
  async flush() {
    if (this.pending.length > 1) {
      await this.sink.write(this.pending);
      this.pending = [];
    }
  }
}
