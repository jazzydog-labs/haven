# Domain Glossary - TTR (Task, Todo, Review) System

## Overview

The TTR system is a commit tracking and review system that allows users to monitor repositories, track commits, and manage code review processes.

## Core Domain Entities

### User
Represents a person who can review commits and make comments.

**Properties:**
- `id`: Unique identifier
- `username`: User's login identifier (e.g., "plva")
- `email`: User's email address
- `display_name`: Full name for display
- `avatar_url`: Profile picture URL (optional)
- `created_at`: When user was created
- `updated_at`: When user was last updated

**Relationships:**
- Has many `Comments`
- Has many `CommitReviews` (through review_assignments)

### Repository
Represents a Git repository being tracked by the system.

**Properties:**
- `id`: Unique identifier
- `name`: Repository name (e.g., "haven")
- `full_name`: Full repository path (e.g., "jazzydog-labs/haven")
- `url`: Repository URL (GitHub URL or local path)
- `branch`: Branch being tracked (e.g., "main")
- `description`: Repository description
- `is_local`: Whether this is a local repository or remote
- `created_at`: When repository was added to system
- `updated_at`: When repository was last updated

**Relationships:**
- Has many `Commits`
- Has many `Users` (through repository access)

### Commit
Represents a Git commit within a tracked repository.

**Properties:**
- `id`: Unique identifier
- `repository_id`: Foreign key to Repository
- `commit_hash`: Git commit SHA
- `message`: Commit message
- `author_name`: Commit author name
- `author_email`: Commit author email
- `committer_name`: Committer name (may differ from author)
- `committer_email`: Committer email
- `committed_at`: When commit was made
- `diff_stats`: Summary of changes (files changed, insertions, deletions)
- `created_at`: When commit was added to system
- `updated_at`: When commit was last updated

**Relationships:**
- Belongs to one `Repository`
- Has one `CommitReview`
- Has many `Comments`

### CommitReview
Represents the review status and metadata for a specific commit.

**Properties:**
- `id`: Unique identifier
- `commit_id`: Foreign key to Commit
- `reviewer_id`: Foreign key to User (who reviewed it)
- `status`: Review status (enum)
- `reviewed_at`: When review was completed (null if pending)
- `created_at`: When review was created
- `updated_at`: When review was last updated

**Status Enum Values:**
- `PENDING_REVIEW`: Commit is awaiting review
- `APPROVED`: Commit has been reviewed and approved
- `NEEDS_REVISION`: Commit needs changes before approval
- `DRAFT`: Commit is still in draft state

**Relationships:**
- Belongs to one `Commit`
- Belongs to one `User` (reviewer)
- Has many `Comments`

### Comment
Represents a comment made on a commit during review.

**Properties:**
- `id`: Unique identifier
- `commit_id`: Foreign key to Commit
- `user_id`: Foreign key to User (who made the comment)
- `content`: Comment text/content
- `line_number`: Specific line in diff (optional)
- `file_path`: File path for line-specific comments (optional)
- `created_at`: When comment was created
- `updated_at`: When comment was last updated

**Relationships:**
- Belongs to one `Commit`
- Belongs to one `User`
- May belong to one `CommitReview`

## Domain Services

### CommitTrackingService
Handles synchronization between Git repository and the TTR system.

**Responsibilities:**
- Fetch new commits from repository
- Update commit metadata
- Detect branch changes
- Handle repository state synchronization

### ReviewService
Manages the review process for commits.

**Responsibilities:**
- Create review assignments
- Update review status
- Validate review transitions
- Generate review reports

### CommentService
Handles comment operations and notifications.

**Responsibilities:**
- Create and update comments
- Validate comment content
- Link comments to specific code lines
- Generate comment notifications

## Use Cases

### Primary Use Cases

1. **Track Repository**
   - Add repository to system
   - Configure branch tracking
   - Set up periodic sync

2. **Review Commits**
   - View pending commits
   - Examine commit diffs
   - Mark commits as reviewed/needs revision
   - Add comments to commits

3. **Manage Comments**
   - Add general commit comments
   - Add line-specific comments
   - Edit/delete own comments
   - View comment history

### Secondary Use Cases

4. **User Management**
   - Create user accounts
   - Assign repository access
   - Manage user permissions

5. **Repository Management**
   - Add/remove repositories
   - Configure tracking settings
   - View repository statistics

## API Endpoints

### REST API Structure

```
/api/v1/repositories
  GET    /           - List repositories
  POST   /           - Add repository
  GET    /:id        - Get repository details
  PUT    /:id        - Update repository
  DELETE /:id        - Remove repository
  POST   /:id/sync   - Sync repository commits

/api/v1/commits
  GET    /           - List commits (with filters)
  GET    /:id        - Get commit details
  GET    /:id/diff   - Get commit diff

/api/v1/reviews
  GET    /           - List reviews
  POST   /           - Create review
  GET    /:id        - Get review details
  PUT    /:id        - Update review status
  DELETE /:id        - Delete review

/api/v1/comments
  GET    /           - List comments
  POST   /           - Create comment
  GET    /:id        - Get comment details
  PUT    /:id        - Update comment
  DELETE /:id        - Delete comment

/api/v1/users
  GET    /           - List users
  POST   /           - Create user
  GET    /:id        - Get user details
  PUT    /:id        - Update user
```

### GraphQL Schema Overview

```graphql
type User {
  id: ID!
  username: String!
  email: String!
  displayName: String!
  avatarUrl: String
  repositories: [Repository!]!
  reviews: [CommitReview!]!
  comments: [Comment!]!
}

type Repository {
  id: ID!
  name: String!
  fullName: String!
  url: String!
  branch: String!
  description: String
  isLocal: Boolean!
  commits: [Commit!]!
  pendingReviews: [CommitReview!]!
}

type Commit {
  id: ID!
  repository: Repository!
  commitHash: String!
  message: String!
  authorName: String!
  authorEmail: String!
  committedAt: DateTime!
  diffStats: DiffStats!
  review: CommitReview
  comments: [Comment!]!
}

type CommitReview {
  id: ID!
  commit: Commit!
  reviewer: User!
  status: ReviewStatus!
  reviewedAt: DateTime
  comments: [Comment!]!
}

type Comment {
  id: ID!
  commit: Commit!
  user: User!
  content: String!
  lineNumber: Int
  filePath: String
  createdAt: DateTime!
}

enum ReviewStatus {
  PENDING_REVIEW
  APPROVED
  NEEDS_REVISION
  DRAFT
}
```

## Frontend User Interface

### Main Views

1. **Repository Dashboard**
   - List of tracked repositories
   - Repository statistics
   - Quick actions (sync, settings)

2. **Commit List View**
   - Filterable list of commits
   - Review status indicators
   - Quick review actions

3. **Commit Detail View**
   - Commit metadata
   - Diff visualization (using existing diff system)
   - Review status and comments
   - Review actions

4. **Review Dashboard**
   - Pending reviews
   - Review statistics
   - User activity

### User Workflow

1. **Login** → Select user (currently only "plva")
2. **Repository Selection** → Choose repository (currently only local Haven repo)
3. **Commit Review** → View pending commits, examine diffs, mark as reviewed
4. **Comment Management** → Add comments, view comment history

## Implementation Notes

### Database Schema
- Use SQLAlchemy models following existing patterns
- Implement proper foreign key relationships
- Add indexes for common queries (repository_id, commit_hash, status)

### Integration Points
- Leverage existing diff generation system
- Use existing Git operations from CLI module
- Follow Clean Architecture patterns

### Security Considerations
- Validate repository access permissions
- Sanitize comment content
- Implement rate limiting for API endpoints

### Future Enhancements
- Multiple user support
- GitHub integration
- Email notifications
- Advanced filtering and search
- Review assignment automation
- Metrics and reporting