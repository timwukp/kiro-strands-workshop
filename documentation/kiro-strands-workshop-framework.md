# Kiro IDE + Strands SDK: Agentic AI Development Workshop Framework

## Course Overview

**Target Audience**: Software developers and agentic AI builders who want to leverage Kiro IDE and Amazon Q Developer extension as primary development tools for building sophisticated AI agent applications.

**Duration**: 5-day intensive workshop (40 hours total)
**Format**: Hands-on coding with practical projects
**Prerequisites**: Basic Python knowledge, familiarity with AI/ML concepts

## Learning Objectives

By the end of this workshop, participants will be able to:
1. Set up and configure Kiro IDE with Amazon Q Developer extension
2. Build agentic AI applications using Strands SDK
3. Implement advanced agent capabilities with Strands Tools
4. Create multi-agent systems and workflows
5. Deploy and manage AI agents in production environments
6. Integrate with AWS services for scalable AI solutions

## Course Structure

### Day 1: Foundation Setup & Introduction
**Duration**: 8 hours
**Focus**: Environment setup, tool familiarization, and basic concepts

#### Module 1.1: Kiro IDE Setup & Configuration (2 hours)
- **Objective**: Get participants up and running with Kiro IDE
- **Activities**:
  - Download and install Kiro IDE from [kiro.dev](https://kiro.dev)
  - Configure Amazon Q Developer extension
  - Set up steering files for project-specific guidance
  - Configure MCP servers for external integrations
  - One-click migration from VS Code (if applicable)

**Hands-on Lab 1.1**: 
```markdown
# Lab: Kiro IDE First Project Setup
1. Create a new project in Kiro IDE
2. Set up steering file with custom rules
3. Configure MCP server connections
4. Test agentic chat functionality
5. Create your first spec using natural language
```

#### Module 1.2: Strands SDK Introduction (2 hours)
- **Objective**: Understand Strands architecture and core concepts
- **Topics**:
  - Model-driven approach to AI agents
  - Agent Builder vs SDK vs Tools ecosystem
  - Understanding the Strands philosophy
  - Environment setup and configuration

**Hands-on Lab 1.2**:
```python
# Lab: First Strands Agent
from strands import Agent, tool
from strands_tools import calculator, current_time, python_repl

@tool
def letter_counter(word: str, letter: str) -> int:
    """Count occurrences of a specific letter in a word."""
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0
    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")
    return word.lower().count(letter.lower())

agent = Agent(tools=[calculator, current_time, python_repl, letter_counter])

# Test the agent with multiple requests
message = """
I have 4 requests:
1. What is the time right now?
2. Calculate 311169 / 74088
3. Tell me how many letter R's are in the word "strawberry" 🍓
4. Output a script that does what we just spoke about!
   Use your python tools to confirm that the script works before outputting it
"""

agent(message)
```

#### Module 1.3: Development Environment Integration (2 hours)
- **Objective**: Integrate Kiro IDE with Strands development workflow
- **Activities**:
  - Configure Kiro IDE for Python development
  - Set up hooks for automated testing
  - Configure specs for agent development
  - Integrate with version control

#### Module 1.4: Basic Agent Architecture (2 hours)
- **Objective**: Understand agent design patterns
- **Topics**:
  - Agent lifecycle and execution flow
  - Tool selection and composition
  - Error handling and resilience
  - Logging and debugging strategies

### Day 2: Core Agent Development
**Duration**: 8 hours
**Focus**: Building functional agents with essential capabilities

#### Module 2.1: File Operations & System Integration (2 hours)
- **Objective**: Master file handling and system interactions
- **Tools Covered**: `file_read`, `file_write`, `editor`, `shell`

**Hands-on Lab 2.1**:
```python
# Lab: Document Processing Agent
from strands import Agent
from strands_tools import file_read, file_write, editor, shell

agent = Agent(tools=[file_read, file_write, editor, shell])

# Create an agent that can:
# 1. Read configuration files
# 2. Process and transform data
# 3. Generate reports
# 4. Execute system commands for deployment
```

#### Module 2.2: HTTP & API Integration (2 hours)
- **Objective**: Build agents that interact with external services
- **Tools Covered**: `http_request`, API authentication patterns

**Hands-on Lab 2.2**:
```python
# Lab: API Integration Agent
from strands import Agent
from strands_tools import http_request, file_write

agent = Agent(tools=[http_request, file_write])

# Build an agent that:
# 1. Fetches data from REST APIs
# 2. Handles authentication (Bearer, API keys)
# 3. Processes JSON responses
# 4. Converts HTML to markdown
# 5. Stores results in structured formats
```

#### Module 2.3: Python Code Execution & Analysis (2 hours)
- **Objective**: Create agents that can write and execute code
- **Tools Covered**: `python_repl`, `code_interpreter`

**Hands-on Lab 2.3**:
```python
# Lab: Data Analysis Agent
from strands import Agent
from strands_tools import python_repl, file_read
from strands_tools.code_interpreter import AgentCoreCodeInterpreter

# Create isolated code execution environment
code_interpreter = AgentCoreCodeInterpreter(region="us-west-2")
agent = Agent(tools=[python_repl, file_read, code_interpreter.code_interpreter])

# Build an agent that:
# 1. Loads datasets from files
# 2. Performs statistical analysis
# 3. Creates visualizations
# 4. Generates insights and reports
```

#### Module 2.4: Mathematical & Calculation Tools (2 hours)
- **Objective**: Implement agents with advanced mathematical capabilities
- **Tools Covered**: `calculator`, symbolic math operations

**Hands-on Lab 2.4**:
```python
# Lab: Mathematical Problem Solver
from strands import Agent
from strands_tools import calculator, python_repl

agent = Agent(tools=[calculator, python_repl])

# Create an agent that can:
# 1. Solve complex mathematical equations
# 2. Perform symbolic mathematics
# 3. Handle calculus operations
# 4. Generate mathematical proofs
```

### Day 3: Advanced Agent Capabilities
**Duration**: 8 hours
**Focus**: Memory, reasoning, and multi-agent systems

#### Module 3.1: Agent Memory Systems (2 hours)
- **Objective**: Implement persistent memory for agents
- **Tools Covered**: `memory`, `agent_core_memory`, `mem0_memory`

**Hands-on Lab 3.1**:
```python
# Lab: Personal Assistant with Memory
from strands import Agent
from strands_tools.agent_core_memory import AgentCoreMemoryToolProvider
from strands_tools import current_time

# Configure memory provider
provider = AgentCoreMemoryToolProvider(
    memory_id="assistant-memory-123",
    actor_id="user-456",
    session_id="session-789",
    namespace="personal_assistant",
    region="us-west-2"
)

agent = Agent(tools=provider.tools + [current_time])

# Build an agent that:
# 1. Remembers user preferences
# 2. Tracks conversation history
# 3. Learns from interactions
# 4. Provides personalized responses
```

#### Module 3.2: Advanced Reasoning & Thinking (2 hours)
- **Objective**: Implement complex reasoning capabilities
- **Tools Covered**: `think`, advanced reasoning patterns

**Hands-on Lab 3.2**:
```python
# Lab: Strategic Planning Agent
from strands import Agent
from strands_tools import think, memory, python_repl

agent = Agent(tools=[think, memory, python_repl])

# Create an agent that:
# 1. Performs multi-step reasoning
# 2. Analyzes complex problems
# 3. Generates strategic plans
# 4. Evaluates different scenarios
```

#### Module 3.3: Swarm Intelligence & Multi-Agent Systems (2 hours)
- **Objective**: Coordinate multiple agents for complex tasks
- **Tools Covered**: `swarm`, `agent_graph`

**Hands-on Lab 3.3**:
```python
# Lab: Multi-Agent Problem Solving
from strands import Agent
from strands_tools import swarm, agent_graph

agent = Agent(tools=[swarm, agent_graph])

# Build a system that:
# 1. Creates collaborative agent swarms
# 2. Implements competitive problem-solving
# 3. Manages agent communication
# 4. Coordinates parallel processing
```

#### Module 3.4: Workflow Automation (2 hours)
- **Objective**: Create automated workflows and processes
- **Tools Covered**: `workflow`, `batch`, `cron`

**Hands-on Lab 3.4**:
```python
# Lab: Automated Business Process
from strands import Agent
from strands_tools import workflow, batch, cron, http_request, file_write

agent = Agent(tools=[workflow, batch, cron, http_request, file_write])

# Create an agent that:
# 1. Defines multi-step workflows
# 2. Executes parallel operations
# 3. Schedules recurring tasks
# 4. Handles error recovery
```

### Day 4: AWS Integration & Production Deployment
**Duration**: 8 hours
**Focus**: Cloud integration, scalability, and production readiness

#### Module 4.1: AWS Services Integration (2 hours)
- **Objective**: Leverage AWS services in agent applications
- **Tools Covered**: `use_aws`, AWS service patterns

**Hands-on Lab 4.1**:
```python
# Lab: Cloud-Native Agent
from strands import Agent
from strands_tools import use_aws, memory, http_request

agent = Agent(tools=[use_aws, memory, http_request])

# Build an agent that:
# 1. Manages S3 buckets and objects
# 2. Interacts with DynamoDB
# 3. Processes SQS messages
# 4. Triggers Lambda functions
```

#### Module 4.2: Knowledge Base Integration (2 hours)
- **Objective**: Implement RAG patterns with Amazon Bedrock
- **Tools Covered**: `retrieve`, `store_in_kb`, knowledge base management

**Hands-on Lab 4.2**:
```python
# Lab: Knowledge-Powered Agent
from strands import Agent
from strands_tools import retrieve, store_in_kb, memory

agent = Agent(tools=[retrieve, store_in_kb, memory])

# Create an agent that:
# 1. Stores documents in knowledge bases
# 2. Performs semantic search
# 3. Implements RAG patterns
# 4. Manages knowledge lifecycle
```

#### Module 4.3: Media Generation & Processing (2 hours)
- **Objective**: Create agents that work with multimedia content
- **Tools Covered**: `generate_image`, `nova_reels`, `image_reader`, `speak`

**Hands-on Lab 4.3**:
```python
# Lab: Creative Content Agent
from strands import Agent
from strands_tools import generate_image, nova_reels, image_reader, speak

agent = Agent(tools=[generate_image, nova_reels, image_reader, speak])

# Build an agent that:
# 1. Generates images from text
# 2. Creates video content
# 3. Analyzes visual content
# 4. Produces audio output
```

#### Module 4.4: Browser Automation & Web Interaction (2 hours)
- **Objective**: Automate web-based tasks
- **Tools Covered**: `browser`, web automation patterns

**Hands-on Lab 4.4**:
```python
# Lab: Web Automation Agent
from strands import Agent
from strands_tools.browser import LocalChromiumBrowser

browser = LocalChromiumBrowser()
agent = Agent(tools=[browser.browser])

# Create an agent that:
# 1. Navigates web pages
# 2. Fills forms automatically
# 3. Extracts data from websites
# 4. Performs automated testing
```

### Day 5: Real-World Projects & Best Practices
**Duration**: 8 hours
**Focus**: Capstone projects and production considerations

#### Module 5.1: Capstone Project Planning (1 hour)
- **Objective**: Design a comprehensive agent application
- **Activities**:
  - Project requirements gathering
  - Architecture design
  - Tool selection and integration planning
  - Timeline and milestone definition

#### Module 5.2: Capstone Project Implementation (4 hours)
- **Objective**: Build a complete agent application
- **Project Options**:

**Option A: Business Process Automation Agent**
```python
# Automated Customer Support System
# Features:
# - Email processing and categorization
# - Knowledge base integration
# - Automated response generation
# - Escalation handling
# - Performance analytics
```

**Option B: Content Creation & Management Agent**
```python
# Multi-Media Content Pipeline
# Features:
# - Content planning and research
# - Text, image, and video generation
# - Social media scheduling
# - Performance tracking
# - Content optimization
```

**Option C: Data Analysis & Reporting Agent**
```python
# Intelligent Analytics Platform
# Features:
# - Data ingestion from multiple sources
# - Automated analysis and insights
# - Interactive report generation
# - Anomaly detection
# - Predictive modeling
```

#### Module 5.3: Testing & Quality Assurance (1 hour)
- **Objective**: Implement testing strategies for agents
- **Topics**:
  - Unit testing for agent tools
  - Integration testing patterns
  - Performance testing
  - Error handling validation
  - Security considerations

#### Module 5.4: Deployment & Monitoring (1 hour)
- **Objective**: Deploy agents to production
- **Topics**:
  - Containerization strategies
  - AWS deployment patterns
  - Monitoring and logging
  - Performance optimization
  - Scaling considerations

#### Module 5.5: Project Presentations & Review (1 hour)
- **Objective**: Share learnings and get feedback
- **Activities**:
  - Project demonstrations
  - Code review sessions
  - Best practices discussion
  - Future development planning

## Best Practices & Guidelines

### Kiro IDE Best Practices
1. **Steering Files**: Create comprehensive steering files that guide AI behavior
2. **Specs Management**: Use structured specs for feature development
3. **Hook Automation**: Implement hooks for repetitive tasks
4. **MCP Integration**: Leverage MCP servers for external tool access
5. **Natural Language Coding**: Use conversational programming effectively

### Strands SDK Best Practices
1. **Tool Composition**: Select minimal, focused tool sets
2. **Error Handling**: Implement robust error recovery
3. **Memory Management**: Use appropriate memory backends
4. **Performance Optimization**: Monitor and optimize agent performance
5. **Security**: Follow security best practices for production deployment

### Development Workflow
1. **Iterative Development**: Start simple, add complexity gradually
2. **Testing Strategy**: Test individual tools before integration
3. **Documentation**: Maintain clear documentation for agent behavior
4. **Version Control**: Use proper versioning for agent configurations
5. **Monitoring**: Implement comprehensive logging and monitoring

## Prerequisites & Setup

### Required Software
- Kiro IDE (latest version from kiro.dev)
- Python 3.8+ with pip
- Git for version control
- AWS CLI (configured with appropriate permissions)
- Docker (for containerization exercises)

### Python Dependencies
```bash
# Core Strands packages
pip install strands-agents
pip install strands-agents-tools
pip install strands-agents-builder

# Optional dependencies for specific tools
pip install strands-agents-tools[mem0_memory, use_browser]
```

### AWS Setup
- AWS account with appropriate permissions
- Bedrock access enabled
- S3 buckets for storage exercises
- Knowledge Base setup for RAG exercises

### Environment Variables
```bash
# AWS Configuration
export AWS_REGION=us-west-2
export AWS_PROFILE=default

# Strands Configuration
export STRANDS_MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0
export STRANDS_MAX_TOKENS=32768
export STRANDS_KNOWLEDGE_BASE_ID=your-kb-id

# Tool-specific configurations
export BYPASS_TOOL_CONSENT=false
export STRANDS_TOOL_CONSOLE_MODE=enabled
```

## Assessment & Certification

### Daily Assessments
- **Day 1**: Environment setup and basic agent creation
- **Day 2**: Tool integration and functionality implementation
- **Day 3**: Advanced capabilities and multi-agent coordination
- **Day 4**: AWS integration and production deployment
- **Day 5**: Capstone project completion and presentation

### Final Certification Requirements
1. Complete all hands-on labs
2. Successfully implement capstone project
3. Demonstrate understanding of best practices
4. Pass written assessment on concepts and implementation
5. Present working agent application

### Certification Levels
- **Foundation**: Basic agent development with Kiro IDE and Strands SDK
- **Advanced**: Multi-agent systems and AWS integration
- **Expert**: Production deployment and optimization

## Resources & References

### Documentation
- [Kiro IDE Documentation](https://docs.kiro.dev)
- [Strands Agents Documentation](https://strandsagents.com)
- [Amazon Q Developer Guide](https://docs.aws.amazon.com/amazonq/)

### Sample Code Repositories
- [Strands Samples](https://github.com/strands-agents/samples)
- [Strands Tools](https://github.com/strands-agents/tools)
- [Strands Python SDK](https://github.com/strands-agents/sdk-python)

### Community Resources
- [Kiro Discord Server](https://discord.gg/kirodotdev)
- [Strands GitHub Discussions](https://github.com/strands-agents/agent-builder/discussions)
- [AWS Developer Forums](https://forums.aws.amazon.com/)

## Instructor Notes

### Preparation Checklist
- [ ] Verify all software installations work correctly
- [ ] Test AWS permissions and service access
- [ ] Prepare sample datasets and APIs for exercises
- [ ] Set up shared development environment
- [ ] Create backup plans for common setup issues

### Common Troubleshooting
1. **Kiro IDE Installation Issues**: Provide alternative download links
2. **AWS Permission Errors**: Have pre-configured IAM roles ready
3. **Python Environment Conflicts**: Use virtual environments
4. **Network Connectivity**: Prepare offline alternatives for key resources
5. **Tool Integration Failures**: Have debugging guides ready

### Extension Activities
For advanced participants who complete exercises early:
- Implement custom tools for Strands
- Create advanced MCP servers for Kiro IDE
- Explore experimental features and beta capabilities
- Contribute to open-source projects
- Mentor other participants

This comprehensive framework provides a structured approach to learning Kiro IDE and Strands SDK for agentic AI development, with hands-on exercises that build practical skills and real-world applications.