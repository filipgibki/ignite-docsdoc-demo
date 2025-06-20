## **React Project Technical Specifications**

This document outlines the technical conventions and architecture for building our React web application.

## **Technology Stack**

This project is built using a modern, efficient technology stack:

* **Vite:** A next-generation frontend tooling system that provides an extremely fast development server and optimized build process.
* **React:** The core JavaScript library for building user interfaces with a component-based architecture.
* **TypeScript:** A superset of JavaScript that adds static typing, improving code quality and maintainability.
* **Material-UI (MUI):** A comprehensive library of pre-built, accessible, and production-ready React components that serves as the foundation for our UI.
* **Emotion:** A high-performance CSS-in-JS library that is the default styling engine for MUI. It is installed as a dependency of Material-UI.

## **Project Structure**

All application files are organized inside the `src/` directory. This structure promotes separation of concerns and scalability:

```
ignite-todo/
├── public/              # Static assets (images, fonts) accessible from root URL
├── src/
│   ├── assets/          # Static assets compiled by Vite (SVGs, etc.)
│   ├── components/      # Reusable UI components (e.g., Button.tsx, Card.tsx)
│   ├── hooks/           # Custom React hooks (e.g., useFetch.ts)
│   ├── pages/           # Components representing entire pages/routes
│   ├── services/        # Logic for external APIs (e.g., api.ts)
│   ├── types/           # Shared TypeScript type and interface definitions
│   │   └── index.ts
│   ├── utils/           # Helper functions
│   ├── App.tsx          # Main application component and layout root
│   └── main.tsx         # Application entry point
├── index.html
├── package.json
└── tsconfig.json
```

## **Development Conventions**

### **Type Safety**
* **Typing is Mandatory**: Define all shared data structures as types or interfaces in the `src/types/` directory. Use TypeScript for all props, state, and function signatures to ensure type safety. Avoid using the `any` type.

### **State Management**
* Primarily use React's built-in hooks (`useState`, `useEffect`, `useContext`, `useReducer`). Do not introduce a global state management library (like Redux) unless the application's complexity explicitly requires it.
* **State must be immutable.** When updating state (especially objects and arrays), always create a new instance instead of modifying the existing one.
* *Correct Example*: `setData(prevData => [...prevData, newItem]);`
* *Incorrect Example*: `data.push(newItem); setData(data);`

### **Component Architecture**
* Build the UI from small, reusable, single-responsibility components.
* Maintain a **unidirectional data flow**: Pass data and state down from parent to child components via props.
* Use callback functions passed as props for children to communicate events or data changes back up to their parents.

### **Styling**
* Use **Material-UI (MUI)** as the primary component library.
* For component-specific styling, use the `sx` prop provided by MUI for concise, inline styles. This keeps styling concerns co-located with the component logic. Avoid creating separate `.css` or `.module.css` files unless necessary for complex, reusable styles.

### **Code Quality & Naming**
* Component files and their corresponding functions must be named using **PascalCase** (e.g., `DataGrid.tsx`, `function DataGrid()`).
* All other files (hooks, utils, services) and variables/functions within them must be named using **camelCase** (e.g., `useAuth.ts`, `const apiService = ...`).
* Write clean, readable code with meaningful names. Keep functions short and focused on a single responsibility.

## **Testing & Selectors**

To ensure our application is robust and maintainable, it is crucial to write tests that are resilient to changes in the UI, such as text labels or DOM structure.

### **Best Practices for Selectors**

*   **Prioritize `data-testid`**: For end-to-end (E2E) and integration tests, always use `data-testid` attributes to select elements. This decouples tests from implementation details.
*   **Avoid brittle selectors**: Do not rely on CSS class names, tag names, or text content for selectors in tests, as these are prone to frequent changes.
*   **Applying to MUI Components**: For simple Material-UI components like `Button` or `ListItem`, apply the `data-testid` prop directly. For components that wrap an input element, such as `TextField` or `Checkbox`, you should also apply the `data-testid` prop directly to the component. In more complex components with multiple distinct parts, use the `slotProps` prop to target specific internal elements (slots) when necessary.

### **`data-testid` Naming Convention**

Use a consistent and descriptive naming convention for `data-testid` attributes to make them easy to identify and understand.

*   **Format**: `[component-name]-[element-description]` or `[page-name]-[component-name]-[element-description]`
*   **Examples**:
    *   `add-task-form-input`: The input field for adding a new task.
    *   `task-list`: The list containing all task items.
    *   `task-item-label-1`: The label for the task item with id 1.
    *   `task-item-checkbox-1`: The checkbox for the task item with id 1.
    *   `task-item-delete-button-1`: The delete button for the task item with id 1.