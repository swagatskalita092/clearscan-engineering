# Technology Choices

*Why each piece of the verified ClearScan stack is a reasonable choice for this kind of product.*

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

FastAPI provides typed API development, async request support, and integration with Python's data-processing ecosystem. ClearScan uses a FastAPI backend.

### Pydantic

Pydantic supports typed data validation and serialization in Python and integrates directly with FastAPI.

### httpx

httpx provides synchronous and asynchronous HTTP client APIs for Python.

### Stripe

Stripe provides payment and subscription APIs. ClearScan used Stripe for subscription charging until 31 October 2026. Payments are disabled by a feature flag and the code is retained. No card data is stored.

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

GitHub Actions runs the backend tests. Docker packages the backend for Railway. Changing figures such as commit counts live in [STATUS.md](../STATUS.md).

## AI boundary

The Anthropic API is not part of core scoring. It is used only for two text-generation features:

- AI-assisted bullet rewrite suggestions
- AI-generated cover letters

Until 31 October 2026 those features were gated behind the paid tier. ClearScan has been free for every registered user since.
