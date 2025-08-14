# Repository Guidelines

## Project Structure & Module Organization
- `src/`: React + TypeScript source. Place UI in `components/` (PascalCase, e.g., `Header.tsx`), hooks in `hooks/` (camelCase, e.g., `useGameState.ts`), and assets in `assets/`.
- `public/`: Static files served as‑is.
- `index.html`: App entry for Vite.
- `docs/`: Design and process docs (e.g., `architecture.md`, `contributing.md`).
- Config: `vite.config.ts`, `eslint.config.js`, `tsconfig*.json`.

## Build, Test, and Development Commands
- `npm run dev`: Start Vite dev server with HMR.
- `npm run build`: Type‑check (`tsc -b`) and create production build via Vite.
- `npm run preview`: Preview the production build locally.
- `npm run lint`: Run ESLint over the project.

Example: `npm run dev` then open the printed local URL.

## Coding Style & Naming Conventions
- Python 3.11+ and TypeScript; React 19, Vite 7. Prefer functional components and hooks.
- Manage tasks as you develop them so that they are checked off in `. /TODO.md` to manage tasks so that they are checked off.
- Indentation: 2 spaces; max 120 cols suggested.
- Filenames: components `PascalCase.tsx`, hooks `useX.ts`, utilities `camelCase.ts`.
- Imports: use absolute or relative consistently; group React, third‑party, local.
- Linting: ESLint with `@eslint/js`, `typescript-eslint`, React Hooks, and React Refresh configs. Fix issues before commit (`npm run lint`).

## Testing Guidelines
- No test runner is configured yet. If adding tests, prefer Vitest + React Testing Library.
- Place tests next to sources as `*.test.ts`/`*.test.tsx` (e.g., `Button.test.tsx`).
- Aim to cover core UI logic and reducers; keep tests deterministic.

## Commit & Pull Request Guidelines
- Commits: use Conventional Commits (e.g., `feat: add round timer`, `fix: prevent negative score`).
- Scope changes narrowly; meaningful messages over "update"/"wip".
- PRs: include a concise summary, screenshots/GIFs for UI, steps to verify, and links to related issues/docs.
- Keep PRs small and focused; ensure `build` and `lint` pass.

## Security & Configuration Tips
- Do not commit secrets. Vite env vars should use `VITE_` prefix and live in local `.env` files ignored by Git.
- Review `docs/architecture.md` for high‑level design before larger changes.
