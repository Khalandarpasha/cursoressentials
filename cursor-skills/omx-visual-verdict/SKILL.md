---
name: omx-visual-verdict
description: >-
  Structured visual QA verdict for screenshot-to-reference comparisons, returning strict JSON pass/fail guidance. Adapted for Cursor agent use.
---
# Visual Verdict (ported from OmX $visual-verdict)

## Purpose
Compare generated UI screenshots against one or more reference images and return a strict JSON verdict that can drive the next edit iteration.

## When to Use
- The task includes visual fidelity requirements (layout, spacing, typography, component styling)
- You have a generated screenshot and at least one reference image
- You need deterministic pass/fail guidance before continuing edits

## When Not to Use
- No reference images are available for comparison
- The task is purely functional with no visual requirements
- Text-only output verification (use tests instead)

## Rules

- Return **JSON only** as the verdict with the exact shape specified in the Output Contract
- `score`: integer 0-100
- `verdict`: short status — `pass`, `revise`, or `fail`
- `category_match`: `true` when the generated screenshot matches the intended UI category/style
- `differences[]`: concrete visual mismatches (layout, spacing, typography, colors, hierarchy)
- `suggestions[]`: actionable next edits tied to the differences
- `reasoning`: 1-2 sentence summary
- Target pass threshold is **90+**
- If `score < 90`, continue editing and rerun visual-verdict before any further code edits in the next iteration

## Workflow

### Inputs
- `reference_images[]` — one or more image paths for the target design
- `generated_screenshot` — current output image
- Optional: `category_hint` (e.g., `hackernews`, `sns-feed`, `dashboard`)

### Evaluation
1. Compare the generated screenshot against all reference images
2. Assess layout structure, spacing, typography, colors, and component hierarchy
3. Identify concrete visual mismatches
4. Generate actionable suggestions for each difference
5. Compute an overall score (0-100)

### Iteration Loop
- If `score < 90`, the verdict is `revise` — apply suggestions and re-verify
- Continue the edit-verify loop until score >= 90 or the user accepts current state

### Debug Visualization
When mismatch diagnosis is hard:
1. Keep visual-verdict as the authoritative decision
2. Use pixel-level diff tooling (pixel diff / pixelmatch overlay) as a **secondary debug aid** to localize hotspots
3. Convert pixel diff hotspots into concrete `differences[]` and `suggestions[]` updates

## Tools

- **Read tool**: Read reference and generated image files for comparison
- **Shell tool**: Run pixel diff tools or screenshot capture commands if needed
- **StrReplace tool**: Apply CSS/layout fixes based on verdict suggestions

## Output Contract

```json
{
  "score": 0,
  "verdict": "revise",
  "category_match": false,
  "differences": ["..."],
  "suggestions": ["..."],
  "reasoning": "short explanation"
}
```

## Examples

```json
{
  "score": 87,
  "verdict": "revise",
  "category_match": true,
  "differences": [
    "Top nav spacing is tighter than reference",
    "Primary button uses smaller font weight"
  ],
  "suggestions": [
    "Increase nav item horizontal padding by 4px",
    "Set primary button font-weight to 600"
  ],
  "reasoning": "Core layout matches, but style details still diverge."
}
```

## Completion Criteria
- A JSON verdict has been emitted with all required fields
- Score >= 90 (pass threshold), or all actionable suggestions have been applied and re-verified
- Differences list is concrete and tied to specific visual elements
- Suggestions are actionable edits that can be directly applied
