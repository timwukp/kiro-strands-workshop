# Kiro IDE + Strands SDK: Practical Lab Exercises

## Lab Exercise Collection

### Lab 1.1: Kiro IDE First Project Setup

**Objective**: Set up Kiro IDE with proper configuration for agentic AI development

**Prerequisites**: Kiro IDE installed from kiro.dev

**Steps**:

1. **Create New Project**
```bash
# Open Kiro IDE and create new project
mkdir my-agent-project
cd my-agent-project
```

2. **Configure Steering File**
Create `.kiro/steering.md`:
```markdown
# Agent Development Steering

## Project Context
This project focuses on building agentic AI applications using Strands SDK.

## Development Guidelines
- Use Python 3.8+ for all agent implementations
- Follow Strands SDK best practices for tool composition
- Implement proper error handling and logging
- Use type hints for better code clarity
- Test each tool individually before integration

## Code Style
- Use descriptive variable names
- Add docstrings to all functions
- Follow PEP 8 style guidelines
- Use async/await patterns where appropriate

## Agent Behavior Rules
- Always validate input parameters
- Provide clear error messages
- Log important operations
- Handle edge cases gracefully
- Respect user consent for sensitive operations
```

3. **Set up MCP Server Configuration**
Create `.kiro/mcp-servers.json`:
```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    },
    "aws-core": {
      "command": "python",
      "args": ["-m", "awslabs.core_mcp_server"],
      "env": {
        "AWS_REGION": "us-west-2"
      }
    }
  }
}
```

4. **Create First Spec**
Use Kiro's natural language interface:
```
Create a spec for a simple file processing agent that can:
- Read text files from a directory
- Count word frequencies
- Generate summary reports
- Save results to JSON format
```

**Expected Output**: Working Kiro IDE project with proper configuration

---

### Lab 2.1: Document Processing Agent

**Objective**: Build an agent that processes documents and generates insights

**Code Template**:
```python
from strands import Agent, tool
from strands_tools import file_read, file_write, python_repl
import json
import re
from collections import Counter
from pathlib import Path

@tool
def analyze_document(file_path: str) -> dict:
    """
    Analyze a document and return statistics.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Dictionary containing document analysis
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic statistics
        word_count = len(content.split())
        char_count = len(content)
        line_count = len(content.splitlines())
        
        # Word frequency analysis
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = Counter(words)
        
        return {
            "file_path": file_path,
            "word_count": word_count,
            "character_count": char_count,
            "line_count": line_count,
            "top_words": word_freq.most_common(10),
            "unique_words": len(word_freq)
        }
    except Exception as e:
        return {"error": str(e)}

@tool
def batch_analyze_directory(directory_path: str) -> dict:
    """
    Analyze all text files in a directory.
    
    Args:
        directory_path: Path to directory containing text files
        
    Returns:
        Dictionary containing analysis of all files
    """
    results = {}
    directory = Path(directory_path)
    
    for file_path in directory.glob("*.txt"):
        analysis = analyze_document(str(file_path))
        results[file_path.name] = analysis
    
    return results

# Create the agent
agent = Agent(tools=[
    file_read, 
    file_write, 
    python_repl,
    analyze_document,
    batch_analyze_directory
])

# Test the agent
if __name__ == "__main__":
    # Create sample documents for testing
    test_message = """
    I need you to:
    1. Create 3 sample text files with different content
    2. Analyze each file individually
    3. Perform batch analysis on all files
    4. Generate a summary report in JSON format
    5. Save the results to 'analysis_report.json'
    """
    
    response = agent(test_message)
    print(response)
```

**Exercise Tasks**:
1. Extend the agent to handle PDF files
2. Add sentiment analysis capability
3. Implement keyword extraction
4. Create visualization of word frequencies

---

### Lab 2.2: API Integration Agent

**Objective**: Build an agent that interacts with external APIs and processes data

**Code Template**:
```python
from strands import Agent, tool
from strands_tools import http_request, file_write, python_repl
import json
from datetime import datetime

@tool
def fetch_weather_data(city: str, api_key: str) -> dict:
    """
    Fetch weather data for a specific city.
    
    Args:
        city: Name of the city
        api_key: OpenWeatherMap API key
        
    Returns:
        Weather data dictionary
    """
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        # Note: In real implementation, use http_request tool
        # This is a template showing the structure
        response_data = {
            "city": city,
            "temperature": 22.5,
            "humidity": 65,
            "description": "partly cloudy",
            "timestamp": datetime.now().isoformat()
        }
        return response_data
    except Exception as e:
        return {"error": str(e)}

@tool
def process_api_response(response_data: dict) -> str:
    """
    Process API response and create human-readable summary.
    
    Args:
        response_data: Raw API response data
        
    Returns:
        Formatted summary string
    """
    if "error" in response_data:
        return f"Error processing data: {response_data['error']}"
    
    summary = f"""
    Weather Report for {response_data.get('city', 'Unknown')}
    ================================================
    Temperature: {response_data.get('temperature', 'N/A')}°C
    Humidity: {response_data.get('humidity', 'N/A')}%
    Conditions: {response_data.get('description', 'N/A')}
    Updated: {response_data.get('timestamp', 'N/A')}
    """
    
    return summary.strip()

# Create the agent
agent = Agent(tools=[
    http_request,
    file_write,
    python_repl,
    fetch_weather_data,
    process_api_response
])

# Example usage
if __name__ == "__main__":
    test_message = """
    Please help me:
    1. Fetch weather data for New York, London, and Tokyo
    2. Process each response into a readable format
    3. Create a combined weather report
    4. Save the report to 'weather_report.txt'
    5. Also save the raw data as JSON for future reference
    
    Use the http_request tool to make actual API calls to a weather service.
    """
    
    response = agent(test_message)
    print(response)
```

**Exercise Extensions**:
1. Add error handling for API rate limits
2. Implement caching mechanism
3. Add support for multiple API endpoints
4. Create automated reporting schedule

---

### Lab 3.1: Personal Assistant with Memory

**Objective**: Create an agent with persistent memory capabilities

**Code Template**:
```python
from strands import Agent, tool
from strands_tools.agent_core_memory import AgentCoreMemoryToolProvider
from strands_tools import current_time, calculator
import json
from datetime import datetime

@tool
def create_reminder(reminder_text: str, due_date: str = None) -> dict:
    """
    Create a reminder with optional due date.
    
    Args:
        reminder_text: The reminder content
        due_date: Optional due date in YYYY-MM-DD format
        
    Returns:
        Reminder creation confirmation
    """
    reminder = {
        "id": f"reminder_{datetime.now().timestamp()}",
        "text": reminder_text,
        "due_date": due_date,
        "created_at": datetime.now().isoformat(),
        "completed": False
    }
    
    return {
        "status": "created",
        "reminder": reminder,
        "message": f"Reminder created: {reminder_text}"
    }

@tool
def analyze_user_preferences(conversation_history: str) -> dict:
    """
    Analyze conversation history to extract user preferences.
    
    Args:
        conversation_history: Recent conversation text
        
    Returns:
        Extracted preferences and insights
    """
    # Simple keyword-based preference extraction
    preferences = {
        "communication_style": "professional" if "formal" in conversation_history.lower() else "casual",
        "preferred_time": "morning" if "morning" in conversation_history.lower() else "flexible",
        "interests": [],
        "work_patterns": []
    }
    
    # Extract interests based on keywords
    interest_keywords = ["coding", "music", "sports", "reading", "travel", "cooking"]
    for keyword in interest_keywords:
        if keyword in conversation_history.lower():
            preferences["interests"].append(keyword)
    
    return preferences

# Configure memory provider
memory_provider = AgentCoreMemoryToolProvider(
    memory_id="personal-assistant-memory",
    actor_id="user-main",
    session_id=f"session-{datetime.now().strftime('%Y%m%d')}",
    namespace="personal_assistant",
    region="us-west-2"
)

# Create the agent with memory capabilities
agent = Agent(tools=[
    *memory_provider.tools,
    current_time,
    calculator,
    create_reminder,
    analyze_user_preferences
])

# Example interaction
if __name__ == "__main__":
    test_message = """
    Hi! I'm looking for a personal assistant that can help me with:
    1. Remembering my preferences (I prefer morning meetings, like coding and music)
    2. Setting reminders for important tasks
    3. Tracking my work patterns
    4. Providing personalized suggestions based on my history
    
    Can you help me set up a reminder for my team meeting tomorrow at 10 AM?
    Also, please remember that I prefer technical discussions to be detailed.
    """
    
    response = agent(test_message)
    print(response)
```

**Advanced Features to Implement**:
1. Smart scheduling based on preferences
2. Context-aware suggestions
3. Learning from user feedback
4. Integration with calendar systems

---

### Lab 3.3: Multi-Agent Problem Solving System

**Objective**: Create a swarm of specialized agents for complex problem solving

**Code Template**:
```python
from strands import Agent, tool
from strands_tools import swarm, python_repl, http_request, memory
import json

@tool
def create_research_agent_spec() -> dict:
    """Create specification for a research agent."""
    return {
        "role": "researcher",
        "capabilities": [
            "web_search",
            "data_collection",
            "fact_verification",
            "source_citation"
        ],
        "tools": ["http_request", "memory"],
        "personality": "thorough and analytical"
    }

@tool
def create_analysis_agent_spec() -> dict:
    """Create specification for an analysis agent."""
    return {
        "role": "analyst",
        "capabilities": [
            "data_processing",
            "statistical_analysis",
            "pattern_recognition",
            "insight_generation"
        ],
        "tools": ["python_repl", "calculator", "memory"],
        "personality": "logical and detail-oriented"
    }

@tool
def create_synthesis_agent_spec() -> dict:
    """Create specification for a synthesis agent."""
    return {
        "role": "synthesizer",
        "capabilities": [
            "information_integration",
            "report_generation",
            "recommendation_creation",
            "presentation_formatting"
        ],
        "tools": ["file_write", "memory"],
        "personality": "creative and communicative"
    }

@tool
def coordinate_agent_workflow(task: str, agent_specs: list) -> dict:
    """
    Coordinate workflow between multiple specialized agents.
    
    Args:
        task: The main task to be solved
        agent_specs: List of agent specifications
        
    Returns:
        Workflow coordination plan
    """
    workflow = {
        "task": task,
        "phases": [
            {
                "phase": "research",
                "agent": "researcher",
                "objective": "Gather relevant information and data",
                "deliverable": "research_report.json"
            },
            {
                "phase": "analysis",
                "agent": "analyst",
                "objective": "Process and analyze collected data",
                "deliverable": "analysis_results.json"
            },
            {
                "phase": "synthesis",
                "agent": "synthesizer",
                "objective": "Create final recommendations and report",
                "deliverable": "final_report.md"
            }
        ],
        "coordination_pattern": "sequential_with_feedback"
    }
    
    return workflow

# Create the coordinator agent
coordinator_agent = Agent(tools=[
    swarm,
    python_repl,
    http_request,
    memory,
    create_research_agent_spec,
    create_analysis_agent_spec,
    create_synthesis_agent_spec,
    coordinate_agent_workflow
])

# Example multi-agent task
if __name__ == "__main__":
    complex_task = """
    I need to analyze the current state of AI development in healthcare.
    Please coordinate a team of specialized agents to:
    
    1. Research current AI applications in healthcare
    2. Analyze market trends and adoption rates
    3. Identify key challenges and opportunities
    4. Synthesize findings into actionable recommendations
    
    Use a collaborative swarm approach with:
    - A research agent for data gathering
    - An analysis agent for processing information
    - A synthesis agent for creating the final report
    
    The agents should work together and share information throughout the process.
    """
    
    response = coordinator_agent(complex_task)
    print(response)
```

**Swarm Coordination Patterns**:
1. **Sequential**: Agents work in order, passing results forward
2. **Parallel**: Agents work simultaneously on different aspects
3. **Collaborative**: Agents share information and iterate together
4. **Competitive**: Multiple agents propose solutions, best one selected

---

### Lab 4.1: Cloud-Native Agent with AWS Integration

**Objective**: Build an agent that leverages AWS services for scalable operations

**Code Template**:
```python
from strands import Agent, tool
from strands_tools import use_aws, memory, http_request, file_write
import json
from datetime import datetime

@tool
def setup_s3_data_pipeline(bucket_name: str) -> dict:
    """
    Set up S3 bucket for data pipeline operations.
    
    Args:
        bucket_name: Name of the S3 bucket to create/configure
        
    Returns:
        Setup confirmation and configuration details
    """
    pipeline_config = {
        "bucket_name": bucket_name,
        "folders": [
            "raw-data/",
            "processed-data/",
            "reports/",
            "logs/"
        ],
        "lifecycle_policy": {
            "transition_to_ia": 30,
            "transition_to_glacier": 90,
            "expiration": 365
        }
    }
    
    return {
        "status": "configured",
        "config": pipeline_config,
        "next_steps": [
            "Create bucket using use_aws tool",
            "Set up folder structure",
            "Configure lifecycle policies"
        ]
    }

@tool
def process_dynamodb_records(table_name: str, query_params: dict) -> dict:
    """
    Process records from DynamoDB table.
    
    Args:
        table_name: Name of the DynamoDB table
        query_params: Query parameters for filtering records
        
    Returns:
        Processed records and summary statistics
    """
    # Template for DynamoDB processing logic
    processing_summary = {
        "table_name": table_name,
        "query_params": query_params,
        "records_processed": 0,
        "processing_time": datetime.now().isoformat(),
        "status": "ready_for_aws_integration"
    }
    
    return processing_summary

@tool
def trigger_lambda_workflow(function_name: str, payload: dict) -> dict:
    """
    Trigger AWS Lambda function for serverless processing.
    
    Args:
        function_name: Name of the Lambda function
        payload: Data to send to the function
        
    Returns:
        Lambda invocation result
    """
    invocation_request = {
        "function_name": function_name,
        "payload": payload,
        "invocation_type": "RequestResponse",
        "timestamp": datetime.now().isoformat()
    }
    
    return {
        "status": "prepared",
        "request": invocation_request,
        "note": "Use use_aws tool to actually invoke Lambda"
    }

# Create cloud-native agent
cloud_agent = Agent(tools=[
    use_aws,
    memory,
    http_request,
    file_write,
    setup_s3_data_pipeline,
    process_dynamodb_records,
    trigger_lambda_workflow
])

# Example cloud operations
if __name__ == "__main__":
    cloud_task = """
    Help me set up a cloud-native data processing pipeline:
    
    1. Create an S3 bucket called 'my-agent-data-pipeline'
    2. Set up the folder structure for raw data, processed data, and reports
    3. Query a DynamoDB table called 'user-interactions' for recent records
    4. Process the data and generate insights
    5. Store the results back in S3
    6. Trigger a Lambda function to send notifications
    
    Use the AWS tools to perform actual cloud operations.
    Make sure to handle errors gracefully and log all operations.
    """
    
    response = cloud_agent(cloud_task)
    print(response)
```

**AWS Integration Patterns**:
1. **Data Pipeline**: S3 → Lambda → DynamoDB → SQS
2. **Event-Driven**: CloudWatch Events → Lambda → SNS
3. **Batch Processing**: S3 → Batch → EC2 → S3
4. **Real-time**: Kinesis → Lambda → DynamoDB

---

### Lab 5.2: Capstone Project Templates

#### Template A: Business Process Automation Agent

```python
"""
Automated Customer Support System
=================================

This agent handles customer inquiries through multiple channels,
processes requests, and provides automated responses with escalation
capabilities.
"""

from strands import Agent, tool
from strands_tools import (
    http_request, file_read, file_write, memory, 
    use_aws, python_repl, current_time
)
import json
from datetime import datetime, timedelta

class CustomerSupportAgent:
    def __init__(self):
        self.agent = Agent(tools=[
            http_request, file_read, file_write, memory,
            use_aws, python_repl, current_time,
            self.categorize_inquiry,
            self.generate_response,
            self.escalate_to_human,
            self.update_knowledge_base,
            self.track_metrics
        ])
    
    @tool
    def categorize_inquiry(self, inquiry_text: str) -> dict:
        """Categorize customer inquiry using NLP."""
        # Implementation for inquiry categorization
        pass
    
    @tool
    def generate_response(self, category: str, inquiry: str) -> dict:
        """Generate appropriate response based on category."""
        # Implementation for response generation
        pass
    
    @tool
    def escalate_to_human(self, inquiry_id: str, reason: str) -> dict:
        """Escalate complex issues to human agents."""
        # Implementation for escalation logic
        pass
    
    @tool
    def update_knowledge_base(self, new_info: dict) -> dict:
        """Update knowledge base with new information."""
        # Implementation for knowledge base updates
        pass
    
    @tool
    def track_metrics(self, interaction_data: dict) -> dict:
        """Track performance metrics and analytics."""
        # Implementation for metrics tracking
        pass

# Usage example
support_agent = CustomerSupportAgent()
```

#### Template B: Content Creation & Management Agent

```python
"""
Multi-Media Content Pipeline
============================

This agent manages the entire content creation lifecycle from
planning and research to generation, optimization, and distribution.
"""

from strands import Agent, tool
from strands_tools import (
    generate_image, nova_reels, http_request, file_write,
    memory, python_repl, current_time
)

class ContentCreationAgent:
    def __init__(self):
        self.agent = Agent(tools=[
            generate_image, nova_reels, http_request, file_write,
            memory, python_repl, current_time,
            self.research_topic,
            self.create_content_plan,
            self.generate_text_content,
            self.optimize_for_seo,
            self.schedule_publication,
            self.analyze_performance
        ])
    
    @tool
    def research_topic(self, topic: str) -> dict:
        """Research topic and gather relevant information."""
        # Implementation for topic research
        pass
    
    @tool
    def create_content_plan(self, research_data: dict) -> dict:
        """Create comprehensive content plan."""
        # Implementation for content planning
        pass
    
    @tool
    def generate_text_content(self, plan: dict) -> dict:
        """Generate text content based on plan."""
        # Implementation for text generation
        pass
    
    @tool
    def optimize_for_seo(self, content: str) -> dict:
        """Optimize content for search engines."""
        # Implementation for SEO optimization
        pass
    
    @tool
    def schedule_publication(self, content: dict, schedule: dict) -> dict:
        """Schedule content for publication across platforms."""
        # Implementation for content scheduling
        pass
    
    @tool
    def analyze_performance(self, content_id: str) -> dict:
        """Analyze content performance metrics."""
        # Implementation for performance analysis
        pass

# Usage example
content_agent = ContentCreationAgent()
```

These lab exercises provide hands-on experience with the key concepts and tools needed to build sophisticated agentic AI applications using Kiro IDE and Strands SDK. Each lab builds upon previous knowledge while introducing new capabilities and best practices.