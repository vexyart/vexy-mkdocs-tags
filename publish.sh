#!/usr/bin/env bash
# this_file: publish.sh
# Publish script for this Python package
# Workflow: clean → gitnextver → build → publish

# Change to script directory
cd "$(dirname "$0")"

set -e

# Color output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Publishing package...${NC}"
echo -e "${YELLOW}Workflow: clean → gitnextver → build → publish${NC}"

# Step 1: Clean build artifacts
echo -e "${YELLOW}→ Cleaning...${NC}"
uvx hatch clean || true

# Step 2: Run gitnextver to create version tag
echo -e "${YELLOW}→ Running gitnextver...${NC}"
if command -v gitnextver &> /dev/null; then
    gitnextver || echo -e "${YELLOW}↔ gitnextver failed or not configured${NC}"
else
    echo -e "${YELLOW}↔ gitnextver not found, skipping version bump${NC}"
fi

# Step 3: Build the package
echo -e "${YELLOW}→ Building package...${NC}"
uvx hatch build

# Step 4: Publish to PyPI using uv (NOT uvx hatch publish)
echo -e "${YELLOW}→ Publishing to PyPI...${NC}"
if [ -d "dist" ] && [ "$(ls -A dist)" ]; then
    uv publish dist/*
else
    echo -e "${RED}❌ No distribution files found in dist/${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Package published successfully${NC}"
