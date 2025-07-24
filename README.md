# Agent OS

## Stop prompting AI coding agents like it's 2024

Your coding agents are capable of so much more—they just need an operating system. Introducing, Agent OS.

## A system to make AI coding agents build your way, not their way.

Agent OS transforms AI coding agents from confused interns into productive developers. With structured workflows that capture your standards, your stack, and the unique details of your codebase, Agent OS gives your agents the specs they need to ship quality code on the first try—not the fifth.

#### Use it with:

- Claude Code
- Cursor
- Any AI coding tool

#### Free & Open Source

[View on GitHub](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI)

## Why use Agent OS?

Stop wrestling with AI that writes the wrong code. Agent OS transforms coding agents from confused assistants into trusted developers who truly understand your codebase.

3 reasons why product teams use Agent OS:

### 1 Complete context, not just prompts

Unlike basic AI setups, Agent OS provides three layers of context that work together:
- Standards - Your coding style, tech stack, and best practices
- Product - Your mission, architecture, roadmap, and decisions
- Specs - Detailed plans & tasks for each feature implementation

The result: Agents write code that looks like you wrote it—first time, every time.

### 2 Structured development, not chaos

Agent OS replaces random prompting and circular rewrites with a proven workflow. It automatically:
- Writes comprehensive specs before coding begins
- Breaks features into trackable, TDD-focused tasks
- Documents key decisions as they happen
- Updates your roadmap as features ship

The difference: Ship features faster with clear specs and completed tasks—not endless cycles of (re)explaining requirements and redoing work.

### 3 Your standards, your way

Agent OS is completely yours to shape. Define your own coding standards, write custom instructions, and adapt every workflow to match how your team operates. No rigid interfaces or prescribed processes—just markdown files you control. Works seamlessly with any AI tool or IDE you choose.

The relief: Your coding agent finally feels like a senior developer on your team—thinking your way, following your patterns, and shipping at your standards.

## The Three Layers of Context

Agent OS works by layering context—just like you'd onboard a human developer. Each layer builds on the previous one, creating a complete picture of how you build software.

### Layer 1 Your standards

Your standards define how you build software. Your stack. Your opinions. Your style. Your priorities. The standards you expect everyone on your team to follow when building anything. These should include:
- Tech Stack — Your default frameworks, libraries, and tools
- Code Style — Your formatting rules, naming conventions, and preferences
- Best Practices — Your development philosophy (e.g., TDD, commit patterns, etc.)

Your standards documentation lives on your system in `~/.agent-os/standards/...` and are referenced from every project, every codebase. Set once, use everywhere, override as needed.

```
~/.agent-os/standards/...
```

### Layer 2 Your product

At the product (codebase) layer, we document what it is we're building, why we're building it, who it's for, and the big-picture product roadmap. This includes:
- Mission — What you're building, for whom, and why it matters
- Roadmap — Features shipped, in progress, and planned
- Decisions — Key architectural and technical choices (with rationale)
- Product-specific stack — The exact versions and configurations for this codebase

Product documentation lives in your codebase (`.agent-os/product/`) and give agents the full picture of your product.

```
.agent-os/product/
```

### Layer 3 Your specs

Throughout your product's development, you'll create many specs. Each spec is a single feature or enhancement or fix, which typically represents a few hours or days of work (accellerated with the help of AI). Each spec will have its own requirements, technical specs, and tasks breakdown.

Individual feature specifications include:
- SRD (Spec Requirements Document) — Goals for the feature, user stories, success criteria
- Technical Specs — API design, database changes, UI requirements
- Tasks Breakdown — Trackable step-by-step implementation plan with dependencies

Specs live in dated folders inside your codebase (`.agent-os/projects/2025-12-19-user-auth/`) and guide agents through each spec's implementations.

```
.agent-os/projects/2025-12-19-user-auth/
```

With all three layers in place, your agent has everything it needs: how you build (Standards), what you're building (Product), and what to build next (Specs). No more confusion, no more rewrites—just clean, consistent code that looks like you wrote it.

## Install Agent OS

Getting started with Agent OS is a two-step process:

1. **Base Installation** - Install Agent OS on your system
2. **Tool-Specific Setup** - Set up Claude Code, Cursor, or whichever IDE you're using

Installing Agent OS in an existing codebase that's been around a while? Then see Working with Existing Codebases.

See What Gets Installed Where? to understand where all the Agent OS files will live after installation.

### 1 Base Installation

Everyone starts here. The fastest way to get started is by running the install script with this one-liner in your terminal:

```bash
curl -sSL https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/main/setup.sh | bash
```

This script:
- Creates the `~/.agent-os/` folder in your home directory.
- Downloads and installs instructions files (plan-product, create-spec, execute-task, analyze-product) from the [GitHub repo](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/tree/main/instructions).
- Downloads and installs standards file templates (tech-stack, code-style, best-practices) from the [GitHub repo](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/tree/main/standards).
- Preserves any existing files (won't overwrite your customizations).

**Options:**
- Use `--overwrite-instructions` to update and overwrite instruction files when needed.
- Use `--overwrite-standards` to update and overwrite standards files when needed.

#### Manual Installation

##### 1 Create the Agent OS directories

```bash
mkdir -p ~/.agent-os/standards
mkdir -p ~/.agent-os/instructions
```

Note: The `~/` refers to your home directory:
- Mac/Linux: `/Users/yourusername/`
- Windows: `C:\Users\yourusername\` (or use `%USERPROFILE%` in Command Prompt)

##### 2 Copy the standards files

Copy the [standards files](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/tree/main/standards) to `~/.agent-os/standards/`:

- [tech-stack.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/standards/tech-stack.md)
- [code-style.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/standards/code-style.md)
- [best-practices.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/standards/best-practices.md)

##### 3 Copy the instructions files

Copy the [instruction files](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/tree/main/instructions) to `~/.agent-os/instructions/`:

- [plan-product.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/instructions/plan-product.md)
- [create-spec.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/instructions/create-spec.md)
- [execute-tasks.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/instructions/execute-tasks.md)
- [analyze-product.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/instructions/analyze-product.md)

Note: These instruction files work well as-is, but you're welcome to review and adjust them if needed.

### Important: Customize your standards files

Once you've installed the base files, you'll need to customize the standards files in `~/.agent-os/standards/` to match your preferences. This is where you define your way of building software.

The files that were installed (`tech-stack.md`, `code-style.md`, and `best-practices.md`) are just examples or starting points. You're encouraged to replace or add to them, or delete them and start fresh. Then edit them to match your preferences.

### 2 Tool-Specific Setup

With the base installation complete, now set up Agent OS for your AI tool:
- Claude Code
- Cursor
- Hybrid Setup (Claude Code + Cursor)
- Other AI coding tools...

### Claude Code Setup

Use the the following one-liner to run the Claude Code setup script:

```bash
curl -sSL https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/main/setup-claude-code.sh | bash
```

This script:
- Installs the CLAUDE.md from the [GitHub Repo](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/claude-code/user/CLAUDE.md) into your `~/.claude/` folder. This points Claude Code to the instructions and standards located in your `~/.agent-os/` folder.
- Copies the commands from the [GitHub Repo](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/commands) to use as custom slash commands in your `~/.claude/commands/` folder.

#### Manual Claude Code Setup

##### 1 Copy the command files

Copy the [command files](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/tree/main/commands) to `~/.claude/commands/`:

- [plan-product.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/commands/plan-product.md)
- [create-spec.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/commands/create-spec.md)
- [execute-tasks.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/commands/execute-tasks.md)
- [analyze-product.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/commands/analyze-product.md)

##### 2 Copy the CLAUDE.md file

Copy [claude-code/user/CLAUDE.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/claude-code/user/CLAUDE.md) to your system's `~/.claude/` folder

This points Claude Code to your default preferences and global standards.

That's it! You can now use these commands in Claude Code:
- `/plan-product`
- `/create-spec`
- `/execute-tasks`
- `/analyze-product`

### Cursor Setup

Using Cursor? For each project where you want to use Agent OS, use the following one-liner to run the Cursor setup script:

**Important:** First be sure that you're inside your project's root folder so that Cursor rules are installed inside of it.

```bash
curl -sSL https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/main/setup-cursor.sh | bash
```

This script:
- Creates the `.cursor/rules/` directory in your project.
- Copies the commands from the [GitHub repo](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/tree/main/commands) to your `.cursor/rules/` folder with `.mdc` extensions.

#### Manual Cursor Setup

##### 1 Create the Cursor rules directory

```bash
mkdir -p .cursor/rules
```

##### 2 Copy the command files

Copy the [command files](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/tree/main/commands) to `.cursor/rules/` and rename them with `.mdc` extension:

- [plan-product.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/commands/plan-product.md) → `plan-product.mdc`
- [create-spec.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/commands/create-spec.md) → `create-spec.mdc`
- [execute-tasks.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/commands/execute-tasks.md) → `execute-tasks.mdc`
- [analyze-product.md](https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/blob/main/commands/analyze-product.md) → `analyze-product.mdc`

That's it! You can now use these commands in Cursor:
- `@plan-product`
- `@create-spec`
- `@execute-tasks`
- `@analyze-product`

### Hybrid Setup (Claude Code + Cursor)

Using both Claude Code and Cursor? Follow both setups above to enable Agent OS in both tools.

1. Follow the Claude Code setup to enable global commands
2. For each project, follow the Cursor setup to add project rules

Both tools will now work with the same Agent OS installation.

### Other AI coding tools...

Agent OS is just markdown files. To adapt it for any AI tool, find where your tool looks for commands or context, then copy our command files there.

1. Find where your tool looks for commands or context
2. Copy our command files there, adjusting the format as needed

The command files simply point to the instructions and standards located in your `~/.agent-os/` installation.

### Working with Existing Codebases

Already have a product in development? Agent OS works great with existing code:

1. Complete steps 1 and 2 above for your tool.
2. Run the `@analyze-product` command:

```
@analyze-product I want to install Agent OS in my existing codebase
```

This will analyze your codebase, understand what's already built, and create Agent OS documentation that reflects your actual implementation.

### What Gets Installed Where?

After installation, you'll have:

**Base Installation:**

```
~/.agent-os/
├── standards/
│   ├── tech-stack.md       # Your default tech choices
│   ├── code-style.md       # Your formatting preferences
│   └── best-practices.md   # Your development philosophy
└── instructions/
    ├── plan-product.md     # Agent's instructions to initialize a product
    ├── create-spec.md      # Agent's instructions to plan features
    ├── execute-tasks.md    # Agent's instructions to build and ship
    └── analyze-product.md  # Agent's instructions to add to existing code
```

**Claude Code Addition:**

```
~/.claude/
├── CLAUDE.md               # Points to your default preferences
└── commands/
    ├── plan-product.md     # → points to ~/.agent-os/instructions/
    ├── create-spec.md      # → points to ~/.agent-os/instructions/
    ├── execute-tasks.md    # → points to ~/.agent-os/instructions/
    └── analyze-product.md  # → points to ~/.agent-os/instructions/

your-product/
├── .claude/
│   └── CLAUDE.md           # Points to project details and instructions
└── .agent-os/
    ├── product/            # Created by plan-product
    └── specs/              # Created by create-spec
```

**Cursor Addition (Per Project):**

```
your-product/
├── .cursor/
│   └── rules/
│       ├── plan-product.mdc    # → points to ~/.agent-os/instructions/
│       ├── create-spec.mdc     # → points to ~/.agent-os/instructions/
│       ├── execute-tasks.mdc   # → points to ~/.agent-os/instructions/
│       └── analyze-product.mdc # → points to ~/.agent-os/instructions/
├── .agent-os/
│   ├── product/            # Created by plan-product
│   └── specs/              # Created by create-spec
└── CLAUDE.md               # If also using Claude Code
```

**Uninstall Agent OS:**

```bash
# To remove Agent OS completely
curl -sSL https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/main/setup_clean.sh | bash -s -- --all

# To remove only base installation
curl -sSL https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/main/setup_clean.sh | bash -s -- --base

# To remove only Claude Code integration
curl -sSL https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/main/setup_clean.sh | bash -s -- --claude-code
