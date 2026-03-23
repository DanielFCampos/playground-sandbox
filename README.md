# Python Sandbox

A Podman-based VS Code Dev Container that serves as a disposable Python sandbox. Designed for **AI isolation** — give GitHub Copilot full powers inside the container without risking your host machine.

Lightweight (~350-400 MB), fully transparent (custom Dockerfile, no opaque base images), and respawnable — delete and recreate it whenever you want a clean slate.

## What's Inside

| Component | Version | Notes |
|-----------|---------|-------|
| **Python** | 3.13 | `python:3.13-slim` base (Debian Bookworm) |
| **UV** | latest | Installed via official script; fast Python package manager |
| **Node.js** | 22 LTS | Via NodeSource |
| **GitHub CLI** | latest | Official APT repo |
| **git** | latest | System package |
| **User** | `vscode` (UID 1000) | Non-root, passwordless `sudo` |

## Prerequisites

1. **Podman** installed and running (rootless mode)
2. **VS Code** with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension

> **Note:** You may need to set `"dev.containers.dockerPath": "podman"` in VS Code settings if the extension doesn't auto-detect Podman.

## Getting Started

1. Clone this repository
2. Open the folder in VS Code
3. When prompted, click **"Reopen in Container"** — or run the command `Dev Containers: Reopen in Container` from the Command Palette
4. Wait for the build to finish — on first run, Podman builds the image from the Dockerfile

Once the container is up, a `postCreateCommand` prints all tool versions to confirm everything is working:

```
python --version && node --version && uv --version && gh --version && git --version
```

### Workspace Mount

The host's `shared/` folder is bind-mounted into the container at `/workspace`. This is your working directory inside the container — files you create there are visible on the host, and vice versa.

### Keeping the Container Running

By default, VS Code **stops** the container when you close the window. The next time you reopen the folder, the container has to start up again before you can work.

To keep the container running in the background after you disconnect, add `shutdownAction` to `.devcontainer/devcontainer.json`:

```jsonc
{
    "name": "Python Sandbox",
    // ... existing configuration ...
    "shutdownAction": "none"
}
```

With this setting, closing VS Code leaves the container alive. Reconnecting is nearly instant — just open the folder and click **"Reopen in Container"**, or run `Dev Containers: Reopen in Container` from the Command Palette.

When you want to free resources, stop the container manually:

```bash
# Podman
podman stop <container-name>

# Docker
docker stop <container-name>
```

> **Note:** The container does **not** survive a host reboot. After restarting your machine, the container will need to start again as usual.

## How To: Clone, Detach, and Connect to Your Own Repo

If you want to use this project as a starting point for your own sandbox, follow these steps to clone it, remove the link to the original repository, and optionally connect it to a new one.

### 1. Clone the repository

```bash
git clone <repository_url>
```

Replace `<repository_url>` with the HTTPS or SSH URL of this repository.

### 2. Navigate into the cloned directory

```bash
cd <repository_name>
```

### 3. Verify the current remote(s)

```bash
git remote -v
```

You should see something like:

```
origin  <repository_url> (fetch)
origin  <repository_url> (push)
```

### 4. Remove the origin remote

```bash
git remote rm origin
```

### 5. Verify the detachment

```bash
git remote -v
```

This should return no output, confirming your local repository is no longer linked to the original remote.

### 6. (Optional) Connect to a new remote repository

Create a new empty repository on GitHub/GitLab, then add it as the new origin:

```bash
git remote add origin <new_repository_url>
git push -u origin main
```

Your local copy is now an independent repository. You can commit, push, and pull against your own remote without any connection to the original source.

## VS Code Extensions

These workspace extensions are pre-installed inside the container:

| Extension | ID |
|-----------|----|
| Python | `ms-python.python` |
| Pylance | `ms-python.vscode-pylance` |
| debugpy | `ms-python.debugpy` |
| Jupyter | `ms-toolsai.jupyter` |
| GitHub Copilot | `github.copilot` |
| GitHub Copilot Chat | `github.copilot-chat` |
| GitLens | `eamodio.gitlens` |
| Ruff | `charliermarsh.ruff` |
| SQLTools | `mtxr.sqltools` |

**Ruff** is configured as the default Python formatter with format-on-save enabled.

## Extending Usage

### GitHub Copilot CLI

The `gh-copilot` extension is auto-installed every time the container starts (via `postStartCommand`). To use it:

```bash
# Authenticate with GitHub (one-time — credentials persist across rebuilds)
gh auth login

# Use Copilot in the terminal
gh copilot suggest "undo the last git commit"
gh copilot explain "git diff --staged"
```

Authentication is stored in a named Podman volume (`sandbox-gh-config`), so it survives container rebuilds. You only need to re-authenticate if the volume is deleted.

### Playwright + Chromium

Playwright and Chromium are **not pre-installed** to keep the image lean. Install them on-demand when needed:

```bash
uv pip install playwright && playwright install --with-deps chromium
```

This installs the Playwright Python package and downloads a bundled Chromium binary with all required system dependencies.

## Built-in Skills, Instructions & Agents

The `shared/` folder ships with pre-configured customizations for GitHub Copilot and Claude that are active inside the container workspace.

### GitHub Copilot Customizations (`shared/.github/`)

| Type | File | Description |
|------|------|-------------|
| Instructions | `copilot-instructions.md` | Always-on clean code principles (naming, functions, simplicity, error handling) |
| Instructions | `instructions/python.instructions.md` | Python standards — PEP 8, type hints, pytest |
| Instructions | `instructions/typescript.instructions.md` | TypeScript/JS standards — ESM, React, camelCase |
| Instructions | `instructions/sql.instructions.md` | SQL standards — naming, explicit JOINs, parameterized queries |
| Agent | `agents/brainstorm.agent.md` | Adversarial brainstorming agent with 10 personas |
| Prompt | `prompts/code-review.prompt.md` | Code review checklist |
| Skill | `skills/pytest-tests/` | Pytest test generation |

### Claude Skills (`shared/.claude/skills/`)

17 installable skills covering docs, design, testing, and more:

`algorithmic-art` · `brand-guidelines` · `canvas-design` · `claude-api` · `doc-coauthoring` · `docx` · `frontend-design` · `internal-comms` · `mcp-builder` · `pdf` · `pptx` · `skill-creator` · `slack-gif-creator` · `theme-factory` · `web-artifacts-builder` · `webapp-testing` · `xlsx`

## Using Docker Instead of Podman

This dev container is configured for **Podman** (rootless mode) by default. If you need to use **Docker** instead, make two changes in `.devcontainer/devcontainer.json`:

1. **Remove** the `runArgs` block:
    ```jsonc
    // DELETE these lines
    "runArgs": [
        "--userns=keep-id",
        "--security-opt=label=disable"
    ],
    ```

2. **Change** `updateRemoteUserUID` from `false` to `true`:
    ```jsonc
    "updateRemoteUserUID": true,
    ```

**Why?** `--userns=keep-id` is a Podman-only flag that maps your host UID into the container so bind-mounted files in `shared/` have correct ownership. Docker doesn't support this flag, but its `updateRemoteUserUID` setting solves the same problem — it rewrites the container user's UID to match the host user at startup.

`--security-opt=label=disable` disables SELinux label enforcement for bind mounts. Docker accepts this flag but it's unnecessary unless you're on an SELinux-enabled host (Fedora/RHEL), so it can safely be removed.

Everything else (Dockerfile, mounts, extensions, commands) works identically on both engines.

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Custom Dockerfile over predefined images | Full transparency for AI isolation; ~350-400 MB vs 1.2 GB+ |
| `--userns=keep-id` | Maps host UID into container — fixes bind mount permissions with rootless Podman |
| `--security-opt=label=disable` | Disables SELinux label enforcement — avoids bind mount access issues (harmless on non-SELinux systems) |
| Named volume for gh CLI auth | Credentials persist across container rebuilds without leaking to host |
| Filesystem isolation only | No network restrictions — sufficient for current threat model (AI agent sandboxed from host filesystem) |
| Shared folder scoped to `shared/` | Intentionally narrow — not home or Desktop. This is the only escape hatch between host and container. |
| Playwright not pre-installed | Keeps image lean; Chromium + deps add ~400 MB that aren't always needed |

## Maintenance

You own the Dockerfile. Periodically update:

- **Base image**: `python:3.13-slim` → newer patch/minor versions
- **Node.js**: bump the NodeSource setup script version
- **UV**: pinned via install script (uses latest by default)
- **GitHub CLI**: pulled from official APT repo (gets latest on rebuild)

Rebuild the container after updates: `Dev Containers: Rebuild Container` from the Command Palette.
