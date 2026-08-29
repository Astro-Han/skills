import {loadSettings} from "../src/settings";

it("defaults a missing timeout", () => {
  expect(loadSettings({}).timeoutMs).toBe(30_000);
});
