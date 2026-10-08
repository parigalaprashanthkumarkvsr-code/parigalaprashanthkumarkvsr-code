# Setup and customization

1. Create a **public GitHub repository named exactly your GitHub username** to display this README on your GitHub profile. For an ordinary repo, choose any name.
2. Extract this ZIP and push its contents to the repository root. The default README will render without any build step.
3. Check `README.md`, `assets/source/original.svg`, and `scripts/build.py` to customize the name, titles, and project entries. `scripts/build.py` regenerates the SVG panels from the source.
4. To regenerate SVG assets, install Python 3 and `pip install -r requirements.txt`, then run `npm run build` (or `python scripts/build.py`).
5. Test paths using `npm run check` and inspect SVG rendering in your browser or GitHub.
6. The source includes an illustrative radar and originally contained invented-looking star totals and a learner score. Those numbers are suppressed in the module exports. Do **not** treat the radar chart as an objective assessment.
7. GitHub README files **do not execute JavaScript**. The JS build/check scripts run locally, not on your profile. SVGs are committed as standalone image files.

## Panels

- `header.svg`: headline and summary
- `visual-identity.svg`: abstract blue spider-style emblem
- `about-me.svg`: biography
- `builder-index.svg`: illustrative radar
- `current-focus.svg`: interests
- `featured-projects.svg`: editable project directory illustration
- `tech-stack.svg`: technologies
- `learning-log.svg`: learning timeline
- `mission.svg`: personal motto
- `featured-handle.svg`: terminal handle card
- `full-profile.svg`: optional combined original artwork

## Important

The supplied graphic includes sample project names and counts. This package keeps project names as design content, not verified GitHub repository references, and clears the sample numeric star totals. Also confirm the intended username: the uploaded SVG uses two slightly different handle spellings. This export uses `parigalaprashanthkumarkvsr-code` from the top-right label throughout the modular elements.
