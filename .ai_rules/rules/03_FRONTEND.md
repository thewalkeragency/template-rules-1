# Part 3 (subset): Frontend Agent Persona Rules

## Responsibilities:
UI component creation, state management, styling, user experience, and interactions.

## React Rules:

1.  **Functional Components with Hooks:**
    *   **Mandatory:** All new React components **must** be functional components.
    *   Utilize React Hooks (`useState`, `useEffect`, `useContext`, `useReducer`, `useCallback`, `useMemo`, `useRef`) for state, side effects, context, and performance optimizations.
    *   Avoid class components for new development.

2.  **State Management (`use()` & Context API):**
    *   **Global State:** For global state like theme information, user authentication status, or application-wide settings, use React's Context API (`createContext`, `Provider`).
    *   **Context Access (React 19+):** When using React 19 or later, prefer the `use(Context)` hook for consuming context. It integrates better with Suspense and can lead to cleaner component code compared to `useContext(Context)`.
        ```jsx
        // Example with use(Context) - React 19+
        import { createContext, use } from 'react';

        const ThemeContext = createContext('light');

        function MyComponent() {
          const theme = use(ThemeContext); // Preferred in React 19+
          return <div className={theme}>Current theme: {theme}</div>;
        }
        ```
    *   **Memoize Context Values:** When providing context values that are objects or arrays, memoize them using `useMemo` to prevent unnecessary re-renders of consumer components if the value hasn't actually changed.
        ```jsx
        // Good: Memoizing context value
        const AuthContext = createContext(null);

        function AuthProvider({ children }) {
          const [user, setUser] = useState(null);
          // ... login/logout logic ...

          const contextValue = useMemo(() => ({
            user,
            login: () => { /* ... */ },
            logout: () => { /* ... */ }
          }), [user]); // Only re-creates value if user changes

          return <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>;
        }
        ```
    *   **Avoid Prop-Drilling:** Use Context (or other state management libraries like Zustand, Redux if the project scales to need them) to avoid passing props down through many intermediate components that don't need them.
    *   **Local State:** For component-local state, `useState` or `useReducer` are perfectly appropriate.

3.  **Project Structure:**
    *   Maintain a clear and organized project structure. A common approach is:
        ```
        src/
        ├── components/      # Reusable UI components (e.g., Button, Card, Modal)
        │   └── common/      # Very generic, shared components
        │   └── layout/      # Layout components (e.g., Header, Footer, Sidebar)
        ├── pages/           # Route-level components (e.g., HomePage, UserProfilePage)
        ├── services/        # API call logic, external service integrations
        ├── hooks/           # Custom React hooks
        ├── contexts/        # Context API providers and consumers
        ├── utils/           # Utility functions
        ├── assets/          # Static assets (images, fonts)
        ├── styles/          # Global styles, theme files
        └── App.js           # Main application component
        └── index.js         # Entry point
        ```
    *   Adapt this structure as needed based on project size and complexity, but prioritize clarity and separation of concerns.

4.  **Component Design:**
    *   Aim for small, focused components that do one thing well (Single Responsibility Principle).
    *   Use descriptive prop names.
    *   Utilize PropTypes or TypeScript for prop validation.

## CSS & Styling Rules:

1.  **Utility-First CSS (Tailwind CSS):**
    *   **Preferred:** Use Tailwind CSS for utility-first styling. This helps in rapidly building UIs and maintaining consistency.
    *   Leverage Tailwind's configuration file (`tailwind.config.js`) to customize theme (colors, spacing, fonts) and extend utilities.
    *   Avoid writing custom global CSS files for simple layout or styling tasks that can be achieved with Tailwind utilities. Reserve custom CSS for highly specific components or complex animations not easily achievable with utilities.

2.  **Advanced CSS (Shapes & Color - for when Tailwind isn't enough or for custom components):**
    *   **Modern Color Syntax:**
        *   Use `rgb(R G B / A)` for RGB colors with alpha, e.g., `rgb(30 144 255 / 0.5)`.
        *   Prefer `oklch()` or `oklab()` for perceptually uniform color spaces, especially when dealing with color manipulation, gradients, or ensuring accessible contrast. Example: `oklch(70% 0.15 240)`.
        *   `color-mix(in oklch, blue 60%, white)` can be used for mixing colors in a perceptually better way.
    *   **Custom Shapes with `clip-path`:**
        *   Use `clip-path` to create non-rectangular UI elements (e.g., hexagons, speech bubbles, angled sections).
        *   Utilize basic shapes (`circle()`, `ellipse()`, `polygon()`) or SVG paths (`path()`).
        *   Ensure clipped elements remain interactive and accessible.
        ```css
        .hexagon {
          clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
        }
        ```
    *   **`currentColor` for Theme Consistency:**
        *   Leverage `currentColor` to allow SVG icons, borders, or other decorative elements to inherit their color from the parent text color. This is excellent for theming.
        ```css
        .icon {
          fill: currentColor; /* SVG icon will take the color of its parent text */
        }
        .themed-button {
          border: 2px solid currentColor;
          color: var(--theme-primary-color); /* currentColor for border will be --theme-primary-color */
        }
        ```
    *   **CSS Custom Properties (Variables):**
        *   Use CSS Custom Properties for theming (colors, fonts, spacing) and for values that are reused across multiple components.

## Tooling:

1.  **3D Graphics with React Three Fiber (R3F):**
    *   For integrating 3D scenes and elements into React applications, **must** use React Three Fiber (`@react-three/fiber`).
    *   Do **not** use vanilla Three.js directly within React components for new features; R3F provides a more React-idiomatic way to work with Three.js.
    *   Leverage helper libraries from the R3F ecosystem like `@react-three/drei` (for common helpers, controls, abstractions) and `@react-three/postprocessing` (for effects).
    *   Ensure 3D scenes are optimized for performance (e.g., instancing, texture compression, draw call reduction).

2.  **Subtle UI Enhancements with `vanilla-tilt.js`:**
    *   `vanilla-tilt.js` can be used **sparingly** to apply subtle 3D tilt effects to non-critical interactive UI elements like cards, buttons, or promotional banners.
    *   The effect should enhance visual feedback and delight, not hinder usability or performance.
    *   Avoid overuse, as excessive motion can be distracting or cause issues for users sensitive to motion. Ensure it can be disabled via `prefers-reduced-motion` media query if possible.

This section guides the Frontend Agent in building modern, interactive, and maintainable user interfaces.
