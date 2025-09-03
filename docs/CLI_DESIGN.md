# fastmango CLI Design

## 🎯 Design Philosophy

The fastmango CLI combines **Node.js's modern developer experience** with **Django's productivity** to provide an intuitive and efficient command-line interface.

### Core Principles
- **Simplicity**: Short and memorable commands
- **Consistency**: Predictable command patterns
- **Rich Feedback**: Visual output and real-time information
- **Interactive**: Smart prompts and auto-completion

## 🛠 Command Structure

### Basic Command Pattern
```bash
fastmango <command> [subcommand] [options] [arguments]
```

### Complete Command Overview
```bash
fastmango --help                 # Help information
fastmango --version              # Version information
fastmango init [project-name]    # Initialize project
fastmango dev                    # Run development server
fastmango build                  # Production build
fastmango start                  # Run production server
fastmango migrate               # Database migrations
fastmango shell                 # Interactive Python shell
fastmango admin                 # Launch admin interface
fastmango user <subcommand>     # User management
fastmango db <subcommand>       # Database management
fastmango ai <subcommand>       # AI tools management
fastmango deploy <platform>     # Deploy to platform
```

## 📋 Detailed Command Design

### 1. Project Initialization
```bash
fastmango init [project-name]
fastmango init myapp --template=basic
fastmango init myapp --template=fullstack
fastmango init myapp --db=postgresql --ai=enabled
```

**Features**:
- Interactive project configuration
- Template selection (basic, fullstack, ai-enabled)
- Database type selection
- AI integration toggle

**Example Output**:
```
🚀 Creating new fastmango project...

✨ Project Name: myapp
📦 Template: fullstack
🗄️  Database: PostgreSQL
🤖 AI Integration: Enabled

📁 Creating project structure...
  ├── app/
  │   ├── models/
  │   ├── api/
  │   └── core/
  ├── migrations/
  └── tests/

✅ Project created successfully!

Next steps:
  cd myapp
  fastmango dev
```

### 2. Development Server (Node.js dev script style)
```bash
fastmango dev
fastmango dev --port=8001
fastmango dev --reload=off
fastmango dev --admin=disabled
```

**Features**:
- Hot reload development server
- Real-time log streaming
- Concurrent admin UI execution
- Automatic migration checking

**Example Output**:
```
🔥 Starting fastmango dev server...

🌐 API Server: http://localhost:8000
⚙️  Admin Panel: http://localhost:8000/admin
📊 API Docs: http://localhost:8000/docs

🔄 Watching for changes...
✅ Database connected (PostgreSQL)
🤖 AI Tools loaded: 3

[14:30:21] GET /api/v1/users → 200 (45ms)
[14:30:25] POST /api/v1/auth/login → 200 (120ms)
```

### 3. Database Management
```bash
fastmango migrate                    # Run migrations
fastmango migrate --create [name]    # Create migration
fastmango migrate --rollback [rev]   # Rollback migration
fastmango migrate --status           # Migration status
fastmango dbshell                   # Database shell
```

**Example Output**:
```
🗄️  Running database migrations...

📝 Applying migrations:
  ✅ 0001_initial_user_model
  ✅ 0002_add_user_profile
  ✅ 0003_create_posts_table

🎉 All migrations applied successfully!
```

### 4. User Management
```bash
fastmango user create              # Create user
fastmango user create --admin      # Create admin user
fastmango user list               # List users
fastmango user delete <id>        # Delete user
```

### 5. AI Tools Management
```bash
fastmango ai list                 # List AI tools
fastmango ai register <tool>      # Register AI tool
fastmango ai test <tool>          # Test AI tool
fastmango ai usage               # AI usage statistics
```

### 6. Deployment Management
```bash
fastmango build                   # Production build
fastmango deploy railway         # Deploy to Railway
fastmango deploy fly             # Deploy to Fly.io
fastmango deploy --env=staging    # Deploy to staging environment
```

## 🎨 User Experience (UX) Design

### Rich Terminal Output
- **Color coding**: Status-based color differentiation
- **Icons**: Intuitive visual indicators
- **Progress bars**: Progress indication for long operations
- **Tables**: Structured data display

### Interactive Prompts
```python
# During project initialization
✨ What's your project name? myapp
🗄️  Choose database:
  > PostgreSQL
    SQLite
    MySQL

🤖 Enable AI integration? (Y/n) Y
📦 Select template:
  > Basic API
    Full-stack with Admin
    AI-powered App
```

### Error Handling and Help
```bash
❌ Error: Database connection failed

💡 Suggestions:
  • Check if PostgreSQL is running
  • Verify connection string in .env
  • Run: fastmango db status

📚 Docs: https://fastmango.dev/docs/database
```

## 🔧 Technical Implementation

### Typer-based Structure
```python
# fastmango/commands/
├── __init__.py
├── init.py          # fastmango init
├── dev.py           # fastmango dev
├── migrate.py       # fastmango migrate
├── user.py          # fastmango user
├── db.py            # fastmango db
├── ai.py            # fastmango ai
└── deploy.py        # fastmango deploy
```

### Configuration Management
```python
# fastmango.toml or .fastmango/config.yaml
[project]
name = "myapp"
version = "0.1.0"

[database]
url = "postgresql://localhost/myapp"
auto_migrate = true

[development]
host = "localhost"
port = 8000
reload = true
admin_enabled = true

[ai]
enabled = true
provider = "openai"
models = ["gpt-4o-mini"]
```

### Plugin System
```python
# Third-party plugin support
fastmango install fastmango-plugin-auth
fastmango install fastmango-plugin-monitoring
```

## 📊 Performance Goals

### Command Response Time
- `fastmango dev`: Server start in < 2 seconds
- `fastmango migrate`: Migration execution in < 1 second
- `fastmango build`: Build completion in < 10 seconds

### User Experience Metrics
- Learning curve: Django developers proficient within 1 hour
- Command discoverability: All options easily accessible via `--help`
- Error recovery: Clear error messages with actionable solutions

## 🔄 Django manage.py Command Comparison

| Django | fastmango | Improvement |
|--------|--------|-------------|
| `python manage.py runserver` | `fastmango dev` | Shorter and more intuitive |
| `python manage.py migrate` | `fastmango migrate` | No Python path required |
| `python manage.py createsuperuser` | `fastmango user create --admin` | Clearer intent |
| `python manage.py shell` | `fastmango shell` | Concise |
| `python manage.py collectstatic` | `fastmango build` | Modern build concept |

## 🚀 Future Extensions

### Auto-completion Support
```bash
# Install Bash/Zsh auto-completion
fastmango --install-completion
```

### IDE Integration
- VSCode Extension
- PyCharm Plugin
- Vim/Neovim support

### Workflow Integration
```bash
fastmango workflow init          # GitHub Actions template
fastmango workflow deploy        # Deployment pipeline
fastmango workflow test          # Test pipeline
```

## 🎭 Command Aliases and Shortcuts

### Common Aliases
```bash
# Short forms for frequently used commands
fastmango d        # alias for 'fastmango dev'
fastmango m        # alias for 'fastmango migrate'
fastmango s        # alias for 'fastmango shell'
```

### Context-aware Commands
```bash
# Smart detection of project state
fastmango          # Shows project status if in fastmango project directory
fastmango status   # Comprehensive project health check
```

## 🔍 Advanced Features

### Configuration Profiles
```bash
fastmango dev --profile=production    # Use production-like settings
fastmango deploy --profile=staging    # Deploy with staging configuration
```

### Batch Operations
```bash
fastmango migrate --all-apps          # Migrate all registered apps
fastmango test --watch               # Run tests in watch mode
```

### Debug and Inspection Tools
```bash
fastmango inspect routes             # Show all registered routes
fastmango inspect models             # Show all models and relationships
fastmango debug database            # Database connection diagnostics
```

---

*The fastmango CLI is designed to feel familiar to Django developers while embracing modern development practices.*