# 🛠️ 2-Hour Quickstart Setup Guide

**Complete Environment Setup in 30 Minutes**

## 📋 Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 16+ installed  
- [ ] AWS account with Bedrock access
- [ ] Git and GitHub account
- [ ] 2GB free disk space

## 🚀 Quick Setup Script

```bash
# 1. Create project directory
mkdir my-ai-agent && cd my-ai-agent

# 2. Setup Python environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install core dependencies
pip install strands-agents strands-agents-tools bedrock-agentcore uv

# 4. Install Kiro IDE (download from kiro.dev)
# Follow platform-specific instructions

# 5. Configure AWS credentials
aws configure  # or use AWS profiles
```

## 🔧 Tool Installation

### 1. Kiro IDE Setup
```bash
# Download from https://kiro.dev
# Install platform-specific version
# Launch and complete initial setup
```

### 2. Strands SDK Installation
```bash
pip install strands-agents[all] strands-agents-tools
```

### 3. AWS MCP Servers Setup
```bash
# Install UV package manager
pip install uv

# Core MCP servers for quickstart
uv tool install awslabs.core-mcp-server@latest
uv tool install awslabs.aws-knowledge-mcp-server@latest
uv tool install awslabs.bedrock-kb-retrieval-mcp-server@latest
```

### 4. Bedrock AgentCore Setup
```bash
pip install bedrock-agentcore-starter-toolkit
```

## ⚙️ Configuration Files

### Kiro MCP Configuration (`kiro_mcp_settings.json`)
```json
{
  "mcpServers": {
    "awslabs.core-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.core-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "awslabs.aws-knowledge-mcp-server": {
      "command": "uvx", 
      "args": ["awslabs.aws-knowledge-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

### AWS Credentials Setup
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-west-2
```

### Strands Configuration (`.env`)
```bash
# AWS Bedrock settings
AWS_REGION=us-west-2
AWS_PROFILE=default

# Model configuration
DEFAULT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
TEMPERATURE=0.3
```

## 🧪 Verification Tests

### Test 1: Strands SDK
```python
from strands import Agent
from strands_tools import calculator

agent = Agent(tools=[calculator])
result = agent("What is 15 * 23?")
print(f"✅ Strands working: {result}")
```

### Test 2: AWS Bedrock Connection
```python
from strands.models import BedrockModel

model = BedrockModel(
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    region="us-west-2"
)
response = model.generate("Hello, test message")
print(f"✅ Bedrock working: {response[:50]}...")
```

### Test 3: MCP Server Connection
```python
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# Test AWS Knowledge MCP
client = MCPClient(
    lambda: stdio_client(StdioServerParameters(
        command="uvx", 
        args=["awslabs.aws-knowledge-mcp-server@latest"]
    ))
)

with client:
    tools = client.list_tools_sync()
    print(f"✅ MCP working: {len(tools)} tools available")
```

### Test 4: Bedrock AgentCore
```python
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def test_agent(request):
    return {"message": "AgentCore working!", "input": request}

print("✅ AgentCore ready for deployment")
```

## 🔍 Troubleshooting

### Common Issues

**Python Version Error**
```bash
# Check version
python --version  # Must be 3.10+

# Install correct version if needed
pyenv install 3.11.0
pyenv local 3.11.0
```

**AWS Credentials Error**
```bash
# Verify credentials
aws sts get-caller-identity

# Check Bedrock access
aws bedrock list-foundation-models --region us-west-2
```

**MCP Server Connection Error**
```bash
# Test MCP server manually
timeout 15s uv tool run awslabs.core-mcp-server@latest 2>&1 || echo "Command completed or timed out"
```

**Kiro IDE Issues**
- Restart IDE after MCP configuration
- Check MCP servers status in settings
- Verify file paths are correct

## 📁 Project Structure

After setup, your project should look like:
```
my-ai-agent/
├── .venv/                 # Python virtual environment
├── .env                   # Environment variables
├── kiro_mcp_settings.json # Kiro MCP configuration
├── main.py               # Your agent code
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## ✅ Setup Verification Checklist

- [ ] Python 3.10+ installed and working
- [ ] Virtual environment created and activated
- [ ] Strands SDK installed and tested
- [ ] AWS credentials configured
- [ ] Bedrock model access verified
- [ ] MCP servers installed and responding
- [ ] Kiro IDE installed and configured
- [ ] AgentCore toolkit ready
- [ ] All test scripts pass

## 🎯 Next Steps

Once setup is complete:
1. Open `quickstart-implementation-guide.md`
2. Start with Module 1: Basic Agent Development
3. Use `quickstart-templates.py` for code examples
4. Follow the 2-hour learning path

## 📞 Setup Support

**Quick Fixes:**
- Restart terminal after environment changes
- Use `pip install --upgrade` for package issues
- Check AWS region consistency across all configs

**Still stuck?** 
- Check GitHub Issues for common problems
- Join Discord #quickstart-help channel
- Review troubleshooting section in main README

---
**Estimated Setup Time:** 30 minutes
**Next:** Begin 2-hour implementation guide