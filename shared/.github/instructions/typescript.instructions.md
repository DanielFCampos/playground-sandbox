---
applyTo: "**/*.{ts,tsx,js,jsx,mjs,cjs}"
description: "Use when writing, reviewing, or modifying TypeScript or JavaScript code. Covers style, typing, modules, and common patterns."
---
# TypeScript / JavaScript Coding Standards

## Style
- Use `camelCase` for variables and functions; `PascalCase` for classes, interfaces, types, and React components
- Prefer `const` over `let`; never use `var`
- Use template literals over string concatenation
- Use trailing commas in multi-line arrays, objects, and parameter lists

## Types (TypeScript)
- Prefer `interface` for object shapes; use `type` for unions, intersections, and mapped types
- Avoid `any` — use `unknown` when the type is truly unknown, then narrow
- Use discriminated unions over optional fields for mutually exclusive states
- Let TypeScript infer return types for simple functions; annotate explicitly when the return type is complex or non-obvious

## Modules
- Use ES module syntax (`import`/`export`); avoid CommonJS (`require`) in new code
- Prefer named exports over default exports for discoverability
- Keep import order: external packages → internal modules → relative imports, separated by blank lines
- Avoid barrel files (`index.ts` re-exports) in large projects — they hurt tree-shaking and slow builds

## Functions & Classes
- Prefer small pure functions over stateful classes
- Use arrow functions for callbacks and inline lambdas; use `function` declarations for top-level named functions
- Destructure parameters when accessing multiple properties
- Prefer `async`/`await` over raw `.then()` chains

## Error Handling
- Catch specific error types; avoid empty `catch` blocks
- Use `Error` subclasses for domain errors; include descriptive messages
- In async code, always handle rejected promises — never leave them unhandled

## React (when applicable)
- Prefer function components with hooks over class components
- Keep components small; extract logic into custom hooks
- Co-locate component, styles, and tests in the same directory
- Use `key` props correctly — never use array index as key for dynamic lists

## Testing
- Write tests using the project's existing test framework (Jest, Vitest, etc.)
- Name test files `*.test.ts` or `*.spec.ts` next to the source file
- Test behavior, not implementation details
- Prefer `describe`/`it` blocks with clear descriptions
