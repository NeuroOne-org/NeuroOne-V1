# NeuroOne Frontend — Design System

The reference for how this app looks and moves. It describes what is already
built in `frontend/src`, so that new screens extend the system rather than
starting a second one beside it.

> **Scope.** `frontend/web-page/` is a separate Next project with its own
> design language. Nothing in this document applies to it, and nothing in it
> should be copied into here.

---

## 1. The idea

An instrument panel, not a consumer dashboard.

The product estimates disease stage from an MRI and has to be legible to a
clinician under time pressure. That sets three rules that override taste:

1. **Data is the brightest thing on screen.** Chrome recedes; numbers,
   findings and patient names do not.
2. **Nothing is invented.** Every figure on screen traces to a backend field.
   Where a number is unknown, the UI shows an em dash — never a zero, never a
   plausible placeholder.
3. **The model advises, the clinician decides.** Confidence is always shown
   with its likelihood band and its disclaimer, never as a verdict.

Ambient motion (drifting glows, the tilting neural network, the scan line)
belongs on the marketing and auth surfaces. Inside the dashboard the
background is flat and still.

---

## 2. Color

Semantic tokens, defined as channel triplets in `globals.css` and exposed to
Tailwind through `tailwind.config.ts`. **Use the token, never a hex.** Every
token resolves in both themes, so `bg-panel` is correct in light and dark and
no component needs a `dark:` variant.

```css
:root  { --panel: 255 255 255; }   /* light is the base */
.dark  { --panel:  20  23  27; }   /* dark overrides it */
```

```ts
panel: "rgb(var(--panel) / <alpha-value>)"   // keeps bg-panel/60 working
```

Because the overrides hang off a class rather than a media query, putting
`dark` on any element re-themes that subtree alone. That is how the auth and
landing surfaces stay dark while the dashboard follows the user.

The table below lists the **dark** values, which remain the product's default.

### Surfaces

| Token | Hex | Use |
| --- | --- | --- |
| `ink` | `#0B0D10` | Page background |
| `panel` | `#14171B` | Cards, sidebar — one step up from the page |
| `raised` | `#1B1F24` | Inputs, chips, avatars — one step up from a card |
| `line` | `#262B31` | Every border and divider |
| `line-soft` | `#1D2126` | Dial tracks and other interior rules |

In light these invert: `panel` becomes white and sits *above* `ink`, while
`raised` is a light grey. The role of each token — page, card, control — does
not change, only its lightness.

Three surface levels, in that order, and no more. Depth comes from the step
between them, not from shadows — the app uses no drop shadows.

### Text

| Token | Hex | Use |
| --- | --- | --- |
| `text` | `#E7E9EC` | Primary — values, names, headings |
| `text-muted` | `#8A9099` | Secondary — labels, prose, descriptions |
| `text-faint` | `#565C66` | Tertiary — eyebrows, timestamps, hints |

### Accents

Each accent carries one meaning. A `-soft` variant (10% alpha) is the fill
that goes with it; `/30` is the border.

| Token | Hex | Means |
| --- | --- | --- |
| `teal` | `#35D6C8` | Confirmed, healthy, signed off, brand mark |
| `indigo` | `#6E7BFF` | Interactive — primary buttons, links, focus, active nav |
| `amber` | `#FF6A3D` | Attention — errors, worsening trends, high likelihood |

The accents are darkened in light mode (`--amber: 186 60 22`, and so on); the
dark-mode values sit near 2:1 on white and would fail outright as text.

**Light-mode tokens are pinned to measured contrast**, not picked by eye — the
values in `globals.css` carry their ratio in a comment. `text-faint` is the one
to watch: it carries 11px eyebrow labels, so it is held at ~5:1 where a purely
visual choice lands around 3.3:1 and fails AA.

> Known gap: `--text-faint` in **dark** mode is 2.67:1 on `panel`. It predates
> the light theme and is deliberate recession on the auth hero, but it fails AA
> wherever it carries a real label. Raising it to about `120 127 138` would
> reach 4.5:1.

Never use an accent decoratively. Amber on screen means something needs a
clinician; if it is used for flair it stops meaning that.

---

## 3. Typography

Three families, loaded in `src/app/layout.tsx`:

| Family | Font | Used for |
| --- | --- | --- |
| `font-display` | Space Grotesk | Headings, brand, card titles |
| `font-body` | Inter | Everything else |
| `font-mono` | IBM Plex Mono | All numbers, IDs, timestamps, eyebrows |

**Every number is mono and tabular.** Use the `.data-num` component class
(`font-mono tabular-nums`) so that figures do not jitter as they change.

### Scale

The UI is deliberately small and dense; the auth hero is the one place that
is not.

| Role | Size | Notes |
| --- | --- | --- |
| Auth hero headline | `42px` / `48px` at `xl` | `leading-[1.15]`, `tracking-[-0.02em]` |
| Auth hero body | `19px` | `leading-relaxed` |
| Page title | `text-2xl` | `font-display font-medium` |
| Card title | `text-[15px]` | `font-display font-medium` |
| Body | `text-sm` (14px) | |
| Secondary | `text-[13px]` | Table cells, form labels, links |
| Meta | `text-[12px]` | Timestamps, hints |
| Eyebrow / badge | `text-[11px]` | Mono, uppercase, `tracking-[0.14em]` |

Use the `.label-eyebrow` class for section eyebrows rather than rebuilding
the mono/uppercase/tracking stack each time.

---

## 4. Shape and spacing

Radii are small — `4px` / `6px` / `8px` / `12px`. Nothing is a pill except
the progress bars and avatars. Rounded-2xl belongs to a different product.

Standard paddings: cards `p-5`, card headers `px-5 py-4`, table cells
`px-5 py-3.5`, page gutters `px-8 py-8`.

Content widths: dashboard `max-w-6xl`, detail `max-w-5xl`, forms `max-w-3xl`,
auth form column `max-w-[360px]`.

---

## 5. Components

All primitives live in `src/components/ui/`.

- **`Button`** — `primary` (indigo fill), `secondary` (outlined), `ghost`,
  `danger`. Sizes `sm` / `md` / `lg`. Every button scales to `0.97` on
  `:active`.
- **`Input` / `Label` / `FieldError`** — `raised` fill, `line` border, indigo
  ring on focus, amber border on error. Errors sit under the field at
  `text-[12px]`.
- **`Select` / `Textarea` / `Checkbox`** — same treatment.
- **`Card` / `CardHeader` / `CardBody`** — a header takes an eyebrow, a title
  and an optional action slot on the right.
- **`Badge`** — `neutral` / `teal` / `amber` / `indigo`. Mono, uppercase.
- **`state.tsx`** — `Skeleton`, `TableSkeleton`, `ErrorState`, `EmptyState`,
  `Pager`. Every list renders all four states from here; none of them get
  reinvented per page.
- **`switch-button.tsx`** — the theme toggle. Lives in the sidebar footer.

Two upstream components are vendored, both MIT and both adapted rather than
dropped in — their zinc palettes and Tailwind v4 syntax do not belong here:

- **`queue-filter-cards.tsx`** — kokonutui *Spotlight Cards*, turned from a
  feature grid into the queue's filter control.
- **`ui/switch-button.tsx`** — kokonutui *Switch Button*.

Keep the attribution headers on both.

### The four states, always

Any view backed by the API renders: loading (skeleton, not a spinner on an
empty page), error (message plus a retry that actually refetches), empty (an
icon, a sentence, and the action that would fill it), and content. A refetch
keeps the previous content on screen — see `useAsync` in
`src/hooks/use-api.ts`.

---

## 6. Icons

**Keyline icons**, installed as source via the shadcn registry declared in
`components.json`:

```json
"registries": { "@keyline": "https://keylineicons.com/r/{name}.json" }
```

```bash
npx shadcn add @keyline/bell          # stroke (default)
npx shadcn add @keyline/fill/bell     # any non-stroke style is prefixed
npx shadcn search @keyline            # browse the set
```

Icons land in `src/components/icons/` and are re-exported from
`src/components/icons/index.ts`. Import from the barrel:

```tsx
import { Activity, TrendingDown } from "@/components/icons";
```

> **Check every icon you add.** The shadcn CLI currently corrupts these files
> on write — it collapses repeated coordinate tokens in the `d` attribute and
> rewrites `viewBox="0 0 24 24"` as `"0 24"`. Compare the written file against
> `https://keylineicons.com/r/<name>.json` and fix it before committing.

Sizing: `h-4 w-4` inline with text, `h-3.5 w-3.5` in small controls,
`h-3 w-3` inside badges, `h-5 w-5` for the brand mark.

`lucide-react` remains only in the landing page components. Do not add new
lucide imports to the dashboard or auth surfaces.

---

## 7. Motion

Curves are CSS variables in `globals.css` and Tailwind utilities
(`ease-out`, `ease-in-out`, `ease-drawer`):

```css
--ease-out:     cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out:  cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer:  cubic-bezier(0.32, 0.72, 0, 1);
```

### Rules

- **Entering and exiting uses `ease-out`.** Never `ease-in` on UI — it delays
  the first frame, which is exactly the frame being watched.
- **Under 300ms.** Press feedback 100–160ms, small popovers 125–200ms,
  dropdowns 150–250ms, drawers 200–500ms.
- **Name the properties.** `transition-[transform,background-color]`, never
  `transition-all`.
- **Only `transform` and `opacity` animate.** Width, height and padding
  trigger layout.
- **Nothing scales from zero.** Entrances start at `scale(0.95)` or higher
  with `opacity: 0`.
- **Stagger is 35ms per row, capped at 7 rows.** Past that it reads as lag,
  not cascade.
- **Keyboard-initiated actions do not animate.**

`prefers-reduced-motion` is handled globally in `globals.css`, which collapses
every animation and transition. Do not re-implement it per component — **with
one exception**: Motion springs (`useSpring`) run on their own loop and CSS
cannot reach them, so any spring-driven effect must also check
`useReducedMotion()` in JS. The filter cards' tilt does this.

The shared `fade-up` animation (`animate-fade-up`) uses `both` as its fill
mode so a delayed element starts hidden rather than flashing at full opacity.

---

## 8. Theming

`next-themes` with `attribute="class"`, **dark by default**, system preference
off — the product has a look, and the toggle is there for a bright room rather
than to follow the OS. `disableTransitionOnChange` is on: without it every
colour transition on the page fires at once and the swap smears.

- The toggle (`SwitchButton`) sits in the dashboard sidebar footer.
- `<html>` carries `suppressHydrationWarning`, since the theme class is
  written before paint and the server cannot know it.
- Any component reading `useTheme()` must render an inert placeholder until
  mounted, or it flashes the wrong state.

**Dark-only surfaces.** The auth shell and the landing page hard-code `dark`
on their root element. They are signature surfaces built around glow, depth
and a tilting neural network, none of which survive a white background.

> Changing `tailwind.config.ts` needs a dev-server restart. Next caches the
> resolved config, so edits to the palette appear to do nothing until you
> restart — the stylesheet keeps serving the old literals.

---

## 9. Page patterns

### Auth — premium split (`src/components/auth-shell.tsx`)

A `2fr / 1fr` grid above `lg`, with a `minmax(400px, 1fr)` floor so the form
column never squeezes on a smaller laptop. Below `lg` it is one column and
the signature panel is hidden.

- **Left (two thirds)** — the brand statement, sized to be read from across a
  desk: 42–48px headline, 19px body, 580–660px measure. Ambient depth: two
  drifting glows, a 690px tilting neural network at `perspective: 1350px`, a
  scan line. Content staggers in at 40 / 100 / 150 / 210 / 270ms.
- **Right (one third)** — the form, `max-w-[360px]`, centered. Deliberately
  calmer: one glow, one smaller network, particles. It is atmosphere behind
  the fields, not a second hero.

There is no account-creation link. The backend exposes no public registration
route — accounts are created by an admin through `POST /admin/users`.

### Dashboard

A fixed `w-60` sidebar on `panel`, content on `ink` at `px-8 py-8`. Active
nav is `bg-raised` with a teal icon. No ambient motion.

The dashboard is a **ranked triage queue**, per ADR-006 — not a feed and not
an analytics page. Rank comes from the three booleans `/triage` returns
(`has_worsening_trend`, `awaiting_sign_off`, `has_open_early_watch`); the
backend sends no score, so `triageUrgency()` in `src/lib/utils.ts` is the one
place that ordering is defined.

**The filter cards are the queue's controls, not decoration.** Each card is a
button with `aria-pressed` and a spelled-out `aria-label` — the visible card
is an icon, a title, a number and a hint across several spans, which composes
into nothing useful for a screen reader.

Their counts have to be true of the same set, or putting them side by side
invites a false comparison. `/triage` pages but does not filter, so the queue
is fetched once at the API's maximum page size and filtered on the client;
past that ceiling the UI says what the counts cover rather than under-reporting.

### Voice

The dashboard speaks as an assistant that has already done some of the work,
not as a tool reporting state. The line under the greeting says what is in the
queue today and what was done about it — "1 case waiting, and Okafor's is
trending the wrong way, so I've moved it to the top" — never "Cases are ranked
by urgency", which explains the feature instead of the situation.

Every branch of that sentence is derived from a real count. Warmth is in the
phrasing, never in the facts: `summarise()` in `dashboard/page.tsx` has no
branch that claims anything the data does not support, and it describes the
**queue**, so it does not change when a filter is clicked.

---

## 10. Data layer

```
src/lib/types.ts      Wire types, mirroring backend-routes.json
src/lib/endpoints.ts  Every backend call, grouped by resource
src/lib/api.ts        Axios instance, bearer token, error envelope
src/hooks/use-api.ts  useAsync (stale-while-refetching), useDebounced
src/hooks/use-patients.ts  Domain hooks: triage, directory, patient, visits
```

Components call `endpoints.ts`, never `api.get("/some/path")` directly. When
the backend contract changes, regenerate `backend-routes.json` and update
`types.ts` and `endpoints.ts` together.

The domain is **Patient → Visit → (Scan, Symptoms) → Analysis → Report**.
There is no prediction hanging off a patient: a patient has visits, and a
visit is what gets analysed.

---

## 11. Writing

Sentence case everywhere except eyebrows and badges. No exclamation marks.
Say what happened and what to do:

- "Can't reach the server. Check that the backend is running." — not
  "Error: network request failed."
- "The queue is clear" / "New analyses land here as soon as the pipeline
  finishes." — not "No data."
- "Sign off before generating a report" as a disabled button's title — the
  control explains its own state rather than failing when pressed.

Clinical language stays hedged. "Ranked findings", "likelihood", "decision
support" — never "diagnosis", never "detected".
