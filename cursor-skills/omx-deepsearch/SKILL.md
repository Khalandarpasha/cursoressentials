---
name: omx-deepsearch
description: >-
  Perform thorough codebase search for a specified query, pattern, or concept.
  Returns structured findings with file paths, line numbers, and usage patterns.
---
# Deep Search (ported from OmX $deepsearch)

## Purpose

Perform thorough search of the codebase for the specified query, pattern, or concept.

## When to Use

- User needs a comprehensive search across the entire codebase
- Looking for all usages of a concept, pattern, or symbol
- Need to map out where a feature is implemented and consumed
- Need to understand how a concept flows through the codebase

## When Not to Use

- A simple single-file lookup suffices
- The user already knows the file and just needs to read it
- The query is a trivial one-symbol grep

## Workflow

1. **Broad Search**
   - Search for exact matches using `Grep tool`
   - Search for related terms and variations
   - Check common locations (components, utils, services, hooks)
   - Use `Task tool with explore subagent` for structural discovery

2. **Deep Dive**
   - Read files with matches
   - Check imports/exports to find connections
   - Follow the trail (what imports this? what does this import?)

3. **Synthesize**
   - Map out where the concept is used
   - Identify the main implementation
   - Note related functionality

## Tools

- **Grep tool** — search for exact patterns, symbols, and related terms
- **Task tool with explore subagent** — structural codebase exploration and file discovery
- **Read tool** — read matched files for deeper understanding
- **SemanticSearch tool** — find code by meaning when exact text matching is insufficient

## Output Format

- **Primary Locations** (main implementations)
- **Related Files** (dependencies, consumers)
- **Usage Patterns** (how it's used across the codebase)
- **Key Insights** (patterns, conventions, gotchas)

Focus on being comprehensive but concise. Cite file paths and line numbers.
