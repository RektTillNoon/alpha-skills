# SEO/GEO Plugin Security

This plugin is public-safe by design. It contains instructions, metadata,
example evidence, and tests only. It must not contain real credentials, `.env`
files, `.mcp.json`, connector state, cookies, private URLs, customer data, or
provider-specific secret templates.

## Credential Handling

Credentials live in the host agent, user-configured connector, MCP server,
browser profile, provider CLI, or the user's own project environment. They are
not populated by this plugin and must not be copied into reports.

## Redaction Policy

Audit outputs must redact:

- credentials, tokens, cookies, private keys, and authorization headers
- private URLs, query strings, local machine paths, and customer identifiers
- personal data and proprietary internal excerpts
- analytics IDs, account IDs, client IDs, client secrets, and refresh tokens

If a finding depends on sensitive evidence, cite the evidence category, such as
`analytics export`, `access log sample`, or `connector result`, and summarize
the behavior without embedding raw values.

## Local Publish-Safety Proof

Run these checks before publishing:

```bash
python3 -B -m unittest clean-commit.tests.test_inspect_unstaged_changes tests.test_seo_geo_plugin_public_contract
gitleaks detect --source . --verbose
rg -n 'sk-[A-Za-z0-9_-]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|AIza[0-9A-Za-z_-]{35}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----' .agents .claude-plugin plugins/seo-geo README.md tests
rg -n "(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"][^'\"\n]{8,}['\"]" .agents .claude-plugin plugins/seo-geo README.md tests
```

`ggshield` is not part of the required proof because it sends file contents to
GitGuardian unless separately configured and approved by the user.

## Reporting Issues

If you find a credential or private artifact in this plugin, remove it from the
working tree, rotate the exposed credential if it was real, and report the file
path plus the redacted evidence pattern in the repository issue tracker.
