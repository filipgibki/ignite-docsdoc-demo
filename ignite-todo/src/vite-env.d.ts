/// <reference types="vite/client" />

declare namespace React {
  interface DOMAttributes<T> {
    'data-testid'?: string;
  }
}
