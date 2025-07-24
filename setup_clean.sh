#!/bin/bash

# Agent OS Cleanup Script
# This script removes all Agent OS files installed by setup.sh and setup-claude-code.sh

set -e  # Exit on error

# Initialize flags
CLEAN_BASE=false
CLAUDE_CODE=false
FORCE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --base)
            CLEAN_BASE=true
            shift
            ;;
        --claude-code)
            CLAUDE_CODE=true
            shift
            ;;
        --all)
            CLEAN_BASE=true
            CLAUDE_CODE=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --base              Remove base Agent OS installation (~/.agent-os/)"
            echo "  --claude-code       Remove Claude Code specific files (~/.claude/)"
            echo "  --all               Remove both base and Claude Code files"
            echo "  --force             Skip confirmation prompts"
            echo "  -h, --help          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --all           # Remove all Agent OS files"
            echo "  $0 --base          # Remove only base installation"
            echo "  $0 --claude-code   # Remove only Claude Code files"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# If no options specified, show help
if [ "$CLEAN_BASE" = false ] && [ "$CLAUDE_CODE" = false ]; then
    echo "🧹 Agent OS Cleanup Script"
    echo "=========================="
    echo ""
    echo "No cleanup options specified. Use --help for usage information."
    echo ""
    echo "Quick options:"
    echo "  $0 --all           # Remove all Agent OS files"
    echo "  $0 --base          # Remove only base installation"
    echo "  $0 --claude-code   # Remove only Claude Code files"
    echo ""
    exit 1
fi

echo "🧹 Agent OS Cleanup Script"
echo "=========================="
echo ""

# Confirmation prompt (unless --force is used)
if [ "$FORCE" = false ]; then
    echo "⚠️  This will permanently delete Agent OS files:"
    echo ""
    if [ "$CLEAN_BASE" = true ]; then
        echo "  📁 ~/.agent-os/ (entire directory)"
        echo "     - All standards files (tech-stack.md, code-style.md, best-practices.md)"
        echo "     - All instruction files (plan-product.md, create-spec.md, execute-tasks.md, analyze-product.md)"
    fi
    if [ "$CLAUDE_CODE" = true ]; then
        echo "  📁 ~/.claude/commands/ (entire directory)"
        echo "  📁 ~/.claude/hooks/ (entire directory)"
        echo "  📄 ~/.claude/CLAUDE.md"
    fi
    echo ""
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cleanup cancelled."
        exit 0
    fi
    echo ""
fi

# Clean base Agent OS installation
if [ "$CLEAN_BASE" = true ]; then
    echo "🗑️  Removing base Agent OS installation..."
    
    if [ -d "$HOME/.agent-os" ]; then
        rm -rf "$HOME/.agent-os"
        echo "  ✓ Removed ~/.agent-os/ directory"
    else
        echo "  ℹ️  ~/.agent-os/ directory not found (already clean)"
    fi
    echo ""
fi

# Clean Claude Code specific files
if [ "$CLAUDE_CODE" = true ]; then
    echo "🗑️  Removing Claude Code specific files..."
    
    # Remove commands directory
    if [ -d "$HOME/.claude/commands" ]; then
        rm -rf "$HOME/.claude/commands"
        echo "  ✓ Removed ~/.claude/commands/ directory"
    else
        echo "  ℹ️  ~/.claude/commands/ directory not found"
    fi
    
    # Remove hooks directory
    if [ -d "$HOME/.claude/hooks" ]; then
        rm -rf "$HOME/.claude/hooks"
        echo "  ✓ Removed ~/.claude/hooks/ directory"
    else
        echo "  ℹ️  ~/.claude/hooks/ directory not found"
    fi
    
    # Remove CLAUDE.md file
    if [ -f "$HOME/.claude/CLAUDE.md" ]; then
        rm "$HOME/.claude/CLAUDE.md"
        echo "  ✓ Removed ~/.claude/CLAUDE.md"
    else
        echo "  ℹ️  ~/.claude/CLAUDE.md not found"
    fi
    
    # Check if ~/.claude directory is empty and remove it
    if [ -d "$HOME/.claude" ] && [ -z "$(ls -A $HOME/.claude)" ]; then
        rmdir "$HOME/.claude"
        echo "  ✓ Removed empty ~/.claude/ directory"
    elif [ -d "$HOME/.claude" ]; then
        echo "  ℹ️  ~/.claude/ directory contains other files, keeping it"
    fi
    echo ""
fi

echo "✅ Cleanup complete!"
echo ""

# Show what was cleaned
if [ "$CLEAN_BASE" = true ] && [ "$CLAUDE_CODE" = true ]; then
    echo "📋 Removed all Agent OS files (base installation + Claude Code integration)"
elif [ "$CLEAN_BASE" = true ]; then
    echo "📋 Removed base Agent OS installation"
elif [ "$CLAUDE_CODE" = true ]; then
    echo "📋 Removed Claude Code integration files"
fi

echo ""
echo "💡 To reinstall Agent OS:"
if [ "$CLEAN_BASE" = true ]; then
    echo "   Base installation: curl -sSL https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/main/setup.sh | bash"
fi
if [ "$CLAUDE_CODE" = true ]; then
    echo "   Claude Code setup: curl -sSL https://raw.githubusercontent.com/bipa/pytagoras-programming_with_AI/main/setup-claude-code.sh | bash"
fi
echo ""