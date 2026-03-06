# Release Checklist

Use this checklist to capture release evidence for each cut. Keep links immutable and tied to a
single execution so reviewers can audit evidence later.

## CI run IDs

> Do **not** use branch-query links such as
> `actions/workflows/ci.yml?query=branch%3Amain`; those links are moving targets.

Record direct run URLs in the form `https://github.com/<owner>/<repo>/actions/runs/<run_id>`.

- Build & test (CI): https://github.com/<owner>/<repo>/actions/runs/<CI_RUN_ID>
- Security checks: https://github.com/<owner>/<repo>/actions/runs/<SECURITY_RUN_ID>
- Release publish: https://github.com/<owner>/<repo>/actions/runs/<RELEASE_RUN_ID>

## Pre-release

- [ ] Version number bumped.
- [ ] Changelog updated.
- [ ] Release notes drafted.
- [ ] Migration notes written (if needed).

## Validation

- [ ] Unit tests pass.
- [ ] Integration tests pass.
- [ ] Manual smoke test completed.
- [ ] Docs updated for user-visible changes.

## Artifacts

- [ ] Container image digest recorded.
- [ ] Binary/checksum artifacts recorded.
- [ ] SBOM attached.

## Sign-off

- [ ] Engineering approver.
- [ ] Security approver.
- [ ] Product approver.

---

Before marking complete, substitute final GitHub Actions run IDs for every `<..._RUN_ID>` placeholder
above so each evidence link points to one immutable execution.
