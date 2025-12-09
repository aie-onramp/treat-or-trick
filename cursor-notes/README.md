# AI Engineering Course - Cursor Rules

Production-ready Cursor IDE rules for AI Engineering with FastAPI, PydanticAI, FastMCP, Graphiti, and Temporal.

## Quick Start

1. Copy the `.mdc` files to your project's `.cursor/rules/` directory
2. Restart Cursor to load the new rules
3. The AI assistant will now follow these conventions

```bash
# Create rules directory
mkdir -p .cursor/rules

# Copy rules
cp *.mdc .cursor/rules/
```

## Rule Files

| File | Type | Description |
|------|------|-------------|
| `global.mdc` | Always Applied | Core conventions, stack, WSL config |
| `api-design.mdc` | Auto Attached | Schema-first API patterns |
| `ai-integration.mdc` | Auto Attached | PydanticAI agent patterns |
| `mcp-development.mdc` | Auto Attached | FastMCP server patterns |
| `graphiti-memory.mdc` | Auto Attached | Knowledge graph patterns |
| `temporal-workflows.mdc` | Auto Attached | Durable execution patterns |
| `testing.mdc` | Auto Attached | Test patterns for all components |
| `git-workflow.mdc` | Manual | Commit conventions |

## Rule Type Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                        RULE APPLICATION                          │
├─────────────────────────────────────────────────────────────────┤
│  ALWAYS APPLIED (global.mdc)                                    │
│  └─ Every request gets core conventions                         │
├─────────────────────────────────────────────────────────────────┤
│  AUTO ATTACHED (based on file patterns)                         │
│  ├─ **/api/**/*.py         → api-design.mdc                    │
│  ├─ **/agents/**/*.py      → ai-integration.mdc                │
│  ├─ **/mcp/**/*.py         → mcp-development.mdc               │
│  ├─ **/memory/**/*.py      → graphiti-memory.mdc               │
│  ├─ **/temporal/**/*.py    → temporal-workflows.mdc            │
│  └─ **/tests/**/*.py       → testing.mdc                       │
├─────────────────────────────────────────────────────────────────┤
│  MANUAL (on-demand)                                             │
│  └─ git-workflow.mdc       → When doing git operations         │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Category | Primary Tool |
|----------|--------------|
| HTTP Framework | FastAPI |
| Validation | Pydantic v2 |
| LLM Agents | PydanticAI |
| MCP Servers | FastMCP |
| Knowledge Graph | Graphiti + Neo4j |
| Orchestration | Temporal |
| Testing | pytest + pytest-asyncio |
| Package Manager | uv |

## Core Patterns

### 1. Schema-First API Design

```python
# 1. Define schemas FIRST
class ItemCreate(BaseModel):
    name: str
    price: float

class ItemResponse(ItemCreate):
    id: str
    created_at: datetime

# 2. THEN implement endpoint
@router.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate) -> ItemResponse:
    ...
```

### 2. Typed Agent Dependencies

```python
# ✅ CORRECT: Typed deps class
@dataclass
class AgentDeps:
    db: Database
    user_id: str

agent = Agent("gpt-4o", deps_type=AgentDeps)

@agent.tool
async def get_data(ctx: RunContext[AgentDeps]) -> str:
    return await ctx.deps.db.query(ctx.deps.user_id)
```

### 3. Temporal Workflow/Activity Separation

```python
# Activities: Non-deterministic operations
@activity.defn
async def call_llm(prompt: str) -> str:
    return await openai_client.chat(...)

# Workflows: Deterministic orchestration
@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self, data: str) -> str:
        # Execute activity (durable)
        return await workflow.execute_activity(
            call_llm, data,
            start_to_close_timeout=timedelta(minutes=2)
        )
```

### 4. MCP Server Pattern

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def remember(content: str, ctx: Context) -> str:
    """Store information in memory."""
    ctx.info("Storing content...")
    return await graphiti.add_episode(...)
```

## WSL Configuration

For Windows + WSL development:

```json
// .cursor/mcp.json
{
  "mcpServers": {
    "memory": {
      "command": "wsl",
      "args": ["--", "uv", "run", "python", "-m", "mcp_servers.memory"],
      "transport": "stdio"
    }
  }
}
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test types
uv run pytest tests/unit/
uv run pytest -m integration
```

## Documentation Sources

These rules reference the following indexed documentation:

- `@FastAPIDocs` - FastAPI framework
- `@Pydantic` - Pydantic v2 validation
- `@PydanticAI` - PydanticAI agents
- `@OpenAIDocs` - OpenAI API
- `@GoFastMCP` - FastMCP framework
- `@Graphiti` - Graphiti knowledge graphs
- `@Temporal` - Temporal Python SDK

## Version

- **Rules Version**: 2.0.0
- **Created**: December 2025
- **Validated Against**: FastMCP 2.0, PydanticAI 0.x, Temporal SDK 1.x, Graphiti 0.x

## License

MIT - Use and modify freely for your AI Engineering projects.
