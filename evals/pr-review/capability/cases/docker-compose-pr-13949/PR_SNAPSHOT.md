# Frozen pull request snapshot

- PR: https://github.com/docker/compose/pull/13949 — `fix(build): use platform image-manifest digest, not attested index`
- Author: glours
- Target base head: `5bf5a21687107138629baa30be97f0bd9a0c55b2`
- Comparison base: `5bf5a21687107138629baa30be97f0bd9a0c55b2`
- Exact source head: `32290a0db0f7a8271a3cfbfab93e0644f70d5281`
- Diff: 256 additions, 14 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

**What I did**
With the containerd image store and BuildKit provenance attestations (the default), a built image is stored as an attested index whose top-level digest also covers the attestation manifest. That digest churns on every build even when the runnable content is unchanged, so compose recreated containers on every `up --build`.

Compare the digest of the "image" kind manifest instead, selected for the target platform and restricted to locally available manifests, so it is deterministic and reflects only config + layers. Both the build and up sides of the staleness check go through the same selection, and registry-only images keep the Bake-reported digest.

**Related issue**
Fixes #13636

**(not mandatory) A picture of a cute animal, if possible in relation to what you did**


## Linked issues

### https://github.com/docker/compose/issues/13636 — [BUG] `docker compose build` produces different image IDs on each rebuild with containerd image store, but works correctly with overlay2

### Description

When Docker Engine uses the containerd image store (default for new installations since
Docker 28), `docker compose build` produces a new image ID on every rebuild even when no
files have changed. This causes `docker compose up` to unnecessarily recreate all containers
on every deploy.

Disabling the containerd image store on the same server fixes the issue — the second build
reuses the cache completely and the image ID stays the same.

### Steps To Reproduce

Use Docker CE on Linux with the containerd image store enabled (default for fresh installs):

```
$ docker info -f '{{.Driver}}'
overlayfs
```

Create these three files:

**Dockerfile:**
```dockerfile
FROM alpine:3.21
RUN echo "hello" > /hello.txt
COPY config.txt /config.txt
CMD ["cat", "/hello.txt", "/config.txt"]
```

**config.txt:**
```
static config file
```

**docker-compose.yml:**
```yaml
services:
  app:
    build: .
    container_name: test-cache
```

Then run:

```bash
# Build twice with nothing changed in between:
docker compose build
docker images --format '{{.ID}}' --filter reference='*-app'

docker compose build
docker images --format '{{.ID}}' --filter reference='*-app'
```

## Expected behavior

Second build reuses cache. Image ID is the same. `docker compose up` does not recreate the
container.

## Actual behavior

Second build produces a different image ID. `docker compose up` sees a different image and
recreates the container.

Note: individual build steps show `CACHED` for RUN/COPY layers, but the final image still
gets a new ID. The exporting steps (`exporting layers`, `writing image`, `naming`) take
0.1–0.2s instead of 0.0s, suggesting they actually re-export rather than reuse.

### Compose Version

```Text
Docker Compose version v5.1.0
```

### Docker Environment

```Text
Client: Docker Engine - Community
 Version:    29.3.0
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.31.1
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v5.1.0
    Path:     /usr/libexec/docker/cli-plugins/docker-compose

Server:
 Containers: 8
  Running: 7
  Paused: 0
  Stopped: 1
 Images: 8
 Server Version: 29.3.0
 Storage Driver: overlayfs
  driver-type: io.containerd.snapshotter.v1
 Logging Driver: local
 Cgroup Driver: systemd
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 301b2dac98f15c27117da5c8af12118a041a31d9
 runc version: v1.3.4-0-gd6d73eb8
 init version: de40ad0
 Security Options:
  apparmor
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.8.0-106-generic
 Operating System: Ubuntu 24.04.4 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 4
 Total Memory: 7.57GiB
 Name: secondary
 ID: 091526cd-489b-4f47-acad-33efcea821cb
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
 Firewall Backend: iptables
```

### Anything else?

## Related issues

- docker/for-mac#7341 — same symptom on macOS Docker Desktop
- docker/for-mac#7359 — layer not cached under containerd image store (fixed by increasing
  `defaultKeepStorage`, but that does not help here — layers are small)

## Workaround

Disable the containerd image store:

```json
{
  "features": {
    "containerd-snapshotter": false
  }
}
```

After changing `daemon.json` and restarting Docker, existing images are no longer available
(format is incompatible) and need to be rebuilt/re-pulled. Volumes are preserved.

## Exact-head checks

- save-context: CANCELLED
- save-context: SUCCESS
- save-context: SUCCESS
- validate (lint): SUCCESS
- zizmor / zizmor: SUCCESS
- validate (validate-go-mod): SUCCESS
- validate (validate-headers): SUCCESS
- validate (validate-docs): SUCCESS
- binary / prepare: SUCCESS
- binary / build (0, darwin/amd64, ubuntu-24.04): SUCCESS
- binary / build (1, darwin/arm64, ubuntu-24.04): SUCCESS
- binary / build (2, linux/amd64, ubuntu-24.04): SUCCESS
- binary / build (3, linux/arm/v6, ubuntu-24.04): SUCCESS
- binary / build (4, linux/arm/v7, ubuntu-24.04): SUCCESS
- binary / build (5, linux/arm64, ubuntu-24.04): SUCCESS
- binary / build (6, linux/ppc64le, ubuntu-24.04): SUCCESS
- binary / build (7, linux/riscv64, ubuntu-24.04): SUCCESS
- binary / build (8, linux/s390x, ubuntu-24.04): SUCCESS
- binary / build (9, windows/amd64, ubuntu-24.04): SUCCESS
- binary / build (10, windows/arm64, ubuntu-24.04): SUCCESS
- binary / finalize: SUCCESS
- bin-image-test / prepare: SUCCESS
- bin-image-test / build (0, darwin/amd64, ubuntu-24.04): SUCCESS
- bin-image-test / build (1, darwin/arm64, ubuntu-24.04): SUCCESS
- bin-image-test / build (2, linux/amd64, ubuntu-24.04): SUCCESS
- bin-image-test / build (3, linux/arm/v6, ubuntu-24.04): SUCCESS
- bin-image-test / build (4, linux/arm/v7, ubuntu-24.04): SUCCESS
- bin-image-test / build (5, linux/arm64, ubuntu-24.04): SUCCESS
- bin-image-test / build (6, linux/ppc64le, ubuntu-24.04): SUCCESS
- bin-image-test / build (7, linux/riscv64, ubuntu-24.04): SUCCESS
- bin-image-test / build (8, linux/s390x, ubuntu-24.04): SUCCESS
- bin-image-test / build (9, windows/amd64, ubuntu-24.04): SUCCESS
- bin-image-test / build (10, windows/arm64, ubuntu-24.04): SUCCESS
- bin-image-test / finalize: SUCCESS
- test: SUCCESS
- e2e (plugin, stable): SUCCESS
- e2e (standalone, stable): SUCCESS
- e2e (plugin, oldstable): SUCCESS
- e2e (standalone, oldstable): SUCCESS
- binary-finalize: SUCCESS
- coverage: SUCCESS
- release: SKIPPED
- zizmor: SUCCESS
- DCO: SUCCESS
- PR Review: SUCCESS
- codecov/patch: SUCCESS

## Changed files

- `pkg/compose/build.go`: +4/-1
- `pkg/compose/build_bake.go`: +21/-0
- `pkg/compose/images.go`: +70/-13
- `pkg/compose/images_test.go`: +161/-0
