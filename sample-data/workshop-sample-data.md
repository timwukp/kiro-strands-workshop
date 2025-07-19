# Workshop Sample Data and Mock Services

## Sample Dataset Generation

### 1. Customer Support Dataset Generator

**File: `generate_sample_data.py`**

```python
#!/usr/bin/env python3
"""
Generate realistic sample datasets for workshop exercises.
Creates various data formats commonly used in business applications.
"""

import json
import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import faker

# Initialize Faker for realistic data generation
fake = faker.Faker()

class SampleDataGenerator:
    def __init__(self, output_dir="workshop_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_customer_support_tickets(self, count=200):
        """Generate realistic customer support tickets."""
        
        categories = [
            "Technical Issue", "Billing Question", "Feature Request",
            "Bug Report", "Account Access", "Performance Issue",
            "Integration Help", "Documentation", "Training Request"
        ]
        
        priorities = ["Low", "Medium", "High", "Critical"]
        statuses = ["Open", "In Progress", "Waiting for Customer", "Resolved", "Closed"]
        
        tickets = []
        
        for i in range(count):
            created_date = fake.date_time_between(start_date='-90d', end_date='now')
            
            # Simulate ticket progression
            if random.random() < 0.7:  # 70% of tickets have updates
                last_updated = fake.date_time_between(start_date=created_date, end_date='now')
            else:
                last_updated = created_date
            
            ticket = {
                "ticket_id": f"TICK-{i+1:05d}",
                "customer_id": f"CUST-{random.randint(1000, 9999)}",
                "customer_name": fake.name(),
                "customer_email": fake.email(),
                "subject": fake.sentence(nb_words=6),
                "category": random.choice(categories),
                "priority": random.choice(priorities),
                "status": random.choice(statuses),
                "description": fake.paragraph(nb_sentences=3),
                "created_at": created_date.isoformat(),
                "last_updated": last_updated.isoformat(),
                "assigned_agent": fake.name() if random.random() < 0.6 else None,
                "resolution_time_hours": random.randint(1, 168) if random.random() < 0.5 else None,
                "customer_satisfaction": random.randint(1, 5) if random.random() < 0.3 else None,
                "tags": random.sample(["urgent", "vip", "escalated", "technical", "billing"], 
                                   random.randint(0, 3))
            }
            tickets.append(ticket)
        
        # Save as JSON
        with open(self.output_dir / "customer_support_tickets.json", "w") as f:
            json.dump(tickets, f, indent=2, default=str)
        
        # Save as CSV
        with open(self.output_dir / "customer_support_tickets.csv", "w", newline="") as f:
            if tickets:
                writer = csv.DictWriter(f, fieldnames=tickets[0].keys())
                writer.writeheader()
                for ticket in tickets:
                    # Convert lists to strings for CSV
                    ticket_copy = ticket.copy()
                    ticket_copy['tags'] = ','.join(ticket_copy['tags'])
                    writer.writerow(ticket_copy)
        
        print(f"Generated {count} customer support tickets")
        return tickets
    
    def generate_product_catalog(self, count=100):
        """Generate product catalog data."""
        
        categories = [
            "Electronics", "Books", "Clothing", "Home & Garden", 
            "Sports & Outdoors", "Health & Beauty", "Automotive", "Toys & Games"
        ]
        
        brands = [
            "TechCorp", "InnovateCo", "QualityBrand", "PremiumLine",
            "EcoFriendly", "SmartTech", "ClassicStyle", "ModernDesign"
        ]
        
        products = []
        
        for i in range(count):
            category = random.choice(categories)
            
            product = {
                "product_id": f"PROD-{i+1:05d}",
                "sku": f"SKU{random.randint(100000, 999999)}",
                "name": fake.catch_phrase(),
                "description": fake.paragraph(nb_sentences=2),
                "category": category,
                "brand": random.choice(brands),
                "price": round(random.uniform(9.99, 999.99), 2),
                "cost": round(random.uniform(5.00, 500.00), 2),
                "stock_quantity": random.randint(0, 1000),
                "weight_kg": round(random.uniform(0.1, 50.0), 2),
                "dimensions": {
                    "length": round(random.uniform(5, 100), 1),
                    "width": round(random.uniform(5, 100), 1),
                    "height": round(random.uniform(5, 100), 1)
                },
                "rating": round(random.uniform(1.0, 5.0), 1),
                "review_count": random.randint(0, 500),
                "is_active": random.choice([True, False]),
                "created_at": fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
                "tags": random.sample(["bestseller", "new", "sale", "premium", "eco-friendly"], 
                                   random.randint(0, 3))
            }
            products.append(product)
        
        # Save as JSON
        with open(self.output_dir / "product_catalog.json", "w") as f:
            json.dump(products, f, indent=2, default=str)
        
        print(f"Generated {count} products")
        return products
    
    def generate_user_interactions(self, count=1000):
        """Generate user interaction logs."""
        
        actions = [
            "login", "logout", "view_product", "add_to_cart", "remove_from_cart",
            "checkout", "search", "filter", "sort", "review", "contact_support"
        ]
        
        devices = ["desktop", "mobile", "tablet"]
        browsers = ["Chrome", "Firefox", "Safari", "Edge"]
        
        interactions = []
        
        for i in range(count):
            interaction = {
                "interaction_id": str(uuid.uuid4()),
                "user_id": f"USER-{random.randint(1000, 9999)}",
                "session_id": str(uuid.uuid4()),
                "action": random.choice(actions),
                "timestamp": fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
                "device_type": random.choice(devices),
                "browser": random.choice(browsers),
                "ip_address": fake.ipv4(),
                "page_url": fake.url(),
                "referrer": fake.url() if random.random() < 0.7 else None,
                "duration_seconds": random.randint(1, 3600),
                "product_id": f"PROD-{random.randint(1, 100):05d}" if random.random() < 0.4 else None,
                "search_query": fake.sentence(nb_words=3) if random.random() < 0.2 else None,
                "user_agent": fake.user_agent()
            }
            interactions.append(interaction)
        
        # Save as JSON
        with open(self.output_dir / "user_interactions.json", "w") as f:
            json.dump(interactions, f, indent=2, default=str)
        
        print(f"Generated {count} user interactions")
        return interactions
    
    def generate_sales_data(self, count=500):
        """Generate sales transaction data."""
        
        payment_methods = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash"]
        order_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled", "Returned"]
        
        sales = []
        
        for i in range(count):
            order_date = fake.date_time_between(start_date='-1y', end_date='now')
            
            # Generate 1-5 items per order
            items = []
            total_amount = 0
            
            for _ in range(random.randint(1, 5)):
                item_price = round(random.uniform(10, 200), 2)
                quantity = random.randint(1, 3)
                item_total = item_price * quantity
                total_amount += item_total
                
                items.append({
                    "product_id": f"PROD-{random.randint(1, 100):05d}",
                    "quantity": quantity,
                    "unit_price": item_price,
                    "total_price": item_total
                })
            
            sale = {
                "order_id": f"ORD-{i+1:06d}",
                "customer_id": f"CUST-{random.randint(1000, 9999)}",
                "order_date": order_date.isoformat(),
                "status": random.choice(order_statuses),
                "payment_method": random.choice(payment_methods),
                "subtotal": round(total_amount, 2),
                "tax_amount": round(total_amount * 0.08, 2),
                "shipping_cost": round(random.uniform(0, 25), 2),
                "total_amount": round(total_amount * 1.08 + random.uniform(0, 25), 2),
                "items": items,
                "shipping_address": {
                    "street": fake.street_address(),
                    "city": fake.city(),
                    "state": fake.state(),
                    "zip_code": fake.zipcode(),
                    "country": fake.country()
                },
                "notes": fake.sentence() if random.random() < 0.3 else None
            }
            sales.append(sale)
        
        # Save as JSON
        with open(self.output_dir / "sales_data.json", "w") as f:
            json.dump(sales, f, indent=2, default=str)
        
        print(f"Generated {count} sales records")
        return sales
    
    def generate_employee_data(self, count=50):
        """Generate employee/user data for HR scenarios."""
        
        departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations", "Support"]
        positions = ["Manager", "Senior", "Junior", "Lead", "Specialist", "Coordinator", "Director"]
        
        employees = []
        
        for i in range(count):
            hire_date = fake.date_between(start_date='-5y', end_date='now')
            
            employee = {
                "employee_id": f"EMP-{i+1:04d}",
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "department": random.choice(departments),
                "position": f"{random.choice(positions)} {fake.job()}",
                "hire_date": hire_date.isoformat(),
                "salary": random.randint(40000, 150000),
                "manager_id": f"EMP-{random.randint(1, max(1, i)):04d}" if i > 0 and random.random() < 0.8 else None,
                "office_location": fake.city(),
                "is_active": random.choice([True, False]) if random.random() < 0.1 else True,
                "skills": random.sample([
                    "Python", "JavaScript", "SQL", "Project Management", "Data Analysis",
                    "Marketing", "Sales", "Customer Service", "Leadership", "Communication"
                ], random.randint(2, 6)),
                "performance_rating": round(random.uniform(2.0, 5.0), 1),
                "last_review_date": fake.date_between(start_date=hire_date, end_date='now').isoformat()
            }
            employees.append(employee)
        
        # Save as JSON
        with open(self.output_dir / "employee_data.json", "w") as f:
            json.dump(employees, f, indent=2, default=str)
        
        print(f"Generated {count} employee records")
        return employees
    
    def generate_all_datasets(self):
        """Generate all sample datasets."""
        print("Generating sample datasets for workshop...")
        
        self.generate_customer_support_tickets(200)
        self.generate_product_catalog(100)
        self.generate_user_interactions(1000)
        self.generate_sales_data(500)
        self.generate_employee_data(50)
        
        # Create a summary file
        summary = {
            "generated_at": datetime.now().isoformat(),
            "datasets": {
                "customer_support_tickets": {"count": 200, "formats": ["json", "csv"]},
                "product_catalog": {"count": 100, "formats": ["json"]},
                "user_interactions": {"count": 1000, "formats": ["json"]},
                "sales_data": {"count": 500, "formats": ["json"]},
                "employee_data": {"count": 50, "formats": ["json"]}
            },
            "usage_notes": [
                "These datasets are for workshop exercises only",
                "Data is randomly generated and not based on real information",
                "Use these datasets for testing agent functionality",
                "Modify as needed for specific exercises"
            ]
        }
        
        with open(self.output_dir / "dataset_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ All datasets generated in '{self.output_dir}' directory")
        print("📊 Dataset summary saved to 'dataset_summary.json'")

if __name__ == "__main__":
    generator = SampleDataGenerator()
    generator.generate_all_datasets()
```

### 2. Mock API Server for Workshop

**File: `mock_api_server.py`**

```python
#!/usr/bin/env python3
"""
Mock API server for workshop exercises.
Provides realistic API endpoints for agent integration testing.
"""

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import json
import random
import time
from datetime import datetime, timedelta
import uuid
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load sample data
data_dir = Path("workshop_data")
sample_data = {}

def load_sample_data():
    """Load sample datasets into memory."""
    global sample_data
    
    try:
        with open(data_dir / "customer_support_tickets.json") as f:
            sample_data['tickets'] = json.load(f)
        
        with open(data_dir / "product_catalog.json") as f:
            sample_data['products'] = json.load(f)
        
        with open(data_dir / "user_interactions.json") as f:
            sample_data['interactions'] = json.load(f)
        
        with open(data_dir / "sales_data.json") as f:
            sample_data['sales'] = json.load(f)
        
        with open(data_dir / "employee_data.json") as f:
            sample_data['employees'] = json.load(f)
        
        print("✅ Sample data loaded successfully")
    except FileNotFoundError as e:
        print(f"⚠️  Sample data file not found: {e}")
        print("Run generate_sample_data.py first to create sample datasets")

# API Routes

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/weather/<city>')
def get_weather(city):
    """Mock weather API endpoint."""
    # Simulate API delay
    time.sleep(random.uniform(0.1, 0.5))
    
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "foggy", "windy"]
    
    return jsonify({
        "city": city,
        "temperature": random.randint(-10, 35),
        "humidity": random.randint(30, 90),
        "pressure": random.randint(980, 1030),
        "wind_speed": random.randint(0, 25),
        "condition": random.choice(weather_conditions),
        "timestamp": datetime.now().isoformat(),
        "forecast": [
            {
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "temperature": random.randint(-5, 30),
                "condition": random.choice(weather_conditions)
            } for i in range(1, 6)
        ]
    })

@app.route('/api/tickets', methods=['GET', 'POST'])
def handle_tickets():
    """Customer support tickets API."""
    if request.method == 'GET':
        # Query parameters
        status = request.args.get('status')
        priority = request.args.get('priority')
        limit = int(request.args.get('limit', 50))
        
        tickets = sample_data.get('tickets', [])
        
        # Filter by status
        if status:
            tickets = [t for t in tickets if t['status'].lower() == status.lower()]
        
        # Filter by priority
        if priority:
            tickets = [t for t in tickets if t['priority'].lower() == priority.lower()]
        
        # Limit results
        tickets = tickets[:limit]
        
        return jsonify({
            "tickets": tickets,
            "total": len(tickets),
            "filters": {"status": status, "priority": priority}
        })
    
    elif request.method == 'POST':
        # Create new ticket
        ticket_data = request.json
        
        new_ticket = {
            "ticket_id": f"TICK-{random.randint(10000, 99999)}",
            "customer_id": ticket_data.get('customer_id', f"CUST-{random.randint(1000, 9999)}"),
            "subject": ticket_data.get('subject', 'New Support Request'),
            "description": ticket_data.get('description', ''),
            "priority": ticket_data.get('priority', 'Medium'),
            "status": "Open",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        return jsonify({
            "message": "Ticket created successfully",
            "ticket": new_ticket
        }), 201

@app.route('/api/products', methods=['GET'])
def get_products():
    """Product catalog API."""
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    limit = int(request.args.get('limit', 20))
    
    products = sample_data.get('products', [])
    
    # Filter by category
    if category:
        products = [p for p in products if p['category'].lower() == category.lower()]
    
    # Filter by price range
    if min_price is not None:
        products = [p for p in products if p['price'] >= min_price]
    
    if max_price is not None:
        products = [p for p in products if p['price'] <= max_price]
    
    # Limit results
    products = products[:limit]
    
    return jsonify({
        "products": products,
        "total": len(products),
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price
        }
    })

@app.route('/api/analytics/summary')
def get_analytics_summary():
    """Analytics summary endpoint."""
    # Simulate processing time
    time.sleep(random.uniform(0.5, 1.0))
    
    return jsonify({
        "period": "last_30_days",
        "metrics": {
            "total_sales": random.randint(50000, 200000),
            "total_orders": random.randint(500, 2000),
            "average_order_value": round(random.uniform(50, 150), 2),
            "customer_satisfaction": round(random.uniform(4.0, 5.0), 1),
            "support_tickets": random.randint(100, 500),
            "resolution_time_hours": round(random.uniform(2, 48), 1)
        },
        "trends": {
            "sales_growth": f"{random.randint(-10, 25)}%",
            "customer_growth": f"{random.randint(0, 15)}%",
            "satisfaction_change": f"{random.randint(-5, 10)}%"
        },
        "generated_at": datetime.now().isoformat()
    })

@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    """User management API."""
    if request.method == 'GET':
        # Return sample users
        users = [
            {
                "id": i,
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "role": random.choice(["admin", "user", "manager"]),
                "active": random.choice([True, False]),
                "last_login": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
            } for i in range(1, 21)
        ]
        
        return jsonify({"users": users})
    
    elif request.method == 'POST':
        # Create new user
        user_data = request.json
        
        new_user = {
            "id": random.randint(100, 999),
            "name": user_data.get('name', 'New User'),
            "email": user_data.get('email', 'newuser@example.com'),
            "role": user_data.get('role', 'user'),
            "active": True,
            "created_at": datetime.now().isoformat()
        }
        
        return jsonify({
            "message": "User created successfully",
            "user": new_user
        }), 201

@app.route('/api/search')
def search_api():
    """Generic search API."""
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    limit = int(request.args.get('limit', 10))
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    # Mock search results
    results = []
    for i in range(min(limit, random.randint(3, 15))):
        results.append({
            "id": str(uuid.uuid4()),
            "title": f"Search result {i+1} for '{query}'",
            "description": f"This is a mock search result related to {query}",
            "category": category,
            "relevance_score": round(random.uniform(0.5, 1.0), 2),
            "url": f"https://example.com/result/{i+1}"
        })
    
    return jsonify({
        "query": query,
        "category": category,
        "results": results,
        "total_results": len(results),
        "search_time_ms": random.randint(10, 100)
    })

@app.route('/api/slow-endpoint')
def slow_endpoint():
    """Endpoint that simulates slow response for testing timeouts."""
    delay = int(request.args.get('delay', 5))
    time.sleep(delay)
    
    return jsonify({
        "message": f"Response after {delay} seconds",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/error-test')
def error_test():
    """Endpoint for testing error handling."""
    error_type = request.args.get('type', 'server_error')
    
    if error_type == 'not_found':
        abort(404)
    elif error_type == 'unauthorized':
        abort(401)
    elif error_type == 'bad_request':
        abort(400)
    elif error_type == 'rate_limit':
        abort(429)
    else:
        abort(500)

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Mock authentication endpoint."""
    credentials = request.json
    
    if not credentials or 'username' not in credentials or 'password' not in credentials:
        return jsonify({"error": "Username and password required"}), 400
    
    # Mock authentication (accept any credentials for demo)
    token = str(uuid.uuid4())
    
    return jsonify({
        "message": "Login successful",
        "token": token,
        "expires_in": 3600,
        "user": {
            "username": credentials['username'],
            "role": "user",
            "permissions": ["read", "write"]
        }
    })

@app.route('/api/protected')
def protected_endpoint():
    """Protected endpoint requiring authentication."""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authentication required"}), 401
    
    return jsonify({
        "message": "Access granted to protected resource",
        "data": {"secret": "This is protected data"},
        "timestamp": datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting Mock API Server for Workshop")
    print("📊 Loading sample data...")
    
    load_sample_data()
    
    print("\n📡 Available API endpoints:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/weather/<city> - Weather data")
    print("  GET  /api/tickets - Support tickets")
    print("  POST /api/tickets - Create ticket")
    print("  GET  /api/products - Product catalog")
    print("  GET  /api/analytics/summary - Analytics data")
    print("  GET  /api/users - User list")
    print("  POST /api/users - Create user")
    print("  GET  /api/search - Search API")
    print("  GET  /api/slow-endpoint - Slow response test")
    print("  GET  /api/error-test - Error handling test")
    print("  POST /api/auth/login - Authentication")
    print("  GET  /api/protected - Protected resource")
    
    print("\n🌐 Server starting on http://localhost:5000")
    print("📖 Use these endpoints in your workshop exercises")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
```

This provides comprehensive sample data and mock services for realistic workshop exercises, including:

1. **Realistic Sample Data**: Customer support tickets, product catalogs, user interactions, sales data, and employee records
2. **Mock API Server**: RESTful endpoints for testing HTTP integration
3. **Various Data Formats**: JSON and CSV outputs for different use cases
4. **Error Simulation**: Endpoints for testing error handling and timeouts
5. **Authentication Testing**: Mock login and protected endpoints

The data generation creates realistic, varied datasets that participants can use throughout the workshop exercises.