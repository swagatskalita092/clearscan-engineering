# Architecture

This diagram intentionally stays at the verified system-boundary level. It does not represent undocumented private modules or internal service boundaries.

```mermaid
flowchart LR
    User[ClearScan user]

    subgraph Frontend["Frontend on Netlify"]
        Web["React + Vite application<br/>Tailwind CSS · React Router<br/>React Helmet · Lucide React<br/>Supabase JS Client"]
    end

    subgraph Backend["Backend on Railway"]
        API["FastAPI on Python 3.12<br/>38 endpoints<br/>Pydantic · httpx"]
    end

    subgraph Data["Supabase Frankfurt"]
        Auth["Supabase authentication"]
        DB["PostgreSQL<br/>row-level access control"]
    end

    Stripe["Stripe<br/>Payments"]
    Claude["Anthropic Claude API<br/>Paid bullet rewrites<br/>Paid cover letters"]
    Resend["Resend"]

    User --> Web
    Web --> API
    Web --> Auth
    API --> DB
    API <--> Stripe
    API --> Claude
    API --> Resend
```

## Verified deployment boundaries

- The React and Vite frontend is hosted on Netlify.
- The FastAPI backend is hosted on Railway.
- PostgreSQL and authentication use Supabase, with the database in the Frankfurt region.
- Row-level access control is enabled in Supabase/PostgreSQL.
- Payments are handled by Stripe; no card data is stored.
- Anthropic Claude API calls are limited to paid bullet rewrite suggestions and paid cover-letter generation.
- GitHub Actions runs the automated tests. Production deploys automatically from the main branch: the frontend on Netlify and the backend on Railway, built from a Dockerfile.
