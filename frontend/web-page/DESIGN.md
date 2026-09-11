# NeuroOne — Design System

Personal/academic project (final-year B.Tech), clinician-assist neurodegenerative
diagnosis tool. This doc captures the visual direction decided so far: brand
identity, color, typography, and the login screen spec. Treat it as a living
document — extend it as new screens (dashboard, case review, diagnosis output)
get designed.

---

## 1. Brand identity

**Wordmark:** the full text "NeuroOne", set in **Seira** (Ermedia Studio) —
a modern, elegant serif with fluid ligatures. Used for the logotype only,
never for body copy or UI labels (it's a display face, not built for small
sizes or long text).

- License: free for personal/academic use. Confirmed appropriate for this
  project's current scope (coursework + portfolio/resume use, not a
  commercial product). If this project ever becomes a commercial product
  or a registered business, the commercial license from Ermedia Studio
  would need to be purchased at that point.
- Get the font file from the foundry/listing (Ermedia Studio, via 1001 Fonts
  or similar) and self-host it — don't hotlink a third-party site. Drop the
  OTF/WOFF into your frontend's font assets folder and reference it:

  ```css
  @font-face {
    font-family: 'Seira';
    src: url('/fonts/Seira.woff2') format('woff2'),
         url('/fonts/Seira.otf') format('opentype');
    font-weight: 400;
    font-display: swap;
  }

  .logo-wordmark {
    font-family: 'Seira', 'Cormorant Garamond', serif; /* licensed fallback */
    font-size: 28px;
    letter-spacing: 0.01em;
  }
  ```

- Fallback: **Cormorant Garamond** (open-licensed, no restrictions) if the
  Seira file isn't loaded yet or fails — keeps the same "elegant serif"
  character without a broken-font moment.
- Lockup: wordmark only, no icon mark for now. Sits top-left of the login
  form panel (where the placeholder bat/icon mark currently is), and
  top-left of the main app nav once the dashboard is built.

## 2. Color system

Two tiers: a calm, light **Product** palette for anything a clinician
actually works in, and a richer **Brand** palette reserved for auth/marketing
moments. Both are drawn from the same blue-violet-teal family so they read
as one identity, not two.

### Product (dashboard, forms, tables, reports)

| Token | Hex | Use |
|---|---|---|
| `bg` | `#EAF3FB` | App background |
| `surface` | `#FFFFFF` | Cards, panels, modals |
| `ink` | `#0F2A43` | Primary text |
| `ink-soft` | `#4B6076` | Secondary text, captions |
| `border` | `rgba(15,42,67,0.12)` | Dividers, input borders |
| `primary` | `#2F6FA6` | Buttons, links, active states |
| `primary-hover` | `#255A87` | Hover/pressed state |

### Brand (login screen, decorative panel, marketing surfaces)

| Token | Hex | Use |
|---|---|---|
| `brand-navy` | `#151B4D` | Decorative panel background base |
| `brand-indigo` | `#3D3AA8` | Panel gradient / secondary shapes |
| `brand-violet` | `#6C4FE0` | Panel accent shapes |
| `brand-teal` | `#2FB6A3` | Panel accent shapes |
| `brand-amber` | `#F4C338` | Single warm accent — use sparingly (one shape/highlight, not a field) |

### Status colors (diagnosis output, case flags)

Worth defining now since AI-01's contract already has confidence tiers and
an `early_watch` category:

| Token | Hex | Use |
|---|---|---|
| `status-watch` | `#D98E04` | `early_watch` flag — reuses the brand-amber family, so a flag visually ties back to the brand rather than looking like a generic warning color |
| `status-critical` | `#D94F4F` | High-severity / at-risk findings |
| `status-stable` | `#2E9E6B` | Active/stable/confirmed states |

## 3. Typography

- **Logotype:** Seira — wordmark only (see §1).
- **UI/product font:** **IBM Plex Sans** — chosen deliberately over a generic
  geometric sans because its "engineered/data-sheet" character reinforces
  that this is a technical diagnostic tool, and it holds up well at small
  sizes in dense tables (patient lists, case history, evidence citations).
- Pairing logic: an elegant serif wordmark against a precise, technical
  interface font is intentional — classy brand mark, clinical product.

| Role | Font | Size / Weight |
|---|---|---|
| Wordmark | Seira | 28–32px, regular |
| Page heading (H1) | IBM Plex Sans | 24px, 600 |
| Section heading (H2) | IBM Plex Sans | 18px, 600 |
| Body | IBM Plex Sans | 15px, 400 |
| Label / caption | IBM Plex Sans | 13px, 500 |

Line length target: keep body text under ~80 characters per line.

## 4. Login screen

**Structure carried over from the reference design (unchanged):**
left panel = form, right panel = decorative art. Order of elements in the
form: wordmark → heading ("Welcome back!") → subtext → email field →
password field → remember-me / forgot-password row → primary CTA →
divider ("Or, Login with") → Google sign-in → register link.

**What changes — the skin:**
- Form panel background: `surface` (`#FFFFFF`) on `bg` (`#EAF3FB`) page
  background, replacing the plain white-on-white of the reference.
- Primary CTA button: `primary` (`#2F6FA6`), not the reference's purple.
- Decorative right panel: keeps the reference's color *family*
  (`brand-navy` / `brand-indigo` / `brand-violet` / `brand-teal`, with
  `brand-amber` as a single sparing highlight) — but the actual artwork
  changes.

**Art direction for the decorative panel (open — needs an artist/asset pass):**
Replace the generic stock shapes (stars, diamonds, triangles) with motifs
that actually reference "neuro" — branching synapse/dendrite lines, a
subtle signal-waveform, node-and-connection patterns — rendered in the same
brand palette above. The goal is the panel should look like it belongs to
*this* product, not a generic UI-kit background.

## 5. Open items

- [ ] Source the real Seira font file (personal-use download) and self-host it
- [ ] Commission or generate the neuro-motif artwork for the decorative panel
- [ ] Extend this doc once the dashboard / case-review / diagnosis-output
      screens are designed — status colors above are ready for that work
- [ ] Favicon / small mark — Seira's ligature-heavy letterforms won't survive
      shrinking to favicon size, so this needs a separate simplified mark,
      not just a cropped wordmark
