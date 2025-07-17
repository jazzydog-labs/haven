# Next Phase Plan: Web Diff Viewer with Per-Commit Review

*Created: 2025-07-17*

## Overview

This phase focuses on building a comprehensive web-based diff viewer with per-commit review functionality, including graphs and dashboards for repository insights.

## Phase Goals

1. **Per-Commit Review System**: Allow users to mark commits as reviewed, add comments, and track review status
2. **Enhanced Diff Viewer**: Rich web interface for viewing diffs with syntax highlighting and navigation
3. **Repository Dashboards**: Visual insights with graphs showing commit activity, review progress, and repository health
4. **Commit Management Interface**: Browse commits, filter by status, search, and manage review workflows

## Implementation Plan

### Phase 1: Enhanced Commit Review Infrastructure (Priority 1)

**1.1 Extend Commit Domain Model**
- Add review comments entity linked to commits
- Add review workflow states (draft, pending, approved, needs_revision)
- Add reviewer assignment functionality
- Add review timestamps and metadata

**1.2 Commit Review API Endpoints**
- REST endpoints for commit review CRUD operations
- GraphQL mutations for review actions
- Bulk review operations (mark multiple commits as reviewed)
- Review status filtering and search

**1.3 Database Enhancements**
- Migration for commit review comments table
- Indexes for efficient review queries
- Commit review status tracking

### Phase 2: Web Diff Viewer Interface (Priority 1)

**2.1 Commit List Component**
- Paginated list of commits with review status indicators
- Filter by review status, date range, author
- Search commits by message or hash
- Bulk selection for review operations

**2.2 Diff Viewer Component**
- Syntax-highlighted diff display using Monaco Editor or similar
- Side-by-side and unified diff views
- File tree navigation within commits
- Line-by-line commenting functionality

**2.3 Review Interface**
- Review status controls (approve, request changes, etc.)
- Comment threads on specific lines/files
- Review summary and approval workflow
- Keyboard shortcuts for efficient review

### Phase 3: Dashboards and Analytics (Priority 2)

**3.1 Commit Activity Dashboard**
- Commit frequency charts (daily/weekly/monthly)
- Author contribution graphs
- File change heatmaps
- Code churn analysis

**3.2 Review Progress Dashboard**
- Review completion metrics
- Average review time statistics
- Reviewer workload distribution
- Pending review alerts

**3.3 Repository Health Dashboard**
- Code quality trends
- Test coverage over time
- Documentation coverage
- Technical debt metrics

### Phase 4: Advanced Features (Priority 3)

**4.1 Review Workflows**
- Required reviewer assignments
- Review approval requirements
- Automated review reminders
- Integration with Git hooks

**4.2 Advanced Analytics**
- Diff complexity scoring
- Risk assessment for changes
- Change impact analysis
- Refactoring detection

## Technical Architecture

### Frontend Components Structure
```
apps/web/src/
├── components/
│   ├── commits/
│   │   ├── CommitList.tsx
│   │   ├── CommitCard.tsx
│   │   ├── CommitFilters.tsx
│   │   └── CommitSearch.tsx
│   ├── diff/
│   │   ├── DiffViewer.tsx
│   │   ├── DiffNavigation.tsx
│   │   ├── SyntaxHighlight.tsx
│   │   └── LineComments.tsx
│   ├── review/
│   │   ├── ReviewPanel.tsx
│   │   ├── ReviewComments.tsx
│   │   ├── ReviewActions.tsx
│   │   └── ReviewStatus.tsx
│   └── dashboard/
│       ├── CommitChart.tsx
│       ├── ReviewMetrics.tsx
│       ├── ActivityHeatmap.tsx
│       └── HealthIndicators.tsx
├── pages/
│   ├── Commits.tsx
│   ├── CommitDetail.tsx
│   ├── Dashboard.tsx
│   └── Reviews.tsx
└── hooks/
    ├── useCommits.ts
    ├── useReviews.ts
    └── useDashboard.ts
```

### Backend API Extensions
```
apps/api/src/haven/
├── domain/entities/
│   ├── review_comment.py
│   └── review_workflow.py
├── application/services/
│   ├── review_service.py
│   └── analytics_service.py
├── interface/
│   ├── api/routes/
│   │   ├── review_routes.py
│   │   └── analytics_routes.py
│   └── graphql/
│       ├── review_schema.py
│       └── analytics_schema.py
└── infrastructure/
    └── repositories/
        ├── review_repository.py
        └── analytics_repository.py
```

## Libraries and Tools

### Frontend
- **Diff Display**: Monaco Editor or react-diff-viewer-continued
- **Charts**: Chart.js with react-chartjs-2 or Recharts
- **Syntax Highlighting**: Prism.js or highlight.js
- **Date Handling**: date-fns for time-based filtering
- **State Management**: Continue with React hooks + context

### Backend
- **Code Analysis**: pygit2 for advanced Git operations
- **Metrics**: SQLAlchemy aggregate queries for analytics
- **Caching**: Redis for dashboard data caching
- **Background Jobs**: Celery for heavy analytics computation

## Database Schema Changes

### New Tables
```sql
-- Review comments for commits
CREATE TABLE commit_review_comments (
    id SERIAL PRIMARY KEY,
    commit_id INTEGER REFERENCES commits(id),
    reviewer_id INTEGER REFERENCES users(id),
    line_number INTEGER,
    file_path VARCHAR(500),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Review workflow tracking
CREATE TABLE commit_reviews (
    id SERIAL PRIMARY KEY,
    commit_id INTEGER REFERENCES commits(id),
    reviewer_id INTEGER REFERENCES users(id),
    status VARCHAR(20) NOT NULL, -- draft, pending, approved, needs_revision
    reviewed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(commit_id, reviewer_id)
);

-- Repository analytics cache
CREATE TABLE repository_analytics (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id),
    metric_name VARCHAR(100) NOT NULL,
    metric_value JSONB NOT NULL,
    calculated_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(repository_id, metric_name)
);
```

## Development Approach

### Implementation Strategy
1. **Start with Backend**: Extend domain models and APIs first
2. **Build Core UI**: Implement basic commit list and diff viewer
3. **Add Review Features**: Layer on review functionality
4. **Create Dashboards**: Build analytics and visualizations
5. **Polish & Optimize**: Performance tuning and UX improvements

### Testing Strategy
- Unit tests for all new domain entities and services
- Integration tests for review workflows
- Component tests for diff viewer functionality
- E2E tests for complete review processes

### Quality Gates
- Maintain 70%+ test coverage
- All TypeScript types properly defined
- API documentation updated
- Performance: Diff viewer loads in <2s for typical commits

## Success Metrics

### Functional Goals
- [ ] Users can browse and filter commits by review status
- [ ] Diff viewer displays syntax-highlighted diffs with navigation
- [ ] Review comments can be added to specific lines/files
- [ ] Commits can be marked as reviewed with status tracking
- [ ] Dashboard shows commit activity and review progress graphs
- [ ] All review data persists and syncs across sessions

### Technical Goals
- [ ] Diff viewer handles commits with 100+ changed files
- [ ] Dashboard loads in <3s with 1000+ commits
- [ ] Review operations complete in <500ms
- [ ] Mobile-responsive design for basic review operations

## Next Steps

1. **Immediate**: Start with Phase 1.1 - Extend Commit Domain Model
2. **Week 1**: Complete backend review infrastructure
3. **Week 2**: Build core diff viewer interface
4. **Week 3**: Add review functionality
5. **Week 4**: Create dashboards and analytics

This plan provides a solid foundation for per-commit review functionality while building toward comprehensive repository management and analytics capabilities.