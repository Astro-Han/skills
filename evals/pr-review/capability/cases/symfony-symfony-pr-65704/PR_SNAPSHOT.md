# Frozen pull request snapshot

- PR: https://github.com/symfony/symfony/pull/65704 — `[HttpClient] Drop credentials when a redirect changes the scheme`
- Author: nicolas-grekas
- Target base head: `cce3166e8a8efbe5d44433a9dd9c4d293735e540`
- Comparison base: `565300eaad6e347918d2e8c478d30ceabe6088ab`
- Exact source head: `d25fabf6e4f59f9a76f78c32651d5d2452eb92ac`
- Diff: 141 additions, 11 deletions, 8 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

| Q             | A
| ------------- | ---
| Branch?       | 5.4
| Bug fix?      | yes
| New feature?  | no
| Deprecations? | no
| Issues        | -
| License       | MIT

When a response redirects to another host, the redirect handling of every client drops the `Authorization` and `Cookie` headers before following it. It kept them when the host was the same but the scheme changed, so an `https://` request redirected to `http://` on the same host sent the credentials in clear text. Browsers and the Fetch standard strip these headers on any change of origin, and the scheme is part of the origin.

The scheme is now compared next to the host in the four places that make this decision: `CurlHttpClient`, `NativeHttpClient`, `AmpResponse` and `NoPrivateNetworkHttpClient`. Other custom headers keep following the redirect as before, and a redirect to the same scheme and host still carries the credentials.

The test starts a small server that serves TLS and plain HTTP on the same port, using the certificate already in the fixtures: a TLS request is redirected to the plain URL of the same host and port, and a plain request echoes the headers it received. The test runs for the curl, native, Amp and mock clients through `HttpClientTestCase`, and once more with `NoPrivateNetworkHttpClient`. With the fix reverted, the native, Amp and `NoPrivateNetwork` clients fail it with `Failed asserting that an array does not have the key 'authorization'`. The curl client passes it on both states: libcurl 8.5.0 drops the headers itself on a scheme change, so the change in `CurlHttpClient` aligns the code path for the libcurl versions that do not.

Not covered: the port stays out of the comparison on this branch, as before (a redirect to another port of the same host keeps the credentials). Windows was not tested locally.

This targets 5.4 on purpose, as a hardening change: it fixes a credential leak that exists in the same shape on every maintained branch.

Checks run: `./phpunit src/Symfony/Component/HttpClient` (804 tests, 26 skipped, no failures) and php-cs-fixer on the changed files.


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- x86 / minimal-exts / lowest-php: FAILURE
- Integration (7.2): SUCCESS
- Psalm: SUCCESS
- Unit Tests (7.2): SUCCESS
- Verify Packages: SUCCESS
- Integration (8.0): SUCCESS
- Unit Tests (7.4): SUCCESS
- Unit Tests (8.2, high-deps): FAILURE
- Unit Tests (8.2, low-deps): FAILURE
- Unit Tests (8.3): SUCCESS
- Unit Tests (8.4, amqp,apcu,igbinary,intl,mbstring,memcached,redis): SUCCESS

## Changed files

- `src/Symfony/Component/HttpClient/CurlHttpClient.php`: +5/-3
- `src/Symfony/Component/HttpClient/NativeHttpClient.php`: +5/-5
- `src/Symfony/Component/HttpClient/NoPrivateNetworkHttpClient.php`: +3/-2
- `src/Symfony/Component/HttpClient/Response/AmpResponse.php`: +1/-1
- `src/Symfony/Component/HttpClient/Tests/Fixtures/tls/redirect-server.php`: +42/-0
- `src/Symfony/Component/HttpClient/Tests/HttpClientTestCase.php`: +22/-0
- `src/Symfony/Component/HttpClient/Tests/NoPrivateNetworkHttpClientTest.php`: +23/-0
- `src/Symfony/Component/HttpClient/Tests/TestRedirectServer.php`: +40/-0
