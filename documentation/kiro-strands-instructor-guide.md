# Kiro IDE + Strands SDK Workshop: Instructor Guide

## Pre-Workshop Preparation (2-3 weeks before)

### Infrastructure Setup

#### 1. Development Environment Preparation

**Kiro IDE Setup**
```bash
# Download and test Kiro IDE on multiple platforms
# Verify compatibility with different operating systems
# Test MCP server integrations
# Prepare backup installation files

# Create shared project templates
mkdir -p workshop-templates/{basic-agent,api-integration,multi-agent,aws-integration}
```

**AWS Account Configuration**
```bash
# Set up workshop AWS account with appropriate permissions
# Create IAM roles for participants
# Set up Bedrock access and knowledge bases
# Configure S3 buckets for exercises
# Prepare Lambda functions for integration exercises

# Example IAM policy for workshop participants
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "dynamodb:*",
        "lambda:InvokeFunction",
        "bedrock:*",
        "sqs:*",
        "sns:*"
      ],
      "Resource": "*"
    }
  ]
}
```

**Python Environment Setup**
```bash
# Create standardized Python environment
python -m venv workshop-env
source workshop-env/bin/activate  # On Windows: workshop-env\Scripts\activate

# Install all required packages
pip install strands-agents
pip install strands-agents-tools
pip install strands-agents-builder
pip install strands-agents-tools[mem0_memory,use_browser]

# Additional development tools
pip install jupyter notebook
pip install pytest
pip install black
pip install flake8

# Create requirements.txt for participants
pip freeze > requirements.txt
```

#### 2. Sample Data and APIs Preparation

**Create Sample Datasets**
```python
# sample_data_generator.py
import json
import csv
from datetime import datetime, timedelta
import random

def create_sample_datasets():
    """Generate sample datasets for workshop exercises."""
    
    # Customer support tickets
    tickets = []
    for i in range(100):
        ticket = {
            "id": f"TICKET-{i:04d}",
            "customer_id": f"CUST-{random.randint(1000, 9999)}",
            "subject": random.choice([
                "Login issues", "Payment problem", "Feature request",
                "Bug report", "Account setup", "Performance issue"
            ]),
            "priority": random.choice(["low", "medium", "high", "urgent"]),
            "status": random.choice(["open", "in_progress", "resolved", "closed"]),
            "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            "description": f"Sample ticket description for ticket {i}"
        }
        tickets.append(ticket)
    
    with open("sample_tickets.json", "w") as f:
        json.dump(tickets, f, indent=2)
    
    # Product catalog
    products = []
    categories = ["Electronics", "Books", "Clothing", "Home", "Sports"]
    for i in range(50):
        product = {
            "id": f"PROD-{i:04d}",
            "name": f"Sample Product {i}",
            "category": random.choice(categories),
            "price": round(random.uniform(10, 500), 2),
            "rating": round(random.uniform(1, 5), 1),
            "in_stock": random.choice([True, False]),
            "description": f"Description for product {i}"
        }
        products.append(product)
    
    with open("sample_products.json", "w") as f:
        json.dump(products, f, indent=2)

if __name__ == "__main__":
    create_sample_datasets()
```

**Mock API Server Setup**
```python
# mock_api_server.py
from flask import Flask, jsonify, request
import json
import random

app = Flask(__name__)

@app.route('/api/weather/<city>')
def get_weather(city):
    """Mock weather API endpoint."""
    return jsonify({
        "city": city,
        "temperature": random.randint(-10, 35),
        "humidity": random.randint(30, 90),
        "description": random.choice(["sunny", "cloudy", "rainy", "snowy"]),
        "timestamp": "2024-01-15T10:00:00Z"
    })

@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    """Mock user management API."""
    if request.method == 'GET':
        return jsonify([
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
        ])
    elif request.method == 'POST':
        user_data = request.json
        return jsonify({"id": 3, "status": "created", **user_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 3. Workshop Materials Preparation

**Create Participant Handbook**
```markdown
# Workshop Participant Handbook

## Quick Reference Guide

### Kiro IDE Shortcuts
- Ctrl+Shift+P: Command palette
- Ctrl+`: Open terminal
- Ctrl+Shift+E: Explorer panel
- F1: Help and documentation

### Strands SDK Quick Commands
```python
# Basic agent creation
from strands import Agent
from strands_tools import file_read, calculator

agent = Agent(tools=[file_read, calculator])
response = agent("Your request here")
```

### Common Troubleshooting
1. **Kiro IDE won't start**: Check system requirements, restart as administrator
2. **MCP server connection failed**: Verify configuration in .kiro/mcp-servers.json
3. **AWS permissions error**: Check IAM roles and policies
4. **Python import errors**: Verify virtual environment activation
```

**Prepare Code Templates**
```python
# agent_template.py
"""
Template for creating Strands agents with best practices.
"""

from strands import Agent, tool
from strands_tools import file_read, file_write, http_request
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for workshop agents with common functionality."""
    
    def __init__(self, name: str, tools: list):
        self.name = name
        self.agent = Agent(tools=tools)
        logger.info(f"Initialized agent: {name}")
    
    def process_request(self, request: str) -> str:
        """Process a request with error handling."""
        try:
            response = self.agent(request)
            logger.info(f"Successfully processed request for {self.name}")
            return response
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return f"Error: {str(e)}"

@tool
def validate_input(data: Any) -> Dict[str, Any]:
    """Template for input validation tool."""
    if not data:
        return {"valid": False, "error": "Empty input"}
    
    return {"valid": True, "data": data}

# Example usage
if __name__ == "__main__":
    agent = BaseAgent("workshop-agent", [file_read, validate_input])
    result = agent.process_request("Test request")
    print(result)
```

## Daily Instruction Plans

### Day 1: Foundation Setup & Introduction

#### Morning Session (4 hours)

**Hour 1: Welcome & Overview (9:00-10:00 AM)**
```
Agenda:
- Welcome and introductions (15 min)
- Workshop overview and objectives (15 min)
- Kiro IDE demonstration (15 min)
- Strands SDK introduction (15 min)

Key Points to Emphasize:
- Agentic AI vs traditional programming
- The power of natural language coding
- Integration between Kiro IDE and development workflow
- Real-world applications and use cases

Interactive Elements:
- Participant introductions with background sharing
- Live polling on experience levels
- Q&A session for initial questions
```

**Hour 2: Kiro IDE Setup (10:15-11:15 AM)**
```
Hands-on Activities:
1. Download and installation (15 min)
2. Initial configuration (15 min)
3. First project creation (15 min)
4. Steering file setup (15 min)

Instructor Notes:
- Have backup installation files ready
- Prepare common troubleshooting solutions
- Use screen sharing for step-by-step guidance
- Assign buddy system for peer support

Common Issues & Solutions:
- Installation permissions: Run as administrator
- Firewall blocking: Add Kiro to exceptions
- Slow download: Provide local installation files
- Configuration errors: Use template configurations
```

**Hour 3: MCP Server Configuration (11:30 AM-12:30 PM)**
```
Learning Objectives:
- Understand MCP protocol and benefits
- Configure GitHub MCP server
- Set up AWS Core MCP server
- Test server connections

Practical Exercise:
1. Create .kiro/mcp-servers.json
2. Configure GitHub integration
3. Test with simple queries
4. Troubleshoot connection issues

Assessment Checkpoint:
- Verify all participants have working MCP connections
- Address individual configuration issues
- Document common problems for future reference
```

**Hour 4: First Strands Agent (1:30-2:30 PM)**
```
Coding Exercise:
- Create basic agent with calculator and time tools
- Test agent functionality
- Add custom tool
- Implement error handling

Code Review Points:
- Tool selection rationale
- Error handling implementation
- Code organization and documentation
- Best practices adherence

Wrap-up:
- Share interesting solutions
- Discuss challenges encountered
- Preview afternoon activities
```

#### Afternoon Session (4 hours)

**Hour 5-6: Advanced Kiro Features (2:45-4:45 PM)**
```
Topics Covered:
- Specs creation and management
- Hook automation setup
- Natural language coding techniques
- Integration with version control

Hands-on Labs:
1. Create comprehensive spec for file processor
2. Set up automated testing hooks
3. Use natural language to generate code
4. Commit and version control integration

Instructor Demonstrations:
- Live coding with natural language
- Spec-driven development workflow
- Hook automation examples
- Git integration best practices
```

**Hour 7-8: Agent Architecture Deep Dive (5:00-7:00 PM)**
```
Theoretical Foundation:
- Agent lifecycle and execution flow
- Tool composition strategies
- Memory and state management
- Performance considerations

Practical Application:
- Design agent architecture for sample problem
- Implement basic agent with multiple tools
- Test and debug agent behavior
- Optimize performance

Group Activity:
- Architecture design challenge
- Peer review of designs
- Discussion of trade-offs and decisions
```

### Day 2: Core Agent Development

#### Detailed Lesson Plans

**Morning Kickoff (9:00-9:15 AM)**
```
Daily Standup Format:
1. Quick review of Day 1 learnings (5 min)
2. Preview of Day 2 objectives (5 min)
3. Address any overnight questions (5 min)

Energy Building Activity:
- Quick coding challenge: "Build an agent that tells jokes"
- Share solutions and laugh together
- Sets positive tone for intensive coding day
```

**File Operations Mastery (9:15-11:15 AM)**
```
Learning Progression:
1. Basic file reading and writing (30 min)
2. Advanced file operations (30 min)
3. Error handling and edge cases (30 min)
4. Performance optimization (30 min)

Instructor Techniques:
- Live coding with commentary
- Deliberate mistake demonstration
- Student-led problem solving
- Pair programming exercises

Assessment Strategy:
- Code review checkpoints every 30 minutes
- Peer evaluation of solutions
- Individual troubleshooting sessions
- Progress tracking on shared board
```

**HTTP & API Integration (11:30 AM-1:30 PM)**
```
Structured Learning Path:
1. HTTP basics and methods (20 min)
2. Authentication patterns (25 min)
3. Response processing (25 min)
4. Error handling and retries (25 min)
5. Real-world API integration (25 min)

Practical Exercises:
- Weather API integration
- Authentication with different methods
- JSON and XML processing
- Rate limiting implementation
- HTML to markdown conversion

Teaching Strategies:
- Use Postman for API exploration
- Show network debugging techniques
- Demonstrate security best practices
- Encourage experimentation with different APIs
```

### Day 3: Advanced Agent Capabilities

#### Memory Systems Workshop (Morning)

**Pre-session Setup (8:45-9:00 AM)**
```bash
# Instructor preparation script
#!/bin/bash

# Set up memory backends for testing
export MEM0_API_KEY="demo-key-for-workshop"
export OPENSEARCH_HOST="localhost:9200"
export AWS_REGION="us-west-2"

# Start local services if needed
docker run -d -p 9200:9200 -e "discovery.type=single-node" opensearchproject/opensearch:latest

# Verify all participants have proper AWS credentials
aws sts get-caller-identity
```

**Memory Implementation Deep Dive (9:00-12:00 PM)**
```
Session Structure:
1. Memory architecture overview (30 min)
2. Hands-on implementation (90 min)
3. Testing and debugging (60 min)

Key Learning Objectives:
- Understand different memory backends
- Implement persistent memory storage
- Create context-aware agents
- Optimize memory performance

Instructor Focus Areas:
- Emphasize data privacy and security
- Show memory lifecycle management
- Demonstrate debugging techniques
- Highlight production considerations

Interactive Elements:
- Memory backend comparison exercise
- Group debugging session
- Performance benchmarking activity
- Security review checklist
```

#### Multi-Agent Systems (Afternoon)

**Swarm Intelligence Workshop (1:00-5:00 PM)**
```
Progressive Complexity:
1. Two-agent communication (60 min)
2. Small swarm coordination (60 min)
3. Complex multi-agent workflows (90 min)
4. Performance optimization (30 min)

Teaching Methodology:
- Start with simple examples
- Build complexity gradually
- Use visual diagrams for architecture
- Encourage creative problem-solving

Assessment Checkpoints:
- Agent communication verification
- Coordination pattern implementation
- Workflow execution testing
- Performance measurement

Troubleshooting Focus:
- Message passing failures
- Coordination deadlocks
- Resource contention issues
- Scaling bottlenecks
```

### Day 4: AWS Integration & Production

#### Cloud-Native Development (Full Day)

**AWS Services Integration (9:00 AM-1:00 PM)**
```
Service Coverage Priority:
1. S3 (Essential) - 60 minutes
2. DynamoDB (Essential) - 60 minutes
3. Lambda (Important) - 60 minutes
4. Additional services (Nice-to-have) - 60 minutes

Hands-on Labs Structure:
- 15 min: Service overview and use cases
- 30 min: Implementation exercise
- 10 min: Testing and validation
- 5 min: Troubleshooting and Q&A

Instructor Preparation:
- Pre-create AWS resources
- Prepare IAM roles and policies
- Set up monitoring dashboards
- Have backup plans for service outages
```

**Production Deployment Workshop (2:00-6:00 PM)**
```
Production Readiness Checklist:
□ Security implementation
□ Monitoring and logging
□ Performance optimization
□ Error handling and recovery
□ Scalability considerations
□ Documentation and maintenance

Practical Exercises:
1. Security audit of existing code
2. Implement comprehensive logging
3. Set up monitoring dashboards
4. Load testing and optimization
5. Deployment automation
6. Disaster recovery planning

Real-world Scenarios:
- Handle production incidents
- Scale under load
- Manage security vulnerabilities
- Update systems without downtime
```

### Day 5: Capstone Projects

#### Project Development (9:00 AM-4:00 PM)

**Project Kickoff (9:00-10:00 AM)**
```
Project Selection Process:
1. Present three project options (20 min)
2. Form teams based on interests (15 min)
3. Project planning and architecture (20 min)
4. Resource allocation and timeline (5 min)

Instructor Role:
- Facilitate team formation
- Provide technical guidance
- Help with scope management
- Ensure balanced team skills

Success Metrics:
- Clear project objectives
- Realistic timeline
- Balanced team composition
- Technical feasibility
```

**Development Sprint (10:00 AM-3:00 PM)**
```
Sprint Structure:
- 10:00-12:00: Core functionality development
- 1:00-2:00: Integration and testing
- 2:00-3:00: Polish and documentation

Instructor Support:
- Rotating consultation sessions
- Technical problem-solving
- Code review and feedback
- Progress monitoring

Quality Gates:
- Hourly progress check-ins
- Code quality reviews
- Functionality demonstrations
- Documentation completeness
```

**Project Presentations (4:00-6:00 PM)**
```
Presentation Format:
- 10 minutes presentation
- 5 minutes Q&A
- 5 minutes peer feedback

Evaluation Criteria:
- Technical implementation quality
- Innovation and creativity
- Presentation effectiveness
- Problem-solving approach

Celebration Activities:
- Award recognition
- Group photo
- Feedback collection
- Networking session
```

## Troubleshooting Guide

### Common Technical Issues

#### Kiro IDE Problems
```
Issue: Kiro IDE won't start
Solutions:
1. Check system requirements (RAM, OS version)
2. Run as administrator/sudo
3. Clear application cache
4. Reinstall with latest version

Issue: MCP server connection fails
Solutions:
1. Verify JSON configuration syntax
2. Check network connectivity
3. Validate API keys and tokens
4. Restart Kiro IDE

Issue: Slow performance
Solutions:
1. Close unnecessary applications
2. Increase system memory
3. Disable real-time antivirus scanning
4. Use SSD storage if available
```

#### Strands SDK Issues
```
Issue: Import errors
Solutions:
1. Verify virtual environment activation
2. Reinstall packages with pip
3. Check Python version compatibility
4. Clear pip cache

Issue: Tool execution failures
Solutions:
1. Check tool permissions
2. Validate input parameters
3. Review error logs
4. Test tools individually

Issue: Memory backend connection
Solutions:
1. Verify AWS credentials
2. Check network connectivity
3. Validate service endpoints
4. Review IAM permissions
```

#### AWS Integration Problems
```
Issue: Permission denied errors
Solutions:
1. Review IAM policies
2. Check resource ARNs
3. Verify region settings
4. Update access keys

Issue: Service quotas exceeded
Solutions:
1. Request quota increases
2. Implement retry logic
3. Use alternative services
4. Optimize resource usage

Issue: Network connectivity
Solutions:
1. Check VPC configurations
2. Verify security groups
3. Test DNS resolution
4. Review firewall rules
```

### Participant Support Strategies

#### Different Learning Styles
```
Visual Learners:
- Use diagrams and flowcharts
- Provide visual debugging tools
- Create architecture drawings
- Use color-coded examples

Auditory Learners:
- Explain concepts verbally
- Encourage discussion
- Use audio feedback
- Provide verbal instructions

Kinesthetic Learners:
- Hands-on exercises
- Physical movement during breaks
- Interactive demonstrations
- Trial-and-error learning
```

#### Skill Level Adaptation
```
Beginners:
- Provide detailed step-by-step instructions
- Use pair programming
- Offer additional practice exercises
- Schedule one-on-one sessions

Intermediate:
- Focus on best practices
- Encourage experimentation
- Provide challenging extensions
- Facilitate peer mentoring

Advanced:
- Offer complex challenges
- Encourage innovation
- Provide research opportunities
- Assign mentoring roles
```

## Assessment and Feedback

### Real-time Assessment Techniques

#### Formative Assessment
```python
# Digital assessment tool
class WorkshopAssessment:
    def __init__(self):
        self.participants = {}
        self.checkpoints = []
    
    def add_checkpoint(self, name, criteria):
        """Add assessment checkpoint."""
        self.checkpoints.append({
            'name': name,
            'criteria': criteria,
            'timestamp': datetime.now()
        })
    
    def record_progress(self, participant_id, checkpoint, score):
        """Record participant progress."""
        if participant_id not in self.participants:
            self.participants[participant_id] = {}
        
        self.participants[participant_id][checkpoint] = {
            'score': score,
            'timestamp': datetime.now()
        }
    
    def generate_feedback(self, participant_id):
        """Generate personalized feedback."""
        progress = self.participants.get(participant_id, {})
        
        feedback = {
            'strengths': [],
            'areas_for_improvement': [],
            'recommendations': []
        }
        
        # Analyze progress and generate feedback
        for checkpoint, data in progress.items():
            if data['score'] >= 80:
                feedback['strengths'].append(checkpoint)
            elif data['score'] < 60:
                feedback['areas_for_improvement'].append(checkpoint)
        
        return feedback
```

#### Peer Assessment Activities
```
Code Review Sessions:
- Structured peer review process
- Feedback forms and rubrics
- Rotation system for diverse perspectives
- Focus on constructive criticism

Collaborative Problem Solving:
- Team-based challenges
- Cross-team consultation
- Knowledge sharing sessions
- Group debugging exercises

Presentation Practice:
- Mini-presentations throughout
- Peer feedback on communication
- Technical explanation practice
- Confidence building activities
```

### Continuous Improvement

#### Workshop Feedback Collection
```python
# Feedback collection system
feedback_questions = {
    'daily': [
        "What was the most valuable learning today?",
        "What was most challenging?",
        "How can we improve tomorrow's session?",
        "Rate your confidence level (1-10)"
    ],
    'final': [
        "Overall workshop satisfaction (1-10)",
        "Would you recommend this workshop?",
        "What topics need more coverage?",
        "What topics could be reduced?",
        "Instructor effectiveness rating",
        "Materials quality rating",
        "Suggestions for improvement"
    ]
}
```

#### Post-Workshop Support
```
Follow-up Resources:
- Access to workshop materials for 6 months
- Monthly virtual office hours
- Private Discord/Slack community
- Curated resource library
- Project showcase opportunities

Continuing Education:
- Advanced workshop offerings
- Certification maintenance requirements
- Industry update sessions
- Guest expert presentations
- Career development guidance
```

This comprehensive instructor guide provides the framework and detailed guidance needed to successfully deliver the Kiro IDE + Strands SDK workshop, ensuring both instructor preparedness and participant success.