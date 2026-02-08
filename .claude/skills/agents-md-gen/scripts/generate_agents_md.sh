#!/bin/bash
# AGENTS.md Generator Script
# Creates an AGENTS.md file to help AI agents understand the repository

echo "Generating AGENTS.md file..."

# Get repository name from current directory
REPO_NAME=$(basename $(pwd))

# Create the AGENTS.md file
cat > AGENTS.md << EOF
# $REPO_NAME - AGENTS.md

## Overview
This repository contains a ${REPO_NAME,,} application built with modern development practices. The system follows a modular architecture with clear separation of concerns.

## Directory Structure
\$(tree -L 3 -I 'node_modules|dist|build|.git|.claude' || echo "Install 'tree' command for detailed structure")

## Technologies Used
- Primary Language: [Language determined from code]
- Frameworks: [Frameworks detected from dependencies]
- Build Tools: [Build tools from package.json/Cargo.toml/etc.]
- Testing: [Testing frameworks detected]

## Entry Points
- Main Application: [Detected from package.json/main, main.py, app.py, etc.]
- Configuration: [Configuration files detected]
- API Endpoints: [API routes detected]

## Conventions
- Code Style: [Style guides detected]
- Branch Naming: [Convention inferred]
- Commit Messages: [Format detected]
- Testing: [Test structure detected]

## Key Dependencies
Dependencies are managed via [package manager detected]. Key dependencies include:
- [Dependencies listed from package manager files]

## Common Tasks
\`\`\`bash
# To run the application
[Command to run application]

# To run tests
[Command to run tests]

# To build the application
[Command to build application]

# To lint the code
[Command to lint code]
\`\`\`

## Development Workflow
1. Clone the repository
2. Install dependencies
3. Configure environment variables
4. Run the application
5. Run tests to verify functionality

## Notes for AI Agents
- When modifying code, follow existing patterns
- When adding features, maintain backward compatibility where possible
- When fixing bugs, ensure tests pass before submitting changes
- When refactoring, preserve functionality while improving structure
EOF

echo "✓ AGENTS.md generated successfully"