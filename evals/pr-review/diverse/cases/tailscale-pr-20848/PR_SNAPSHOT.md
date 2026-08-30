# Frozen pull request snapshot

- PR: https://github.com/tailscale/tailscale/pull/20848 — `hostinfo: improve detection of linux desktops`
- Author: cmol
- Target base head: `5a1066f494d482a4e9c573a4a334fb91418da3cd`
- Comparison base: `d200b3f18f0ee4cff1f6819a78a9fe8e6a7367f2`
- Exact source head: `efb3c35cae23d06988a564e5d7073f1cf0a892ca`
- Diff: 262 additions, 12 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Our desktop detection was using "wayland-1" as a search string for
detecting wayland desktops, but many desktops use other indexes for the
session. Additionally we did not detect mir or gamescope.

Add a new detection method that leans on systemd-logind (if available)
and fall back to using the existing method of looking for open unix
sockets, but add search strings and tail the index off of the wayland
session detection.

Fixes #20847

Signed-off-by: Claus Lensbøl <claus@tailscale.com>


## Linked issues

### https://github.com/tailscale/tailscale/issues/20847 — Linux desktop detection looks for wrong wayland string

Our Linux wayland detection looks for "wayland-1" but that string does not exist in that file for a standard Ubuntu 26.04 install. The system does end up detecting as having a desktop, but only because xWayland is running and our detection for x11 works on xWayland too.

That might work for some installs, but for wayland only systems, this is will likely fail.

On top of that, we do not detect mir or gamescope (the compositor of SteamOS).

## Exact-head checks

- prepare: SKIPPED
- gomod-cache: SUCCESS
- Analyze (go): SUCCESS
- deploy: SUCCESS
- checklocks: SUCCESS
- lint: SUCCESS
- EasyEasy: SUCCESS
- vet: SUCCESS
- matrix.test: SKIPPED
- fuzz: SUCCESS
- race-root-integration (1/4): SUCCESS
- race-root-integration (2/4): SUCCESS
- race-root-integration (3/4): SUCCESS
- race-root-integration (4/4): SUCCESS
- test (amd64): SUCCESS
- test (amd64, -race, 1/3): SUCCESS
- test (amd64, -race, 2/3): SUCCESS
- test (amd64, -race, 3/3): SUCCESS
- test (386): SUCCESS
- Windows (benchmarks): SUCCESS
- Windows (1/2): SUCCESS
- Windows (2/2): SUCCESS
- macos: SUCCESS
- privileged: SUCCESS
- cross (linux, arm64): SUCCESS
- cross (linux, 386): SUCCESS
- cross (linux, loong64): SUCCESS
- cross (linux, arm, 5): SUCCESS
- cross (linux, arm, 7): SUCCESS
- cross (darwin, amd64): SUCCESS
- cross (darwin, arm64): SUCCESS
- cross (windows, amd64): SUCCESS
- cross (windows, arm64): SUCCESS
- cross (freebsd, amd64): SUCCESS
- cross (openbsd, amd64): SUCCESS
- ios: SUCCESS
- crossmin (plan9, amd64): SUCCESS
- crossmin (aix, ppc64): SUCCESS
- crossmin (solaris, amd64): SUCCESS
- crossmin (illumos, amd64): SUCCESS
- android: SUCCESS
- wasm: SUCCESS
- tailscale_go: SUCCESS
- depaware: SUCCESS
- go_generate: SUCCESS
- make_tidy: SUCCESS
- licenses: SUCCESS
- staticcheck (macOS): SUCCESS
- staticcheck (Windows): SUCCESS
- staticcheck (Linux): SUCCESS
- staticcheck (Portable (1/4)): SUCCESS
- staticcheck (Portable (2/4)): SUCCESS
- staticcheck (Portable (3/4)): SUCCESS
- staticcheck (Portable (4/4)): SUCCESS
- notify_slack: SUCCESS
- merge_blocker: SUCCESS
- check_mergeability_strict: SUCCESS
- check_mergeability: SUCCESS
- CodeQL: SUCCESS
- DCO: SUCCESS
- unnamed: SUCCESS

## Changed files

- `hostinfo/hostinfo.go`: +27/-11
- `hostinfo/hostinfo_linux.go`: +96/-0
- `hostinfo/hostinfo_linux_test.go`: +139/-0
- `hostinfo/hostinfo_test.go`: +0/-1
