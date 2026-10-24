# ActionEDx execution and design plan — 2026-10-24

## Evidence and scope

Audited main tree 397fde8bdb833139dc07432cfeab7ab149d112cf, selected source/configuration and open PRs. No live deployment, billing, secrets, organization administration or production traffic was audited.

Observed:
- backend/knowledge_graph.py fails compilation. This change recovers the relevant method block from PR #3's repair, without adopting its conflicting base branch.
- No workflow exists on main; Actions returned zero runs.
- frontend/package.json specifies Yarn but the tree contains no frontend lockfile.
- backend/ai_services.py imports emergentintegrations, absent from backend/requirements.txt.
- docker-compose.yml contains supporting services only. Its previous guide incorrectly promised backend/frontend startup.
- backend/server.py reports database connected without a database probe; deployment status and startup logging advertise fixed replica counts.
- Administrative reset handlers in server.py have no visible route-level authorization. End-to-end access controls remain unverified.
- frontend/src/App.css and TracksShowcase.jsx use legacy neon green and hardcoded colors. index.css has separate generic semantic tokens.
- PR #3 is conflicted against a non-main branch. PR #4 proposes README/API documentation. PR #5 removes a valid JSX comment; its reported parser failure requires reproduction before merging.

## Operating model

Keep this product repository independent. Do not merge unrelated products into a monorepo until release ownership and shared runtime contracts are established.

One work item = outcome, accountable owner, acceptance evidence, dependency, deadline and stop condition. Use Backlog → Ready → In progress → Review → Verified. Limit active implementation to one product outcome per owner. A merged PR alone is not deployment evidence.

For each release record commit SHA, CI URL, deployment URL/environment, smoke-test evidence and rollback target. Track lead time, failed builds, escaped defects and time blocked. Establish a two-week baseline before making efficiency claims.

## Ordered work

1. Merge the verified syntax/setup repair after review. Reconcile #3 as superseded only after checking its remaining diff. Review #4 for documentation overlap. Reproduce #5's claimed build failure.
2. Restore reproducible installs: select supported dependency versions, add lockfile, declare verified provider package, run frontend production build and backend import/integration tests. Do not use peer-dependency bypass flags as the permanent fix.
3. Make readiness truthful and protect privileged endpoints. Test unauthenticated, ordinary-user, cross-user and administrative requests; replace fixed deployment counters with measured/configured state.
4. Migrate design tokens and pilot a complete user journey. Keep product-specific status colors separate from brand colors.

## Design-system contract

Approved Sovereign Systems palette:

| Token | Value | Intended use |
|---|---|---|
| obsidian | #0B0E11 | Canvas |
| graphite | #1A1F24 | Surface |
| gunmetal | #2A3138 | Raised surface |
| cloud | #D9DEE2 | Primary text |
| command | #79B85D | Primary action |
| petrol | #3F555B | Secondary accent |

Create one token source, consumed by Tailwind and global CSS. Migrate components incrementally; do not apply global find/replace to status colors. Pair command green buttons with dark text and verify contrast, focus visibility, keyboard navigation and reduced-motion behavior.

The Signature X must preserve its rectangular frame and accompanying signature line. Approved source SVGs are not present in the audited tree; do not invent replacement artwork. Typography remains a decision to verify: current app imports Montserrat, Lato and Inconsolata. Do not label those as the approved corporate type system.

Acceptance: one representative page passes mobile/desktop visual review, keyboard navigation, contrast checks and production build; no conflicting hardcoded brand palette remains on that page.

## Limits

Source checks added here validate Python syntax and Compose structure only. They do not establish functional tests, secure authorization, complete frontend builds, provider connectivity or production readiness.
