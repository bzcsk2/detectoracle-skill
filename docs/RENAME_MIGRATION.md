# DetectorOracle Rename Migration

This project was renamed from **IssueOracle** to **DetectorOracle**.

## Public contract

The public project identity is now:

- Repository: `bzcsk2/detectoracle-skill`
- Skill name: `detectoracle`
- User-facing invocation: `/detectoracle ...`
- Built artifact: `dist/detectoracle.skill`
- Skill directory: `skills/detectoracle`
- Preferred user data directory: `~/.detectoracle`
- Preferred configuration directory: `~/.config/detectoracle`
- Preferred environment variables: `DETECTORACLE_*`
- Canonical mined experience path: `~/.detectoracle/bugplay/experience.json`

## Compatibility contract

The following legacy names are intentionally still accepted during the migration window:

- Python compatibility module: `skills/detectoracle/scripts/issueoracle.py`
- Legacy user data directory: `~/.issueoracle`
- Legacy configuration directory: `~/.config/issueoracle`
- Legacy environment variables: `ISSUEORACLE_*`
- Legacy mined experience path: `~/.detectoracle/bugplay/candidates/experience.json`

This avoids breaking existing local installs or losing previously mined bug-experience data.

## Migration policy

1. New docs, CLI examples, marketplace-facing metadata, and generated artifacts should use DetectorOracle.
2. Existing users should not be forced to move data manually.
3. Compatibility aliases may stay until a future major-version cleanup.
4. Any future removal of `issueoracle.py` or `ISSUEORACLE_*` must include explicit release notes and migration tests.

## Current known limitation

The canonical shell/script entrypoint is `detectoracle.py`, but the core implementation module is still named `issueoracle.py` for compatibility. This is acceptable for the 0.4.x migration window; future cleanup should move the CLI implementation into a neutral module such as `lib.cli`.
