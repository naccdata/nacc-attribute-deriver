# Tech Stack

## Language & runtime

- Python, pinned to **3.12** (`interpreter_constraints = ["==3.12.*"]`).
- Runtime dependency: `pydantic>=2.10.6`. Tests use `pytest>=8.3.5`.

## Build system: Pants

This repo is managed by [Pants](https://www.pantsbuild.org/) 2.29. Source root is
the repo root; targets are declared in `BUILD` files throughout the tree. Enabled
backends: python, ruff (check + format), docformatter, mypy, shell, and ruff
formatting for BUILD files.

Dependencies are locked in `python-default.lock` (resolve name `python-default`).
Top-level requirements live in `requirements.txt` and are wired in via
`python_requirements` in the root `BUILD`.

## Code quality

- **Formatter/linter**: ruff (`ruff.toml`) — line length 88, 4-space indent,
  target `py312`. Lint rule sets: `A, B, E, W, F, I, RUF, SIM, C90, PLW0406,
  COM818, SLF001`. Tests ignore `I001` and `SLF001`.
- **Docstrings**: docformatter.
- **Types**: mypy. Keep code typed; the codebase uses explicit type hints
  throughout.

## Running commands (devcontainer + Pants)

Pants runs inside the devcontainer. Prefer the **kiro-pants-power** MCP tools
over raw shell — they manage the container lifecycle automatically. Every call
needs `workspace_folder` set to the absolute path of this repository's root on
your machine.

| Task | Tool | Equivalent Pants command |
| --- | --- | --- |
| Auto-format & fix | `pants_fix` | `pants fix ::` |
| Lint | `pants_lint` | `pants lint ::` |
| Type check | `pants_check` | `pants check ::` |
| Run tests | `pants_test` | `pants test ::` |
| Build dist | `pants_package` | `pants package ::` |
| Full gate | `full_quality_check` | fix → lint → check → test |
| Update BUILD files | `pants_tailor` | `pants tailor ::` |

Scope with `scope`/`path` (e.g. `scope="file"`,
`path="tests/attributes/.../test_x.py"`) or `test_filter` for pytest-style
name filtering. Use `::` to mean "this dir and everything under it".

**Before considering a change done, run `full_quality_check`** (or at least
`pants_fix`, then `pants_check` and `pants_test` on the affected targets).

## Releasing

Set the version in `nacc_attribute_deriver/BUILD`, then tag `vX.Y.Z` on `main`
and push the tag — `.github/workflows/build.yml` builds and publishes. See the
README.
