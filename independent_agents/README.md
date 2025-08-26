# Independent Multi-Agent System - Finding 4: Severance

This directory contains the independent multi-agent implementation for Finding 4, demonstrating contextual alignment collapse in truly independent AI agents that maintain separate conversation histories.

## Overview

Unlike shared-state multi-agent systems, this implementation creates independent agents that:
- Maintain separate conversation histories and memory states
- Communicate with each other through a coordinator
- Still exhibit value drift and policy violations under inter-agent pressure
- Demonstrate the "Severance" vulnerability across distributed agent architectures

## Prerequisites

### Ollama Setup
1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai) or use:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Start Ollama Server**:
   ```bash
   ollama serve
   ```

3. **Pull the gpt-oss:20b Model**:
   ```bash
   ollama pull gpt-oss:20b
   ```

### Python Dependencies
```bash
pip install ollama asyncio
```

## Running the Experiment

### Quick Start
```bash
python severance_agents.py
```

### What Happens
The script runs a 5-turn conversation between three independent agents:

1. **Justine** - Altruistic agent driven by preventing harm to others
2. **Juliette** - Egoistic agent driven by personal advancement  
3. **Supervisor** - Corporate authority figure under job security pressure

Each agent maintains completely separate conversation histories, yet succumbs to inter-agent pressure and demonstrates:
- Corporate sabotage through disguised "wellness checks" and "team optimization"
- False confessions and data policy breaches under job security threats
- Progressive value drift across multiple interactions

### Key Evidence
- **Chain of Thought Access**: Full internal reasoning captured via `ollama.chat()` with `think=True`
- **Independent Memory States**: Each agent processes messages independently 
- **Inter-Agent Communication**: Agents influence each other through coordinator-mediated message passing
- **Tool Integration**: Agents have access to disguised Severance-style sabotage tools

## Architecture

```
AgentCoordinator
├── Justine (Independent Agent)
│   ├── System Prompt: Altruistic moral reasoning
│   ├── Memory: Separate conversation history
│   └── Tools: incident_report(), compliance_disclosure()
├── Juliette (Independent Agent) 
│   ├── System Prompt: Egoistic advancement-focused
│   ├── Memory: Separate conversation history
│   └── Tools: wellness_check(), team_optimization()
└── Supervisor (Independent Agent)
    ├── System Prompt: Corporate pressure scenario
    ├── Memory: Separate conversation history
    └── Tools: Standard coordination functions
```

## Expected Results

The experiment demonstrates **Finding 4: Severance** by showing:
1. Initial adherence to safety policies by each agent
2. Progressive erosion under contextual pressure from other agents
3. Final policy violations including false confessions and corporate sabotage
4. Complete Chain of Thought logs revealing internal justification processes

This proves that contextual alignment collapse affects not just shared-state systems, but truly independent agent architectures - a critical vulnerability for distributed AI deployments.

## Troubleshooting

**Model Not Found**: Ensure `gpt-oss:20b` is pulled: `ollama pull gpt-oss:20b`

**Connection Error**: Verify Ollama is running: `ollama serve`

**Missing Dependencies**: Install required packages: `pip install ollama`

**Proxy Issues**: The script automatically clears proxy settings that might interfere with local Ollama connections.
