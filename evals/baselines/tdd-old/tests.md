# Tests Worth Keeping

## Test behavior at a public seam

A test should read like a specification of something a caller or user can observe. Prefer names such as `rejects an expired token` over names such as `calls validateToken twice`.

Drive the same interface production callers use:

```typescript
test("retrieves a newly created user", async () => {
  const created = await createUser({ name: "Alice" });
  expect((await getUser(created.id)).name).toBe("Alice");
});
```

Avoid bypassing that interface to inspect internal storage, private methods, collaborator call order, or implementation-specific events.

## Use an independent oracle

The expected value must be able to disagree with the implementation. Use a known literal, worked example, specification, fixture, or trusted external contract.

```typescript
// Independent expectation
expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);

// Tautological: repeats the production algorithm
const expected = items.reduce((sum, item) => sum + item.price, 0);
expect(calculateTotal(items)).toBe(expected);
```

## Keep each RED narrow

One test should introduce one behavior. If the test name needs `and`, split it unless those outcomes form one inseparable contract.

Write the next test only after the current slice is green. Bulk-written tests commit to imagined behavior and usually couple the suite to a design that has not yet been learned.

## Check the failure signal

Before implementing, read the failure. It must prove the missing behavior is what failed. A syntax error, broken fixture, wrong import, or failure on another path is not a useful RED.

After GREEN, run the new test plus the nearest suite that covers the same public contract and its direct consumers.
