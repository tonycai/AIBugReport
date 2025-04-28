graph LR
    subgraph User Interface
        B[CLI]
    end

    subgraph API Layer
        D(REST API Endpoints)
    end

    subgraph Core Logic Layer
        E(Bug Management)
        F(User Management)
        G(Project Management)
        H(LLM Orchestration)
    end

    subgraph Data Storage
        I[MySQL Database]
    end

    subgraph Pinata Integration
        J(Pinata SDK Interaction)
    end

    subgraph MCP Integration
        K(MCP Client)
    end

    subgraph LLM Interaction
        L(Prompt Engineering)
        M(Response Parsing)
    end

    subgraph "LLM (via MCP)"
        N[External LLM Service]
    end

    subgraph "Error Handling"
        O(Exception Catching)
        P(Error Logging)
        Q(Standardized Responses)
    end

    B --> D

    D --> E
    D --> F
    D --> G
    D --> H

    E --> I
    F --> I
    G --> I
    H --> K

    J --> I

    K --> N
    K --> L

    L --> N
    L --> M

    M --> H

    E --> O
    F --> O
    G --> O
    H --> O
    I --> O
    J --> O
    K --> O
    L --> O
    M --> O

    O --> D

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#ccf,stroke:#333,stroke-width:2px
    style E fill:#9cf,stroke:#333,stroke-width:2px
    style I fill:#fcc,stroke:#333,stroke-width:2px
    style J fill:#cfc,stroke:#333,stroke-width:2px
    style K fill:#ffc,stroke:#333,stroke-width:2px
    style L fill:#cff,stroke:#333,stroke-width:2px
    style N fill:#eee,stroke:#333,stroke-width:2px
    style O fill:#ada,stroke:#333,stroke-width:2px
