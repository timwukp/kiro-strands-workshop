# Security Guidelines for Kiro IDE + Strands SDK Workshop

## Overview

This document provides essential security best practices for participants in the Kiro IDE + Strands SDK workshop. Following these guidelines will help you build secure AI agent applications and avoid common security pitfalls.

## Table of Contents

1. [Secure Subprocess Execution](#secure-subprocess-execution)
2. [File Operations Security](#file-operations-security)
3. [Handling Credentials](#handling-credentials)
4. [Input Validation](#input-validation)
5. [Error Handling](#error-handling)
6. [Network Security](#network-security)
7. [AWS Security Best Practices](#aws-security-best-practices)
8. [Security Checklist](#security-checklist)

## Secure Subprocess Execution

When executing system commands from Python, follow these security practices:

### ❌ Insecure Practices

```python
# NEVER use shell=True with user-provided input
user_input = input("Enter filename: ")
subprocess.run(f"cat {user_input}", shell=True)  # VULNERABLE to command injection

# NEVER use string formatting with subprocess
filename = "user_data.txt"
subprocess.run(f"cat {filename}", shell=True)  # VULNERABLE to command injection
```

### ✅ Secure Practices

```python
# Use a list of arguments instead of a string
user_input = input("Enter filename: ")
subprocess.run(["cat", user_input], check=False)  # Safer

# Avoid shell=True whenever possible
subprocess.run(["ls", "-la"], check=False)  # Safer than shell=True

# If you must use shell commands, validate inputs strictly
import re
user_input = input("Enter filename: ")
if re.match(r'^[a-zA-Z0-9_\-\.]+$', user_input):  # Strict validation
    subprocess.run(["cat", user_input], check=False)
else:
    print("Invalid filename")
```

## File Operations Security

When working with files, follow these security practices:

### ❌ Insecure Practices

```python
# NEVER use user input directly in file paths
user_input = input("Enter filename: ")
with open(f"/data/{user_input}", "r") as f:  # VULNERABLE to path traversal
    data = f.read()

# NEVER use relative paths without validation
with open("../../../etc/passwd", "r") as f:  # VULNERABLE to path traversal
    data = f.read()
```

### ✅ Secure Practices

```python
# Validate and sanitize file paths
import os
import re

user_input = input("Enter filename: ")
if not re.match(r'^[a-zA-Z0-9_\-\.]+$', user_input):
    print("Invalid filename")
else:
    # Use os.path.join for path construction
    safe_path = os.path.join("data", user_input)
    
    # Use os.path.abspath to resolve the path and check if it's within allowed directory
    abs_path = os.path.abspath(safe_path)
    allowed_dir = os.path.abspath("data")
    
    if abs_path.startswith(allowed_dir):
        with open(abs_path, "r") as f:
            data = f.read()
    else:
        print("Access denied: path outside allowed directory")
```

## Handling Credentials

Proper credential management is crucial for security:

### ❌ Insecure Practices

```python
# NEVER hardcode credentials in source code
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# NEVER store credentials in unencrypted files
with open("credentials.txt", "w") as f:
    f.write(f"username=admin\npassword=secret123")
```

### ✅ Secure Practices

```python
# Use environment variables for credentials
import os

aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Use AWS CLI credential management
# $ aws configure
# AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name [None]: us-west-2
# Default output format [None]: json

# Use a credentials manager or secrets manager service
import boto3
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "my-app/db-credentials"
    region_name = "us-west-2"
    
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        # Handle exceptions properly
        print(f"Error retrieving secret: {e}")
        return None
```

## Input Validation

Always validate user input to prevent security vulnerabilities:

### ❌ Insecure Practices

```python
# NEVER trust user input without validation
user_input = input("Enter SQL query: ")
cursor.execute(user_input)  # VULNERABLE to SQL injection

# NEVER use eval() with user input
user_input = input("Enter expression: ")
result = eval(user_input)  # VULNERABLE to code execution
```

### ✅ Secure Practices

```python
# Use parameterized queries for SQL
user_input = input("Enter user ID: ")
cursor.execute("SELECT * FROM users WHERE id = %s", (user_input,))

# Validate input against strict patterns
import re
user_input = input("Enter username: ")
if re.match(r'^[a-zA-Z0-9_]{3,16}$', user_input):
    # Process valid username
    pass
else:
    print("Invalid username format")

# Use safe alternatives to eval()
from ast import literal_eval
user_input = input("Enter a list or dictionary: ")
try:
    # Only evaluates literals like [], {}, etc.
    result = literal_eval(user_input)
except (ValueError, SyntaxError):
    print("Invalid input")
```

## Error Handling

Proper error handling prevents information leakage and improves security:

### ❌ Insecure Practices

```python
# NEVER expose detailed error messages to users
try:
    # Some operation
    result = 10 / 0
except Exception as e:
    print(f"Error details: {str(e)}")  # VULNERABLE to information leakage
    print(f"Stack trace: {traceback.format_exc()}")  # VULNERABLE to information leakage
```

### ✅ Secure Practices

```python
# Log detailed errors but show generic messages to users
import logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

try:
    # Some operation
    result = 10 / 0
except Exception as e:
    # Log detailed error for developers
    logging.error(f"Division error: {str(e)}", exc_info=True)
    
    # Show generic message to users
    print("An error occurred. Please try again later.")

# Use custom exception handling for different error types
try:
    # Some operation
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    # Process file...
except FileNotFoundError as e:
    logging.error(str(e))
    print("The requested file could not be found.")
except PermissionError:
    logging.error(f"Permission denied for file: {filename}")
    print("You don't have permission to access this file.")
except Exception as e:
    logging.error(f"Unexpected error: {str(e)}", exc_info=True)
    print("An unexpected error occurred.")
```

## Network Security

Secure your network communications:

### ❌ Insecure Practices

```python
# NEVER use unencrypted connections for sensitive data
import http.client
conn = http.client.HTTPConnection("example.com")  # VULNERABLE: unencrypted

# NEVER disable SSL verification
import requests
response = requests.get("https://example.com", verify=False)  # VULNERABLE: SSL verification disabled
```

### ✅ Secure Practices

```python
# Always use HTTPS for network communications
import http.client
conn = http.client.HTTPSConnection("example.com")  # Encrypted connection

# Always verify SSL certificates
import requests
response = requests.get("https://example.com", verify=True)  # SSL verification enabled

# Use proper timeout settings
response = requests.get("https://example.com", timeout=10)  # 10 second timeout

# Validate server certificates
import ssl
import socket

context = ssl.create_default_context()
context.check_hostname = True
context.verify_mode = ssl.CERT_REQUIRED

with socket.create_connection(("example.com", 443)) as sock:
    with context.wrap_socket(sock, server_hostname="example.com") as ssock:
        print(f"Connected to {ssock.version()}")
```

## AWS Security Best Practices

When working with AWS services:

### ❌ Insecure Practices

```python
# NEVER use overly permissive IAM policies
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": "*",
#       "Resource": "*"
#     }
#   ]
# }

# NEVER make S3 buckets public by default
s3_client.create_bucket(
    Bucket="my-bucket",
    ACL="public-read"  # VULNERABLE: public access
)
```

### ✅ Secure Practices

```python
# Use the principle of least privilege for IAM policies
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": [
#         "s3:GetObject",
#         "s3:PutObject"
#       ],
#       "Resource": "arn:aws:s3:::my-bucket/*"
#     }
#   ]
# }

# Secure S3 bucket configuration
s3_client.create_bucket(Bucket="my-bucket")  # Private by default

# Enable S3 bucket encryption
s3_client.put_bucket_encryption(
    Bucket="my-bucket",
    ServerSideEncryptionConfiguration={
        'Rules': [
            {
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'AES256'
                }
            }
        ]
    }
)

# Use AWS Secrets Manager for credentials
import boto3
from botocore.exceptions import ClientError

def get_database_credentials():
    secret_name = "prod/db/credentials"
    region_name = "us-west-2"
    
    client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        # Handle exceptions properly
        logging.error(f"Error retrieving secret: {e}")
        raise
```

## Security Checklist

Use this checklist to evaluate the security of your AI agent applications:

### Subprocess and Command Execution
- [ ] Avoid `shell=True` in subprocess calls
- [ ] Use lists of arguments instead of strings
- [ ] Validate all user inputs before using in commands
- [ ] Use the principle of least privilege for executed commands

### File Operations
- [ ] Validate and sanitize all file paths
- [ ] Use absolute paths with proper validation
- [ ] Restrict file operations to specific directories
- [ ] Set proper file permissions

### Credential Management
- [ ] Use environment variables or secrets managers for credentials
- [ ] Never hardcode credentials in source code
- [ ] Rotate credentials regularly
- [ ] Use the principle of least privilege for credentials

### Input Validation
- [ ] Validate all user inputs
- [ ] Use parameterized queries for databases
- [ ] Avoid dangerous functions like `eval()` and `exec()`
- [ ] Implement proper input sanitization

### Error Handling
- [ ] Log detailed errors for developers
- [ ] Show generic error messages to users
- [ ] Handle different error types appropriately
- [ ] Avoid exposing sensitive information in error messages

### Network Security
- [ ] Use HTTPS for all network communications
- [ ] Verify SSL certificates
- [ ] Implement proper timeout settings
- [ ] Validate server certificates

### AWS Security
- [ ] Use the principle of least privilege for IAM policies
- [ ] Secure S3 bucket configurations
- [ ] Enable encryption for data at rest and in transit
- [ ] Use AWS Secrets Manager for credentials

## Additional Resources

- [OWASP Python Security Project](https://owasp.org/www-project-python-security/)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [Python Security Documentation](https://docs.python.org/3/library/security.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

Remember: Security is a continuous process, not a one-time task. Regularly review and update your security practices as new vulnerabilities and best practices emerge.