# Cursor IDE Quickstart Guide
## December 2025 Edition

*Last Verified: 2025-12-08 via web_search MCP tool*

---

## What is Cursor?

Cursor is an AI-native code editor built on VS Code that integrates advanced AI capabilities directly into your development workflow. Used by millions of developers and over half of the Fortune 500 companies, Cursor offers intelligent code generation, full codebase understanding, and an AI agent that can write entire features autonomously.

**Key Differentiators:**
- **Agent Mode**: A human-AI programmer that works on complex, multi-file tasks autonomously
- **Tab Autocomplete**: Custom model with 28% higher acceptance rate than competitors
- **Full Codebase Context**: Understands your entire project regardless of size
- **Multi-Model Support**: Access OpenAI, Anthropic Claude, Google Gemini, and xAI models

---

## Installation

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 4 GB | 8 GB+ |
| Disk Space | 2 GB | 5 GB+ |
| OS | Windows 10+, macOS 10.15+, Ubuntu 20.04+ | Latest versions |
| Network | Stable internet connection | Fast broadband |

### Installation Steps

1. **Download**: Visit [cursor.com](https://cursor.com) and download for your OS
2. **Install**: Run the installer (works like VS Code installation)
3. **Import Settings**: Cursor can automatically import your VS Code extensions, themes, and keybindings
4. **Sign In**: Create an account or sign in to activate your plan

### Configuration Wizard

During first launch, you'll be prompted to configure:
- **Keyboard shortcuts**: VS Code (recommended), Vim, Emacs, or other presets
- **Language for AI**: Set your preferred language for AI interactions
- **Codebase-wide context**: Enable for AI to understand your entire project
- **Terminal commands**: Add `cursor` command to terminal (optional)

---

## Core Features & Shortcuts

### Essential Keyboard Shortcuts

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| **Tab Autocomplete** | | |
| Accept suggestion | `Tab` | `Tab` |
| Reject suggestion | `Esc` | `Esc` |
| Partial accept | `⌘ + →` | `Ctrl + →` |
| **Inline Edit (Cmd K)** | | |
| Open inline edit | `⌘ + K` | `Ctrl + K` |
| Apply changes | `⌘ + Enter` | `Ctrl + Enter` |
| Cancel changes | `⌘ + Backspace` | `Ctrl + Backspace` |
| **Chat/Ask Mode** | | |
| Open chat | `⌘ + L` | `Ctrl + L` |
| Add selection to chat | `⌘ + Shift + L` | `Ctrl + Shift + L` |
| **Agent/Composer** | | |
| Open Agent | `⌘ + I` | `Ctrl + I` |
| Open full-screen Agent | `⌘ + Shift + I` | `Ctrl + Shift + I` |
| **General** | | |
| Command palette | `⌘ + Shift + P` | `Ctrl + Shift + P` |
| Quick file open | `⌘ + P` | `Ctrl + P` |
| Toggle sidebar | `⌘ + B` | `Ctrl + B` |
| Toggle terminal | `` ⌘ + ` `` | `` Ctrl + ` `` |
| View all shortcuts | `⌘ + R` then `⌘ + S` | `Ctrl + R` then `Ctrl + S` |

### @ Symbol Context References

Use these in Chat or Agent mode to provide context:

| Symbol | Purpose |
|--------|---------|
| `@filename` | Reference a specific file |
| `@functionName` | Reference a specific function |
| `@codebase` | Search across your entire codebase |
| `@web` | Search the web for information |
| `@Docs` | Pull in library documentation |

---

## The Three Modes of Cursor AI

### 1. Tab Autocomplete
The fastest way to get AI assistance. As you type, Cursor predicts your next edit with multi-line suggestions.

**Best for:**
- Repetitive code patterns
- Boilerplate completion
- Quick fixes
- Natural language to code (type a comment, get the code)

**Tips:**
- Cursor predicts based on recent changes
- Works with natural language comments
- Hit `Tab` repeatedly for sequential completions

### 2. Ask Mode (Chat)
Open with `⌘/Ctrl + L` for a conversational interface.

**Best for:**
- Questions about your codebase
- Understanding existing code
- Getting explanations
- Quick research without leaving the IDE

**Tips:**
- Use `@filename` to reference specific files
- Ask "please provide sources" if uncertain about AI responses
- Select code before opening chat to include it as context

### 3. Agent Mode
Open with `⌘/Ctrl + I` for autonomous multi-file editing.

**Best for:**
- Implementing new features
- Multi-file refactoring
- Complex architectural changes
- Running terminal commands

**Key Features (as of Cursor 2.0+):**
- **Composer Model**: Purpose-built coding model, 4x faster than similar intelligence models
- **Background Agents**: Work on tasks while you focus elsewhere
- **Browser Integration**: Agent can interact with web pages
- **Sandboxed Terminals**: Secure command execution on macOS

---

## Project Rules Configuration

Rules provide persistent, scoped instructions for how Cursor AI should behave in your project.

### Setting Up Project Rules

1. **Create rules directory**: `.cursor/rules/` in your project root
2. **Create rule files**: Use `.mdc` (Markdown Components) format
3. **Define rule metadata**: Control when rules apply

### Rule File Format (.mdc)

```markdown
---
description: React Component Standards
globs: "**/*.tsx"
alwaysApply: false
---

# Guidelines
- Use functional components with hooks
- Follow naming convention: PascalCase for components
- Keep components under 200 lines
- @component-template.tsx
```

### Rule Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Always** | Applied to every request | Core coding standards |
| **Auto Attached** | Applied when matching files are referenced | Language-specific rules |
| **Agent Requested** | AI chooses when relevant | Contextual guidelines |
| **Manual** | Invoked explicitly | Special workflows |

### User Rules (Global)

For rules that apply across all projects:
1. Go to `Cursor Settings → Rules → User Rules`
2. Enter plain text instructions
3. These apply to all workspaces

**Example User Rules:**
```
Respond concisely. Avoid filler language.
Prefer TypeScript over JavaScript.
Always use async/await over .then() chains.
```

### Legacy Support

The `.cursorrules` file in project root still works but is deprecated. Migrate to `.cursor/rules/` for better control and version management.

---

## MCP (Model Context Protocol) Integration

MCP allows you to connect Cursor to external tools and data sources.

### What is MCP?

MCP is an open protocol that standardizes how AI applications connect with tools and data. Think of it as a plugin system for extending Cursor's capabilities.

### Configuration Locations

| Location | Scope |
|----------|-------|
| `.cursor/mcp.json` | Project-specific servers |
| `~/.cursor/mcp.json` | Global (all workspaces) |

### Basic MCP Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "mcp-server-package"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### Transport Types

| Type | Use Case |
|------|----------|
| **stdio** | Local development, simple setup |
| **SSE** | Remote servers, distributed teams |
| **Streamable HTTP** | Flexible remote connections |

### Popular MCP Servers

- **Filesystem**: Access local files and directories
- **PostgreSQL**: Query databases directly
- **GitHub**: Interact with repositories
- **Slack**: Team communication integration
- **Sequential Thinking**: Structured problem-solving

### Verifying MCP Connection

1. Open `Cursor Settings → MCP`
2. Check for green indicator next to server name
3. Available tools appear under "Available Tools"

**Limitation**: Cursor supports up to 40 tools from MCP servers.

---

## Pricing Plans (December 2025)

*Note: Pricing changed to usage-based credits in June 2025*

### Plan Comparison

| Plan | Price | Key Features |
|------|-------|--------------|
| **Hobby (Free)** | $0/month | 2,000 completions, 50 slow requests, 2-week Pro trial |
| **Pro** | $20/month | $20 usage credit pool, unlimited Tab, Background Agents |
| **Pro Plus** | $60/month | $70 usage credit pool, more premium model access |
| **Ultra** | $200/month | $400 usage credit pool, priority feature access |
| **Business** | $40/user/month | SSO, admin controls, centralized billing |

### Understanding Usage Credits

- **Tab completions**: Unlimited on Pro and above
- **Agent requests**: Consume credits based on model and context size
- **Auto mode**: Uses lighter models, unlimited on paid plans

**Approximate requests per $20 credit pool:**
- ~225 Claude Sonnet 4 requests
- ~550 Gemini requests
- ~500 GPT-5 requests

### Choosing a Plan

| If you... | Choose... |
|-----------|-----------|
| Are learning or experimenting | Hobby (Free) |
| Code daily, moderate AI use | Pro |
| Heavy Agent usage | Pro Plus |
| Run multiple agents, power user | Ultra |
| Need team governance | Business |

---

## Quick Workflow Examples

### Example 1: Generate a New Component

1. Press `⌘/Ctrl + I` to open Agent
2. Type: "Create a React component for a user profile card with avatar, name, and bio"
3. Review the generated code
4. Press `Accept` to apply changes

### Example 2: Refactor Existing Code

1. Select the code you want to refactor
2. Press `⌘/Ctrl + K` for inline edit
3. Type: "Refactor this to use async/await instead of promises"
4. Review and accept changes

### Example 3: Understand Unfamiliar Code

1. Select complex code
2. Press `⌘/Ctrl + Shift + L` to add to chat
3. Ask: "Explain what this code does step by step"

### Example 4: Multi-File Feature Implementation

1. Press `⌘/Ctrl + I` to open Agent
2. Describe: "Add user authentication with JWT tokens. Create login/logout endpoints, middleware, and update the user model"
3. Agent will create/modify multiple files
4. Review diff for each file before accepting

---

## Best Practices

### For Better AI Responses

1. **Be specific**: Instead of "make this better", say "optimize this query for performance by adding an index hint"
2. **Provide context**: Use `@filename` to reference relevant files
3. **Iterate**: If the first response isn't right, refine your prompt
4. **Use examples**: Show the AI what you want with before/after examples

### For Project Rules

1. Keep rules concise (under 500 lines)
2. Use glob patterns to scope rules to relevant files
3. Include code examples in rules via `@filename` references
4. Version control your `.cursor/rules/` directory

### For Team Collaboration

1. Store project rules in `.cursor/rules/` for team sharing
2. Use Business plan for centralized governance
3. Define Team Rules in Cursor dashboard for org-wide standards
4. Document custom MCP server configurations

---

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| AI suggestions not appearing | Check internet connection, verify plan limits |
| MCP server not connecting | Verify config JSON syntax, check server logs |
| High memory usage | Reduce concurrent agents, close unused tabs |
| Shortcuts not working | Check for conflicts in keyboard settings |

### Getting Help

- **Documentation**: [cursor.com/docs](https://cursor.com/docs)
- **Community Forum**: [forum.cursor.com](https://forum.cursor.com)
- **Changelog**: [cursor.com/changelog](https://cursor.com/changelog)

---

## Version History

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| 2.1 | Late 2025 | Instant grep, multi-agent interface improvements |
| 2.0 | Oct 29, 2025 | Composer model, new agent UI, parallel agents |
| 1.7 | Sept 29, 2025 | Agent Autocomplete, Hooks, Team Rules |
| 1.6 | Oct 2025 | Updated Agent workflows |

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    CURSOR QUICK REFERENCE                    │
├─────────────────────────────────────────────────────────────┤
│ Tab         → Accept AI suggestion                          │
│ Esc         → Reject suggestion                             │
│ ⌘/Ctrl + K → Inline edit (Cmd K)                            │
│ ⌘/Ctrl + L → Open Chat (Ask mode)                           │
│ ⌘/Ctrl + I → Open Agent mode                                │
│ ⌘/Ctrl + P → Quick file open                                │
├─────────────────────────────────────────────────────────────┤
│ @filename   → Reference file    │ @codebase → Search code   │
│ @web        → Web search        │ @Docs     → Library docs  │
├─────────────────────────────────────────────────────────────┤
│ Rules: .cursor/rules/*.mdc      │ MCP: .cursor/mcp.json     │
└─────────────────────────────────────────────────────────────┘
```

---

*Guide compiled from official Cursor documentation and community resources. For the latest updates, visit [cursor.com/changelog](https://cursor.com/changelog).*

**Verification Sources:**
- Cursor Official Docs (docs.cursor.com)
- Cursor Changelog (cursor.com/changelog)
- Cursor Features Page (cursor.com/features)
- Community tutorials and guides
- web_search MCP tool queries on December 8, 2025
