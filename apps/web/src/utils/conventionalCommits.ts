interface CommitTypeInfo {
  emoji: string;
  label: string;
  color: string;
}

export const conventionalCommitTypes: Record<string, CommitTypeInfo> = {
  feat: { emoji: '✨', label: 'Feature', color: 'purple' },
  fix: { emoji: '🐛', label: 'Fix', color: 'red' },
  docs: { emoji: '📚', label: 'Docs', color: 'blue' },
  style: { emoji: '💎', label: 'Style', color: 'pink' },
  refactor: { emoji: '♻️', label: 'Refactor', color: 'green' },
  perf: { emoji: '⚡', label: 'Performance', color: 'orange' },
  test: { emoji: '🧪', label: 'Test', color: 'yellow' },
  build: { emoji: '🔨', label: 'Build', color: 'gray' },
  ci: { emoji: '👷', label: 'CI', color: 'indigo' },
  chore: { emoji: '🔧', label: 'Chore', color: 'gray' },
  revert: { emoji: '⏪', label: 'Revert', color: 'red' },
  wip: { emoji: '🚧', label: 'WIP', color: 'yellow' },
};

export function parseConventionalCommit(message: string): {
  type?: string;
  scope?: string;
  subject: string;
  breaking: boolean;
} {
  // Match conventional commit pattern: type(scope)!: subject
  const regex = /^(\w+)(?:\(([^)]+)\))?(!)?:\s*(.+)/;
  const match = message.match(regex);
  
  if (!match) {
    return { subject: message, breaking: false };
  }
  
  const [, type, scope, breaking, subject] = match;
  return {
    type: type?.toLowerCase(),
    scope,
    subject,
    breaking: !!breaking,
  };
}

export function getCommitTypeInfo(type?: string): CommitTypeInfo | null {
  if (!type) return null;
  return conventionalCommitTypes[type.toLowerCase()] || null;
}