it("blocks editing expanded context", () => {
  expect(beginEditUserMessage({text: "prompt + listing", displayText: "prompt"}).ok).toBe(false);
});
