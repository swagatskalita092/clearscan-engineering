# Request and Payment Flows

The flows below contain only confirmed product behavior and intentionally remain at a high-level system boundary.

## Résumé upload and scoring

```mermaid
sequenceDiagram
    actor User
    participant Frontend as React frontend
    participant API as FastAPI backend
    participant Scoring as Deterministic scoring engine

    User->>Frontend: Submit résumé for scoring
    Frontend->>API: Send scoring request
    API->>Scoring: Parse and evaluate résumé
    Scoring->>Scoring: TF-IDF extraction
    Scoring->>Scoring: Skills taxonomy and O*NET benchmarking
    API-->>Frontend: Return scoring result
    Frontend-->>User: Present result
```

The measured end-to-end parse time is under 6 seconds. The core scoring path is deterministic and does not call an LLM.

## Premium Claude features

Claude API calls occur only when a paid user invokes one of these gated features:

1. AI-assisted bullet rewrite suggestions
2. AI-generated cover letters

```mermaid
sequenceDiagram
    actor User
    participant Frontend as React frontend
    participant API as FastAPI backend
    participant Claude as Anthropic Claude API

    User->>Frontend: Request paid AI feature
    Frontend->>API: Send feature request
    API->>Claude: Make gated API call
    Claude-->>API: Return generated result
    API-->>Frontend: Return result
    Frontend-->>User: Present result
```

## Checkout and subscription lifecycle

Stripe payments are live. Payments are handled by Stripe; no card data is stored. Stripe handles upgrades, renewals, and downgrades.

```mermaid
sequenceDiagram
    actor User
    participant Frontend as React frontend
    participant API as FastAPI backend
    participant Stripe as Stripe

    User->>Frontend: Begin paid subscription
    Frontend->>API: Request checkout
    API->>Stripe: Create or initiate checkout flow
    Stripe-->>User: Complete payment flow
    Stripe-->>API: Confirm subscription status
    API->>API: Update account access

    Note over Stripe,API: Stripe also handles renewals,<br/>upgrades, and downgrades
```
