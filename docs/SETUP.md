# GitHub profile setup — organized

This is the source for the GitHub profile repository
`parigalaprashanthkumarkvsr-code/parigalaprashanthkumarkvsr-code`
(a public repo with exactly the same name as the username, rendered on the profile).

## Required layout (root)

```text
README.md
assets/profile-dashboard.png
assets/sysinfo.svg
assets/portrait.svg
assets/graph.svg
tools/
docs/SETUP.md
.github/workflows/refresh-graph.yml
```

GitHub renders `README.md` from the repository root. The hero banner uses a
relative path (`./assets/profile-dashboard.png`), so the whole `assets/` folder
must be committed.

## Publish / update

```powershell
git add README.md assets/ tools/ docs/ .github/
git commit -m "Organize profile: dashboard, fixed links, living graph"
git push origin main
```

## Notes

- Account is `parigalaprashanthkumarkvsr-code`. All project links in `README.md`
  were fixed from the old typo `parigalaprashanthkumsvr-code`.
- `tools/pull_contributions.py` and `tools/render_portrait.py` now use the
  correct `USER="parigalaprashanthkumarkvsr-code"`.
- `tools/render_graph.py` writes to `assets/graph.svg` (was `graph.svg`).
  Workflow `refresh-graph.yml` commits `assets/contributions.json` + `assets/graph.svg`.
- Stats cards (`github-readme-stats`, streak) are live images keyed by username.
- Dashboard artwork contains illustrative graphics, not live GitHub numbers.
  Live numbers come from the stats cards + auto-refreshed `assets/graph.svg`.
