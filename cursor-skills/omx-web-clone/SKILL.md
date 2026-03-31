---
name: omx-web-clone
description: >-
  URL-driven website cloning with visual and functional verification using browser automation and iterative refinement. Adapted for Cursor agent use.
---
# Web Clone (ported from OmX $web-clone)

## Purpose
Clone a target website from its URL, replicating both visual appearance and core interactive functionality. Uses browser automation for live page extraction, code generation, and iterative verification with the omx-visual-verdict skill for visual scoring.

## When to Use
- User provides a target URL and wants the site replicated as working code
- User says "clone site", "clone website", "copy webpage", or "web-clone"
- Task requires both visual fidelity AND functional parity with the original
- Reference is a live URL (not a static screenshot — use omx-visual-verdict skill for screenshot-only tasks)

## When Not to Use
- User only has screenshot references without a live URL — use omx-visual-verdict skill directly
- User wants to modify, redesign, or "improve" the site — use standard implementation flow
- Target requires authentication, payment flows, or backend API parity — out of scope for v1
- Multi-page / multi-route deep cloning — v1 handles single-page scope only

## Why This Matters
Website cloning requires extracting structure, styles, and interactions from a live page and faithfully reproducing them in code. This skill provides a structured 5-pass pipeline that ensures both visual fidelity and functional correctness through iterative verification.

## Rules

- **Legal notice**: Only clone sites you own or have explicit permission to replicate. Respect copyright and trademarks.
- Browser automation tools must be available for this skill to work.
- Use accessibility snapshots for structural understanding — they are far more token-efficient than screenshots.
- Take screenshots only when visual verification is needed (Pass 1 baseline, Pass 4 comparison).
- Skip external consultation for straightforward extraction; use it only if verification repeatedly fails on the same issue.

### Scope Limits (v1)

**Included:**
- Layout structure (header, nav, content areas, sidebar, footer)
- Typography (font families, sizes, weights, line heights)
- Colors, spacing, borders, border-radius
- Core interactions: navigation links, buttons, form elements, dropdowns, modals, toggles
- Responsive hints from the extracted layout (flexbox/grid patterns)

**Excluded:**
- Backend API integration or data fetching
- Authentication flows or protected content
- Dynamic/personalized content (user-specific data)
- Multi-page crawling or route graph cloning
- Third-party widget functionality (maps, embeds, chat widgets)
- Image/asset replication (use placeholders for external images)

### Context Budget
Pass 1 extraction can produce very large data. Apply these limits proactively:
- **DOM tree**: If the serialized JSON exceeds ~30KB, reduce depth from 8 to 4 and re-extract
- **Accessibility snapshot**: If it exceeds ~20KB, summarize key landmarks rather than keeping the full tree
- **Interactive elements**: Cap at 50 elements. If more exist, keep only visible ones
- **Total extraction context**: Aim for under 60KB combined
- **Screenshots**: Take one baseline in Pass 1 and one comparison in Pass 4. Do not take screenshots between iterations unless debugging a specific region

## Workflow

### Inputs
- `target_url` (required): The URL to clone
- `output_dir` (optional, default: current working directory): Where to generate the clone project
- `tech_stack` (optional, inferred from project context): HTML/CSS/JS, React, Vue, Svelte, etc.

### Pass 1 — Extract

Capture the target page's structure, styles, interactions, and visual baseline.

1. **Navigate**: Use browser automation to navigate to `target_url`
2. **Wait for render**: Wait for the page to fully render (network idle or timeout of 5s)
3. **Accessibility snapshot**: Capture the semantic tree (roles, names, values, interactive states) — primary structural reference
4. **Full-page screenshot**: Save as reference baseline `target-full.png`
5. **DOM + computed styles**: Extract using this script:
   ```javascript
   (() => {
     const walk = (el, depth = 0) => {
       if (depth > 8 || !el.tagName) return null;
       const cs = window.getComputedStyle(el);
       return {
         tag: el.tagName.toLowerCase(),
         id: el.id || undefined,
         classes: [...el.classList].slice(0, 5),
         styles: {
           display: cs.display, position: cs.position,
           width: cs.width, height: cs.height,
           padding: cs.padding, margin: cs.margin,
           fontSize: cs.fontSize, fontFamily: cs.fontFamily,
           fontWeight: cs.fontWeight, lineHeight: cs.lineHeight,
           color: cs.color, backgroundColor: cs.backgroundColor,
           border: cs.border, borderRadius: cs.borderRadius,
           flexDirection: cs.flexDirection, justifyContent: cs.justifyContent,
           alignItems: cs.alignItems, gap: cs.gap,
           gridTemplateColumns: cs.gridTemplateColumns,
         },
         text: el.childNodes.length === 1 && el.childNodes[0].nodeType === 3
           ? el.textContent?.trim().slice(0, 100) : undefined,
         children: [...el.children].map(c => walk(c, depth + 1)).filter(Boolean),
       };
     };
     return walk(document.body);
   })()
   ```
6. **Interactive elements**: Extract using this script:
   ```javascript
   (() => {
     const results = [];
     document.querySelectorAll(
       'button, a[href], input, select, textarea, [role="button"], ' +
       '[onclick], [aria-haspopup], [aria-expanded], details, dialog'
     ).forEach(el => {
       results.push({
         tag: el.tagName.toLowerCase(),
         type: el.type || el.getAttribute('role') || 'interactive',
         text: (el.textContent || '').trim().slice(0, 80),
         href: el.href || undefined,
         ariaLabel: el.getAttribute('aria-label') || undefined,
         isVisible: el.offsetParent !== null,
       });
     });
     return results;
   })()
   ```
7. **Network patterns** (optional): Note XHR/fetch calls for reference. Do not attempt to replicate backends.

### Pass 2 — Build Plan

Analyze extraction results and decompose into a component plan.

1. **Identify page regions**: From DOM tree + accessibility snapshot, identify major sections:
   - Navigation bar / header
   - Hero / banner section
   - Main content area(s)
   - Sidebar (if present)
   - Footer
   - Overlay elements (modals, drawers)

2. **Map components**: For each region, define:
   - Component name and responsibility
   - Key style properties (from computed styles)
   - Content summary (headings, text, images)
   - Child components if nested

3. **Create interaction map**: From interactive elements list:
   - Navigation links → anchor tags with `href`
   - Form elements → proper `<form>` with inputs, labels, validation
   - Buttons → click handlers (toggle, submit, navigate)
   - Dropdowns/modals → show/hide toggle with transitions
   - Accordions/tabs → state-based visibility

4. **Extract design tokens**: Identify recurring values:
   - Color palette (primary, secondary, background, text colors)
   - Font stack (families, size scale, weight scale)
   - Spacing scale (padding/margin patterns)
   - Border radius values

5. **Define file structure**:
   ```
   {output_dir}/
   ├── index.html          (or App.tsx / App.vue)
   ├── styles/
   │   ├── globals.css      (reset + tokens)
   │   └── components.css   (or scoped styles)
   ├── scripts/
   │   └── interactions.js  (toggle, modal, dropdown logic)
   └── assets/              (placeholder images)
   ```
   Adapt to `tech_stack` if specified (React components, Vue SFCs, etc.).

### Pass 3 — Generate Clone

Implement the clone from the plan. Work component-by-component.

1. **Scaffold**: Create the directory structure and base files
2. **Design tokens first**: Implement CSS custom properties or Tailwind config from extracted tokens
3. **Layout shell**: Build the page-level layout matching the original's flexbox/grid structure
4. **Components**: Implement each region top-down:
   - Match DOM structure from extraction (semantic tags, landmark roles)
   - Apply computed styles — prioritize layout properties, then typography, then decorative
   - Use actual extracted text content; use placeholder `<img>` for external images
5. **Interactions**: Wire up detected behaviors:
   - Navigation: working `<a>` tags (to `#` anchors or stubs for v1)
   - Forms: proper structure with `<label>`, input types, placeholder text
   - Toggles: JavaScript for dropdowns, modals, accordions
   - Hover/focus states: CSS transitions matching original behavior
6. **Responsive**: If the original uses responsive breakpoints, add basic responsive rules

### Pass 4 — Verify

Compare the clone against the original across three dimensions.

1. **Serve the clone**: Start a local server:
   ```bash
   npx serve {output_dir} -l 3456 --no-clipboard
   ```
   Fallback: `python3 -m http.server 3456 -d {output_dir}`

2. **Visual verification**:
   - Navigate to clone URL with browser automation
   - Take full-page screenshot of clone
   - Run omx-visual-verdict skill with reference and generated screenshots
   - Visual pass threshold: **score >= 85**

3. **Structural verification**: Compare landmark counts:
   - Count `<nav>`, `<main>`, `<footer>`, `<form>`, `<button>`, `<a>` in both original and clone
   - Structure passes when all major landmarks exist

4. **Functional spot-check**: Test 2-3 detected interactions via browser automation:
   - Click a navigation link → verify URL change or scroll behavior
   - Toggle a dropdown/modal → verify visibility change
   - Interact with a form field → verify it accepts input

5. **Emit composite verdict** (see Output Contract below)

### Pass 5 — Iterate

Fix highest-impact issues and re-verify.

1. **Prioritize fixes** by impact: layout > interactions > spacing > typography > colors
2. **Apply targeted edits**: Fix only the issues listed in `priority_fixes`. Do not refactor working code
3. **Re-verify**: Repeat Pass 4
4. **Loop**: Continue until `overall_verdict` is `pass` OR max **5 iterations** reached
5. **Final report**: Summarize what was successfully cloned, any remaining differences, and elements that could not be replicated

## Tools

- **Shell tool**: Serve the clone locally, run build commands, install dependencies
- **Write tool**: Create new project files (HTML, CSS, JS) for the clone scaffold
- **StrReplace tool**: Apply targeted fixes during iteration passes
- **Read tool**: Read extraction data and reference files
- **Task tool (browser-use subagent)**: Browser automation for page navigation, screenshots, accessibility snapshots, DOM extraction, and functional spot-checks
- **Task tool (subagent)**: Delegate component generation or parallel implementation tasks

## Output Contract

After each verification pass, emit a **composite web-clone verdict** JSON:

```json
{
  "visual": {
    "score": 0,
    "verdict": "revise",
    "category_match": false,
    "differences": ["..."],
    "suggestions": ["..."],
    "reasoning": "short explanation"
  },
  "functional": {
    "tested": 0,
    "passed": 0,
    "failures": ["..."]
  },
  "structure": {
    "landmark_match": false,
    "missing": ["..."],
    "extra": ["..."]
  },
  "overall_verdict": "revise",
  "priority_fixes": ["..."]
}
```

Rules:
- `visual` follows the VisualVerdict shape from omx-visual-verdict skill
- `functional.tested/passed` are counts; `failures` list specific interaction failures
- `structure.landmark_match` is `true` when all major HTML landmarks (nav, main, footer, forms) are present
- `overall_verdict`: `pass` when visual.score >= 85 AND functional.failures is empty AND structure.landmark_match is true
- `priority_fixes`: ordered by impact, drives the next iteration

## Examples

**User**: "Clone https://news.ycombinator.com"

**Pass 1**: Navigate to HN. Extract: table-based layout, orange (#ff6600) nav bar, story list with links + points + comments, footer. Screenshot saved.

**Pass 2**: Regions: nav bar (logo + links), story table (30 rows x title + meta), footer. Tokens: orange #ff6600, gray #828282, Verdana font, 10pt base. Interaction map: story links (external), comment links, "more" pagination.

**Pass 3**: Generate index.html with HN-style table layout, CSS matching extracted colors/fonts, working `<a>` tags for stories.

**Pass 4**: Visual score=78 (font size off, spacing between stories too tight). Functional 2/2 (links work). Structure match=true.

**Pass 5 iteration 1**: Fix font to Verdana 10pt, increase row padding → score=88. Functional 2/2. Structure match. → `overall_verdict: pass`. Done.

## Checklist
- [ ] Pass 1 extraction completed and summarized (screenshot + accessibility tree + DOM styles + interactions)
- [ ] Pass 2 component plan created with file structure
- [ ] Pass 3 clone generated and files written to `output_dir`
- [ ] Clone serves locally without errors
- [ ] Pass 4 composite verdict emitted with all three dimensions
- [ ] `overall_verdict` is `pass`, or max 5 iterations reached with best-effort report

## Appendix

### Iteration Thresholds
- **Visual pass**: score >= 85
- **Functional pass**: zero failures on tested interactions
- **Structure pass**: all major landmarks present
- **Overall pass**: all three dimensions pass
- **Max iterations**: 5 (report best achieved result if threshold not met)

### Error Handling
- **Browser tools unavailable**: Stop. Instruct user to configure browser automation. Do not attempt to clone without browser tools.
- **Page fails to load**: Report the URL and HTTP status. Suggest the user verify the URL is accessible.
- **DOM extraction returns empty**: The page may use heavy client-side rendering. Wait longer and retry once.
- **Visual score stuck below threshold after 3 iterations**: Report the current state as best-effort. List the unresolved differences for the user.
- **Extraction data too large for context**: Truncate deep DOM branches (depth > 6). Focus on top-level structure and defer nested details to iteration fixes.
