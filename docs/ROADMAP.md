# FastMango Development Roadmap

## Overview

This document outlines the development phases for FastMango, an AI-first web framework that unifies FastAPI, FastMCP, and Django patterns.

## Phase 1: Core Framework Foundation (MVP)
**Timeline**: 2-3 months  
**Goal**: Basic MangoApp class with unified web/AI/MCP integration

### Milestones
- [ ] **Core Architecture**
  - MangoApp class with FastAPI integration
  - Basic LLM engine (Pydantic AI)
  - MCP server integration (FastMCP)
  - Unified configuration system

- [ ] **CLI Tools**
  - `fastmango new` project generator
  - `fastmango run` development server
  - Basic project templates
  - Alias recommendation (`fmgo`)

- [ ] **Database Integration**
  - SQLModel + SQLAlchemy async
  - Basic migrations (Alembic)
  - Django-style model patterns

### Key Deliverables
```python
# Target API for Phase 1
from fastmango import MangoApp

app = MangoApp()

@app.get("/api/users")
async def get_users():
    return await User.objects.all()

@app.llm_endpoint("/chat")
async def chat(message: str):
    return await app.llm.generate(message)

@app.mcp_tool()
def search_database(query: str):
    return User.objects.filter(name__contains=query)
```

## Phase 2: AI & MCP Enhancement
**Timeline**: 1-2 months  
**Goal**: Advanced AI/MCP features and multiple provider support

### Milestones
- [ ] **Multi-LLM Support**
  - OpenAI, Anthropic, Ollama providers
  - Provider switching and fallback
  - Context management and caching

- [ ] **Advanced MCP Features**
  - Auto-generated MCP tools from models
  - MCP client capabilities
  - Tool composition and chaining

- [ ] **Developer Experience**
  - Hot reload for MCP tools
  - AI/MCP debugging tools
  - Enhanced error handling

## Phase 3: Production Features
**Timeline**: 1-2 months  
**Goal**: Production-ready features and deployment support

### Milestones
- [ ] **Security & Auth**
  - JWT authentication
  - API key management
  - MCP tool permissions

- [ ] **Monitoring & Observability**
  - Request/response logging
  - AI usage metrics
  - Performance monitoring

- [ ] **Deployment**
  - Docker containerization
  - Cloud deployment guides
  - Environment configuration

## Phase 4: First Use Case - 국회 공공데이터 MCP
**Timeline**: 1 month  
**Goal**: Real-world validation with Korean National Assembly data

### Milestones
- [ ] **Public Data Integration**
  - 열린국회정보 API wrapper
  - 공공데이터 포털 integration
  - NABOSTATS API support

- [ ] **MCP Tools Development**
  - Assembly member search
  - Bill tracking and analysis
  - Budget data queries
  - Statistical analysis tools

- [ ] **Service Deployment**
  - Oracle Cloud deployment
  - Public MCP server hosting
  - Documentation and examples

### Target MCP Tools
```python
@app.mcp_tool()
def search_assembly_members(name: str, party: str = None):
    """국회의원 검색"""
    
@app.mcp_tool() 
def get_bill_info(bill_id: str):
    """의안 정보 조회"""
    
@app.mcp_tool()
def get_budget_data(year: int, category: str):
    """예산 데이터 조회"""
```

## Success Metrics

### Phase 1 Success Criteria
- CLI can generate functional FastMango project
- Basic web + AI + MCP integration working
- 5+ GitHub stars, initial community interest

### Phase 2 Success Criteria  
- Multiple LLM providers supported
- Advanced MCP tooling functional
- 50+ GitHub stars, developer adoption

### Phase 3 Success Criteria
- Production deployment successful
- Security and monitoring in place
- 200+ GitHub stars, enterprise interest

### Phase 4 Success Criteria
- Public 국회 데이터 MCP server running
- Real-world usage and feedback
- 500+ GitHub stars, media coverage

## Risk Mitigation

### Technical Risks
- **FastMCP API changes**: Pin versions, maintain compatibility layer
- **Pydantic AI evolution**: Monitor updates, contribute to ecosystem
- **Performance bottlenecks**: Profile early, optimize incrementally

### Market Risks
- **AI ecosystem changes**: Stay flexible, support multiple providers
- **Competition emergence**: Focus on unique value proposition
- **Developer adoption**: Community engagement, excellent documentation

## Resource Requirements

### Development Time
- **Solo development**: 5-7 months total
- **Part-time commitment**: ~20 hours/week
- **Milestone-driven approach**: Ship incrementally

### Infrastructure Needs
- **Development**: Local development environment
- **Testing**: Oracle Cloud free tier
- **Deployment**: Home network + Oracle Cloud
- **Monitoring**: Open source tools (Prometheus, Grafana)

## Next Steps

### Immediate Actions (Week 1-2)
1. Create detailed GitHub issues from this roadmap
2. Set up project structure and CI/CD
3. Begin Phase 1 core architecture implementation

### Milestone Tracking
- GitHub Projects for kanban-style tracking
- Weekly progress reviews
- Community feedback integration

---

*Updated: 2025-09-02*
*Next Review: Weekly during active development*