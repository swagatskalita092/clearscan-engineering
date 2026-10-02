# Technology Choices

ClearScan's verified stack is listed below. The rationale describes generally applicable properties of each technology, not undocumented claims about the original private implementation decision.

## Frontend

### React

React supports component-based user interfaces and a mature frontend ecosystem.

### Vite

Vite provides a focused development and build toolchain for modern frontend applications.

### Tailwind CSS

Tailwind CSS provides utility-based styling that can keep UI implementation close to component markup.

### React Router

React Router provides client-side routing for React applications.

### React Helmet

React Helmet manages document-head metadata from React components.

### Lucide React

Lucide React provides a consistent set of SVG icons as React components.

### Supabase JS Client

The Supabase JavaScript client connects browser applications to supported Supabase capabilities.

## Backend

### FastAPI and Python 3.12

FastAPI provides typed API development, async request support, and integration with Python's data-processing ecosystem. ClearScan currently exposes 38 FastAPI endpoints.

### Pydantic

Pydantic supports typed data validation and serialization in Python and integrates directly with FastAPI.

### httpx

httpx provides synchronous and asynchronous HTTP client APIs for Python.

### Stripe

Stripe provides payment and subscription APIs. ClearScan uses live Stripe payments. Payments are handled by Stripe; no card data is stored.

### Resend

Resend provides an API for application email.

## Data and authentication

### Supabase and PostgreSQL

Supabase combines managed PostgreSQL, authentication, and row-level access control. ClearScan uses Supabase/PostgreSQL, with its database in the Frankfurt region.

## Hosting and delivery

### Netlify

Netlify hosts the ClearScan frontend and supports deployment of web frontend assets.

### Railway

Railway hosts the ClearScan backend and supports deployment of application services.

### GitHub Actions and Docker

GitHub Actions runs the automated tests. Docker packages the backend for Railway. ClearScan has made 220+ commits to production since July 2026.

## AI boundary

The Anthropic API is not part of core scoring. It is used only for two paid features:

- AI-assisted bullet rewrite suggestions
- AI-generated cover letters

These features are gated behind the paid subscription.
