# Release procedure

1. Complete each scoped PR with final diff review and `make verify-release`.
2. Require successful Carbon Budget Gate, Release Validation, docs checks and
   CodeQL for the reviewed PR head. Do not bypass a failing check.
3. Merge to main and wait for post-merge CI/CodeQL and Pages deployment.
4. Verify desktop/mobile dashboard, tabs, evidence values and console health.
5. Check license provenance, third-party notices, changelog and release scope.
6. Record the final main SHA. Create the version tag on that exact SHA only.
7. Publish release notes with changes, verification and material limitations.
8. Verify tag → SHA, published status and Latest. Preserve historical releases.

For each BSL-covered version, record its first public distribution date and
Change Date no later than its fourth anniversary. Do not restart the clock by
retagging or republishing the same version. Earlier MIT grants remain valid.

Optional Azure deployment is a separate operator action. A software release
must not claim endpoint health or real LLM inference without direct evidence.
