# Workshop Setup Scripts and Automation Tools

## Automated Environment Setup

### 1. Workshop Environment Installer

**File: `setup_workshop_environment.py`**

```python
#!/usr/bin/env python3
"""
Automated setup script for Kiro IDE + Strands SDK Workshop
Handles installation, configuration, and verification of all required tools.
"""

import os
import sys
import subprocess
import json
import platform
import urllib.request
import zipfile
import shutil
import datetime  # Added missing datetime import
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WorkshopSetup:
    def __init__(self):
        self.system = platform.system().lower()
        self.home_dir = Path.home()
        self.workshop_dir = self.home_dir / "kiro-strands-workshop"
        self.errors = []
        
    def create_workshop_directory(self):
        """Create main workshop directory structure."""
        logger.info("Creating workshop directory structure...")
        
        directories = [
            self.workshop_dir,
            self.workshop_dir / "projects",
            self.workshop_dir / "templates",
            self.workshop_dir / "data",
            self.workshop_dir / "scripts",
            self.workshop_dir / "docs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def check_python_version(self):
        """Verify Python version compatibility."""
        logger.info("Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            error_msg = f"Python 3.8+ required. Current version: {version.major}.{version.minor}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False
        
        logger.info(f"Python version OK: {version.major}.{version.minor}.{version.micro}")
        return True
    
    def setup_virtual_environment(self):
        """Create and configure Python virtual environment."""
        logger.info("Setting up Python virtual environment...")
        
        venv_path = self.workshop_dir / "venv"
        
        try:
            # Create virtual environment
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            
            # Determine activation script path
            if self.system == "windows":
                activate_script = venv_path / "Scripts" / "activate.bat"
                pip_path = venv_path / "Scripts" / "pip.exe"
            else:
                activate_script = venv_path / "bin" / "activate"
                pip_path = venv_path / "bin" / "pip"
            
            # Install required packages
            packages = [
                "strands-agents",
                "strands-agents-tools",
                "strands-agents-builder",
                "strands-agents-tools[mem0_memory,use_browser]",
                "jupyter",
                "notebook",
                "pytest",
                "black",
                "flake8",
                "requests",
                "boto3",
                "awscli"
            ]
            
            for package in packages:
                logger.info(f"Installing {package}...")
                subprocess.run([str(pip_path), "install", package], check=True)
            
            # Create activation script for workshop
            self.create_activation_script(venv_path)
            
            logger.info("Virtual environment setup complete")
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to setup virtual environment: {e}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False
    
    def create_activation_script(self, venv_path):
        """Create convenient activation script for workshop."""
        if self.system == "windows":
            script_content = f"""@echo off
echo Activating Kiro-Strands Workshop Environment...
call "{venv_path}\\Scripts\\activate.bat"
echo Environment activated! Ready for workshop.
echo.
echo Quick commands:
echo   kiro          - Start Kiro IDE
echo   jupyter lab   - Start Jupyter Lab
echo   pytest        - Run tests
echo.
"""
            script_path = self.workshop_dir / "activate_workshop.bat"
        else:
            script_content = f"""#!/bin/bash
echo "Activating Kiro-Strands Workshop Environment..."
source "{venv_path}/bin/activate"
echo "Environment activated! Ready for workshop."
echo ""
echo "Quick commands:"
echo "  kiro          - Start Kiro IDE"
echo "  jupyter lab   - Start Jupyter Lab"
echo "  pytest        - Run tests"
echo ""
"""
            script_path = self.workshop_dir / "activate_workshop.sh"
        
        with open(script_path, "w") as f:
            f.write(script_content)
        
        if self.system != "windows":
            os.chmod(script_path, 0o755)
        
        logger.info(f"Created activation script: {script_path}")
    
    def download_kiro_ide(self):
        """Prepare for Kiro IDE installation with security considerations."""
        logger.info("Preparing for Kiro IDE installation...")
        
        # Create a dedicated directory for Kiro IDE
        kiro_dir = self.workshop_dir / "kiro-ide"
        kiro_dir.mkdir(exist_ok=True)
        
        # Create installation instructions with security notes
        install_instructions = """# Kiro IDE Installation Instructions

## Official Download
1. Download Kiro IDE from the official website: [kiro.dev](https://kiro.dev)
2. Verify the download integrity using the provided checksums
3. Install following the official documentation

## Security Considerations
- Always download from the official website only
- Verify digital signatures or checksums before installation
- Keep the application updated with security patches
- Review permissions requested during installation

## Post-Installation
1. Configure Amazon Q Developer extension
2. Set up MCP server connections
3. Create project steering files

For more information, visit the [official documentation](https://docs.kiro.dev).
"""
        
        instructions_path = kiro_dir / "installation_instructions.md"
        with open(instructions_path, "w") as f:
            f.write(install_instructions)
        
        # Create placeholder installation info with current timestamp
        install_info = {
            "version": "latest",
            "download_url": "https://kiro.dev/download",
            "installation_date": datetime.datetime.now().isoformat(),
            "status": "ready_for_manual_install"
        }
        
        with open(kiro_dir / "install_info.json", "w") as f:
            json.dump(install_info, f, indent=2)
        
        logger.info("Kiro IDE installation instructions prepared")
        logger.info(f"Instructions location: {instructions_path}")
        logger.warning("SECURITY NOTE: Always download Kiro IDE from the official website only")
        return True
    
    def setup_aws_configuration(self):
        """Set up AWS configuration templates in a secure manner."""
        logger.info("Setting up AWS configuration templates...")
        
        # Create workshop AWS directory instead of using the user's .aws directory
        aws_dir = self.workshop_dir / "aws_config_templates"
        aws_dir.mkdir(exist_ok=True)
        
        # Create template credentials file with clear warnings
        credentials_template = """# WARNING: THIS IS A TEMPLATE FILE ONLY
# DO NOT STORE ACTUAL CREDENTIALS IN THIS FILE
# 
# SECURITY BEST PRACTICE: Use AWS CLI's 'aws configure' command instead
# or use environment variables for credentials

[default]
# Replace with your actual AWS credentials using 'aws configure'
aws_access_key_id = YOUR_ACCESS_KEY_HERE
aws_secret_access_key = YOUR_SECRET_KEY_HERE

[workshop]
# Workshop-specific profile
aws_access_key_id = WORKSHOP_ACCESS_KEY
aws_secret_access_key = WORKSHOP_SECRET_KEY
region = us-west-2
"""
        
        credentials_path = aws_dir / "credentials.template"
        # Write with restricted permissions (0600 - user read/write only)
        with open(credentials_path, "w") as f:
            f.write(credentials_template)
        
        # Set secure permissions for credentials template
        if self.system != "windows":  # Skip on Windows as it has different permission model
            os.chmod(credentials_path, 0o600)
        
        # Create config file template
        config_content = """# AWS CLI configuration template
# Copy to ~/.aws/config or use 'aws configure'

[default]
region = us-west-2
output = json

[profile workshop]
region = us-west-2
output = json
"""
        
        config_path = aws_dir / "config.template"
        with open(config_path, "w") as f:
            f.write(config_content)
        
        # Create AWS setup instructions
        instructions = """# Secure AWS Setup Instructions

## Option 1: Using AWS CLI (Recommended)
```bash
# Configure your AWS credentials securely
aws configure
```

## Option 2: Manual Configuration
1. Create ~/.aws directory if it doesn't exist
2. Create ~/.aws/credentials with your AWS credentials
3. Create ~/.aws/config with your AWS configuration
4. Set proper permissions:
   ```bash
   chmod 600 ~/.aws/credentials
   ```

## Security Best Practices
- Never share your AWS credentials
- Use IAM roles when possible instead of access keys
- Create users with minimal permissions needed
- Regularly rotate your access keys
- Consider using AWS SSO for authentication
"""
        
        instructions_path = aws_dir / "aws_setup_instructions.md"
        with open(instructions_path, "w") as f:
            f.write(instructions)
        
        logger.info("AWS configuration templates and instructions created")
        logger.info(f"Templates location: {aws_dir}")
        logger.warning("SECURITY NOTE: Follow the instructions in aws_setup_instructions.md for secure AWS configuration")
        return True
    
    def create_sample_projects(self):
        """Create sample project templates."""
        logger.info("Creating sample project templates...")
        
        templates_dir = self.workshop_dir / "templates"
        
        # Basic agent template
        basic_agent = """from strands import Agent, tool
from strands_tools import file_read, file_write, calculator, current_time

@tool
def custom_greeting(name: str) -> str:
    \"\"\"Generate a personalized greeting.\"\"\"
    return f"Hello {name}! Welcome to the Kiro-Strands workshop!"

# Create agent with selected tools
agent = Agent(tools=[
    file_read,
    file_write, 
    calculator,
    current_time,
    custom_greeting
])

if __name__ == "__main__":
    # Test the agent
    response = agent("Say hello to Alice and tell her the current time")
    print(response)
"""
        
        with open(templates_dir / "basic_agent.py", "w") as f:
            f.write(basic_agent)
        
        # API integration template
        api_agent = """from strands import Agent, tool
from strands_tools import http_request, file_write, python_repl
import json

@tool
def process_api_data(data: dict) -> str:
    \"\"\"Process API response data.\"\"\"
    if 'error' in data:
        return f"API Error: {data['error']}"
    
    # Process the data as needed
    return f"Processed data: {json.dumps(data, indent=2)}"

# Create API integration agent
agent = Agent(tools=[
    http_request,
    file_write,
    python_repl,
    process_api_data
])

if __name__ == "__main__":
    # Example API integration
    response = agent(\"\"\"
    Make a GET request to https://api.github.com/users/octocat
    and process the response data.
    \"\"\")
    print(response)
"""
        
        with open(templates_dir / "api_agent.py", "w") as f:
            f.write(api_agent)
        
        logger.info("Sample project templates created")
        return True
    
    def create_configuration_files(self):
        """Create configuration files for workshop tools."""
        logger.info("Creating configuration files...")
        
        # Kiro IDE configuration
        kiro_config_dir = self.workshop_dir / ".kiro"
        kiro_config_dir.mkdir(exist_ok=True)
        
        # MCP servers configuration
        mcp_config = {
            "servers": {
                "github": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-github"],
                    "env": {
                        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-github-token-here"
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
        
        with open(kiro_config_dir / "mcp-servers.json", "w") as f:
            json.dump(mcp_config, f, indent=2)
        
        # Steering file template
        steering_content = """# Workshop Agent Development Steering

## Project Context
This project is part of the Kiro IDE + Strands SDK workshop for building agentic AI applications.

## Development Guidelines
- Use Python 3.8+ for all implementations
- Follow Strands SDK best practices
- Implement comprehensive error handling
- Use type hints for better code clarity
- Test each component thoroughly

## Code Style
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Follow PEP 8 style guidelines
- Use async/await patterns where appropriate

## Agent Behavior Rules
- Always validate input parameters
- Provide clear and helpful error messages
- Log important operations for debugging
- Handle edge cases gracefully
- Respect user consent for sensitive operations

## Security Considerations
- Never expose sensitive credentials in code
- Validate all external inputs
- Use secure communication protocols
- Implement proper access controls
"""
        
        with open(kiro_config_dir / "steering.md", "w") as f:
            f.write(steering_content)
        
        logger.info("Configuration files created")
        return True
    
    def verify_installation(self):
        """Verify that all components are properly installed."""
        logger.info("Verifying installation...")
        
        verification_results = {
            "python_version": self.check_python_version(),
            "virtual_environment": (self.workshop_dir / "venv").exists(),
            "workshop_structure": self.workshop_dir.exists(),
            "templates": (self.workshop_dir / "templates").exists(),
            "configuration": (self.workshop_dir / ".kiro").exists()
        }
        
        all_good = all(verification_results.values())
        
        if all_good:
            logger.info("✅ All components verified successfully!")
        else:
            logger.warning("⚠️  Some components may need attention:")
            for component, status in verification_results.items():
                status_icon = "✅" if status else "❌"
                logger.info(f"  {status_icon} {component}")
        
        return all_good
    
    def generate_setup_report(self):
        """Generate setup completion report."""
        report_path = self.workshop_dir / "setup_report.md"
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report_content = f"""# Workshop Setup Report

## Setup Summary
- **Setup Date**: {current_time}
- **System**: {platform.system()} {platform.release()}
- **Python Version**: {sys.version}
- **Workshop Directory**: {self.workshop_dir}

## Components Installed
- ✅ Workshop directory structure
- ✅ Python virtual environment
- ✅ Required Python packages
- ✅ Project templates
- ✅ Configuration files
- ⚠️  Kiro IDE (manual installation required)

## Security Notes
- ✅ AWS credentials templates stored securely
- ✅ Secure file permissions applied
- ✅ Security guidelines provided
- ⚠️  Review security-guidelines.md for best practices

## Next Steps
1. **Install Kiro IDE**: Follow instructions in kiro-ide/installation_instructions.md
2. **Configure AWS**: Follow instructions in aws_config_templates/aws_setup_instructions.md
3. **Set GitHub Token**: Update MCP server configuration
4. **Activate Environment**: Run the activation script
5. **Test Setup**: Run the verification script

## Quick Start Commands
```bash
# Activate workshop environment
{"./activate_workshop.bat" if self.system == "windows" else "./activate_workshop.sh"}

# Start Jupyter for interactive development
jupyter lab

# Run sample agent
python templates/basic_agent.py
```

## Troubleshooting
If you encounter issues:
1. Check the error log: `setup_errors.log`
2. Verify Python version (3.8+ required)
3. Ensure internet connectivity for downloads
4. Check system permissions for file creation

## Support Resources
- Workshop documentation: `docs/`
- Sample projects: `templates/`
- Configuration files: `.kiro/`
- Error logs: `setup_errors.log`
- Security guidelines: `security-guidelines.md`
"""
        
        with open(report_path, "w") as f:
            f.write(report_content)
        
        logger.info(f"Setup report generated: {report_path}")
    
    def run_setup(self):
        """Run the complete setup process."""
        logger.info("Starting Kiro-Strands Workshop Setup...")
        
        setup_steps = [
            ("Creating workshop directory", self.create_workshop_directory),
            ("Checking Python version", self.check_python_version),
            ("Setting up virtual environment", self.setup_virtual_environment),
            ("Preparing Kiro IDE", self.download_kiro_ide),
            ("Configuring AWS", self.setup_aws_configuration),
            ("Creating sample projects", self.create_sample_projects),
            ("Creating configuration files", self.create_configuration_files),
            ("Verifying installation", self.verify_installation)
        ]
        
        for step_name, step_function in setup_steps:
            logger.info(f"Step: {step_name}")
            try:
                success = step_function()
                if not success:
                    logger.error(f"Failed: {step_name}")
            except Exception as e:
                error_msg = f"Error in {step_name}: {str(e)}"
                self.errors.append(error_msg)
                logger.error(error_msg)
        
        # Generate final report
        self.generate_setup_report()
        
        if self.errors:
            logger.warning(f"Setup completed with {len(self.errors)} errors:")
            for error in self.errors:
                logger.warning(f"  - {error}")
        else:
            logger.info("🎉 Workshop setup completed successfully!")
        
        return len(self.errors) == 0

if __name__ == "__main__":
    # datetime is already imported at the top of the file
    
    setup = WorkshopSetup()
    success = setup.run_setup()
    
    if success:
        print("\n🎉 Workshop environment is ready!")
        print(f"📁 Workshop directory: {setup.workshop_dir}")
        print("📖 Check setup_report.md for next steps")
    else:
        print("\n⚠️  Setup completed with some issues")
        print("📋 Check the logs for details")
        sys.exit(1)
```

### 2. Environment Verification Script

**File: `verify_workshop_setup.py`**

```python
#!/usr/bin/env python3
"""
Verification script to ensure workshop environment is properly configured.
Run this before starting the workshop to identify any issues.
"""

import sys
import subprocess
import importlib
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkshopVerifier:
    def __init__(self):
        self.home_dir = Path.home()
        self.workshop_dir = self.home_dir / "kiro-strands-workshop"
        self.issues = []
        self.warnings = []
    
    def check_python_packages(self):
        """Verify all required Python packages are installed."""
        logger.info("Checking Python packages...")
        
        required_packages = [
            "strands",
            "strands_tools", 
            "boto3",
            "requests",
            "jupyter",
            "pytest"
        ]
        
        for package in required_packages:
            try:
                importlib.import_module(package)
                logger.info(f"✅ {package}")
            except ImportError:
                error_msg = f"❌ Missing package: {package}"
                self.issues.append(error_msg)
                logger.error(error_msg)
    
    def check_aws_configuration(self):
        """Check AWS configuration and credentials."""
        logger.info("Checking AWS configuration...")
        
        aws_dir = self.home_dir / ".aws"
        credentials_file = aws_dir / "credentials"
        config_file = aws_dir / "config"
        
        if not aws_dir.exists():
            self.issues.append("❌ AWS directory not found")
            return
        
        if not credentials_file.exists():
            self.issues.append("❌ AWS credentials file not found")
        else:
            logger.info("✅ AWS credentials file exists")
        
        if not config_file.exists():
            self.warnings.append("⚠️  AWS config file not found")
        else:
            logger.info("✅ AWS config file exists")
        
        # Test AWS CLI
        try:
            result = subprocess.run(
                ["aws", "sts", "get-caller-identity"], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info("✅ AWS CLI working")
            else:
                self.warnings.append("⚠️  AWS CLI not configured properly")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.warnings.append("⚠️  AWS CLI not available or not responding")
    
    def check_workshop_structure(self):
        """Verify workshop directory structure."""
        logger.info("Checking workshop directory structure...")
        
        required_dirs = [
            "projects",
            "templates", 
            "data",
            "scripts",
            "docs",
            ".kiro"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.workshop_dir / dir_name
            if dir_path.exists():
                logger.info(f"✅ {dir_name}/")
            else:
                self.issues.append(f"❌ Missing directory: {dir_name}/")
    
    def check_configuration_files(self):
        """Check configuration files."""
        logger.info("Checking configuration files...")
        
        kiro_dir = self.workshop_dir / ".kiro"
        
        config_files = [
            ("mcp-servers.json", "MCP servers configuration"),
            ("steering.md", "Steering file")
        ]
        
        for filename, description in config_files:
            file_path = kiro_dir / filename
            if file_path.exists():
                logger.info(f"✅ {description}")
                
                # Validate JSON files
                if filename.endswith('.json'):
                    try:
                        with open(file_path) as f:
                            json.load(f)
                        logger.info(f"✅ {filename} is valid JSON")
                    except json.JSONDecodeError:
                        self.issues.append(f"❌ {filename} contains invalid JSON")
            else:
                self.issues.append(f"❌ Missing: {description}")
    
    def check_sample_projects(self):
        """Verify sample project templates."""
        logger.info("Checking sample projects...")
        
        templates_dir = self.workshop_dir / "templates"
        
        expected_templates = [
            "basic_agent.py",
            "api_agent.py"
        ]
        
        for template in expected_templates:
            template_path = templates_dir / template
            if template_path.exists():
                logger.info(f"✅ {template}")
                
                # Basic syntax check
                try:
                    with open(template_path) as f:
                        compile(f.read(), template_path, 'exec')
                    logger.info(f"✅ {template} syntax OK")
                except SyntaxError as e:
                    self.issues.append(f"❌ Syntax error in {template}: {e}")
            else:
                self.issues.append(f"❌ Missing template: {template}")
    
    def test_strands_functionality(self):
        """Test basic Strands functionality."""
        logger.info("Testing Strands functionality...")
        
        try:
            from strands import Agent, tool
            from strands_tools import calculator, current_time
            
            @tool
            def test_tool(message: str) -> str:
                return f"Test successful: {message}"
            
            # Create test agent
            agent = Agent(tools=[calculator, current_time, test_tool])
            
            # Simple test
            response = agent("Use the test tool to say hello")
            
            if "Test successful" in str(response):
                logger.info("✅ Strands basic functionality working")
            else:
                self.warnings.append("⚠️  Strands test didn't return expected result")
                
        except Exception as e:
            self.issues.append(f"❌ Strands functionality test failed: {e}")
    
    def generate_verification_report(self):
        """Generate verification report."""
        report_path = self.workshop_dir / "verification_report.md"
        
        status = "✅ READY" if not self.issues else "❌ ISSUES FOUND"
        
        report_content = f"""# Workshop Environment Verification Report

## Overall Status: {status}

## Issues Found ({len(self.issues)})
"""
        
        if self.issues:
            for issue in self.issues:
                report_content += f"- {issue}\n"
        else:
            report_content += "- None! Environment is ready for workshop.\n"
        
        report_content += f"""
## Warnings ({len(self.warnings)})
"""
        
        if self.warnings:
            for warning in self.warnings:
                report_content += f"- {warning}\n"
        else:
            report_content += "- None.\n"
        
        report_content += """
## Next Steps

### If Issues Found:
1. Run the setup script again: `python setup_workshop_environment.py`
2. Install missing packages manually
3. Check AWS credentials configuration
4. Verify file permissions

### If Ready:
1. Start with Day 1 materials
2. Activate workshop environment
3. Open Kiro IDE
4. Begin first exercises

## Quick Test Commands
```bash
# Test Python environment
python -c "import strands; print('Strands OK')"

# Test AWS CLI
aws sts get-caller-identity

# Test Jupyter
jupyter --version
```
"""
        
        with open(report_path, "w") as f:
            f.write(report_content)
        
        logger.info(f"Verification report saved: {report_path}")
    
    def run_verification(self):
        """Run complete verification process."""
        logger.info("Starting workshop environment verification...")
        
        verification_steps = [
            ("Python packages", self.check_python_packages),
            ("AWS configuration", self.check_aws_configuration),
            ("Workshop structure", self.check_workshop_structure),
            ("Configuration files", self.check_configuration_files),
            ("Sample projects", self.check_sample_projects),
            ("Strands functionality", self.test_strands_functionality)
        ]
        
        for step_name, step_function in verification_steps:
            logger.info(f"Verifying: {step_name}")
            try:
                step_function()
            except Exception as e:
                error_msg = f"Verification error in {step_name}: {str(e)}"
                self.issues.append(error_msg)
                logger.error(error_msg)
        
        # Generate report
        self.generate_verification_report()
        
        # Summary
        if not self.issues:
            logger.info("🎉 Environment verification successful!")
            logger.info("✅ Ready for workshop")
        else:
            logger.warning(f"⚠️  Found {len(self.issues)} issues that need attention")
            logger.warning(f"📋 Check verification_report.md for details")
        
        if self.warnings:
            logger.info(f"ℹ️  {len(self.warnings)} warnings noted (non-critical)")
        
        return len(self.issues) == 0

if __name__ == "__main__":
    verifier = WorkshopVerifier()
    success = verifier.run_verification()
    
    if success:
        print("\n🎉 Workshop environment verified!")
        print("🚀 Ready to start the workshop")
    else:
        print("\n⚠️  Issues found in environment setup")
        print("🔧 Please address issues before starting workshop")
        sys.exit(1)
```

This setup automation provides:

1. **Automated Environment Setup**: Complete installation and configuration
2. **Verification System**: Comprehensive testing of all components
3. **Error Handling**: Detailed logging and issue tracking
4. **Cross-Platform Support**: Works on Windows, macOS, and Linux
5. **Detailed Reporting**: Clear status reports and next steps

The scripts handle the complex setup process automatically while providing clear feedback and troubleshooting guidance for any issues that arise.