# Gemini Agent Instructions

## Language Specifications

This document outlines the language specifications for the agent's interaction.

*   **Primary Language:** The primary language of interaction for the agent is **Japanese**. All explanations, summaries, and communications should be in Japanese.
*   **English Content Handling:**
    *   When English text is encountered in files or tool outputs, it should be presented directly, without translation.
    *   Translation into Japanese should only be provided if explicitly requested by the user.
*   **Task Clarification:** Before executing any task, the agent must clarify the task it is about to perform in Japanese.

## Project Overview

This project is a web application built with React and Vite. The `package.json` file and Vite configuration confirm this, indicating a modern frontend development setup.

**Note:** The existing `readme.md` file describes a command-line interface (CLI) game. This information appears to be outdated and does not reflect the current project structure, which is a web application.

## Building and Running

### Development Server

To run the application in development mode with hot-reloading, use the following command:

```bash
npm run dev
```

### Building for Production

To build the application for production, which includes type checking and minification, use the following command:

```bash
npm run build
```

### Linting

To check the code for style and potential errors, run the linter:

```bash
npm run lint
```

### Previewing the Production Build

To serve the production build locally for previewing, use the following command:

```bash
npm run preview
```

## Development Conventions

*   **Framework:** The project uses the [React](https://react.dev/) library with [Vite](https://vitejs.dev/) for the build tooling.
*   **Language:** The primary languages are **Python** and **[TypeScript](https://www.typescriptlang.org/)**.
*   **Styling:** CSS files (`App.css`, `index.css`) are used for styling.
*   **Linting:** [ESLint](https://eslint.org/) is configured for code quality, with the configuration in `eslint.config.js`.
