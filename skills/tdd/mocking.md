# Mocking at Boundaries

Use a test double only where the system crosses a boundary you do not control or cannot exercise reliably: external APIs, time, randomness, email, payment providers, and sometimes databases or filesystems.

Do not mock your own modules merely to isolate a unit. Run real internal code through its public interface so refactoring does not require rewriting mock choreography.

## Make boundaries explicit

Pass external dependencies in rather than constructing them inside business logic. Prefer a small domain-specific interface such as `chargePayment(order)` over a generic request function whose mock needs conditional routing.

Assert the observable boundary effect: destination, payload, returned result, emitted event, or persisted state. Avoid asserting private method names or call counts unless the call itself is the public contract.

## Choose fidelity deliberately

- Prefer a real dependency when it is local, fast, isolated, and deterministic.
- Use a fake or stub to exercise rare failures, remove an unavailable external service, or keep the feedback loop fast.
- Add a contract or integration test when a double could drift from the real provider.
- Never call a live production service from a fast test suite.

If a test needs extensive conditional mock setup, the seam is probably too generic or the behavior is being tested at the wrong layer. Narrow the boundary before adding more mock logic.
