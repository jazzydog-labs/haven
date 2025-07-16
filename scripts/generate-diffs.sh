#!/usr/bin/env bash

# Script to generate diff HTML files for each commit in the current branch
# and create an index.html with links to all diffs

set -euo pipefail

# Configuration
OUTPUT_DIR="diff-out"
BRANCH="${1:-HEAD}"
BASE_BRANCH="${2:-main}"
MAX_COMMITS="${3:-50}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}Generating diffs for branch: $BRANCH${NC}"
echo -e "${BLUE}Base branch: $BASE_BRANCH${NC}"
echo -e "${BLUE}Output directory: $OUTPUT_DIR${NC}"
echo ""

# Get list of commits in the current branch (excluding those in base branch)
if [ "$BRANCH" == "HEAD" ]; then
    # If on current branch, get commits not in base branch
    COMMITS=$(git rev-list --reverse --max-count="$MAX_COMMITS" "$BASE_BRANCH".."$BRANCH")
else
    # If specific branch provided
    COMMITS=$(git rev-list --reverse --max-count="$MAX_COMMITS" "$BASE_BRANCH".."$BRANCH")
fi

# Check if diff2html is installed
if ! command -v diff2html &> /dev/null; then
    echo -e "${YELLOW}diff2html is not installed. Installing...${NC}"
    npm install -g diff2html-cli
fi

# Arrays to store commit info for index
declare -a COMMIT_HASHES
declare -a COMMIT_MESSAGES
declare -a COMMIT_AUTHORS
declare -a COMMIT_DATES
declare -a COMMIT_FILES

# Counter for commits
COUNT=0

# Generate diff for each commit
echo -e "${GREEN}Generating individual commit diffs...${NC}"
for COMMIT in $COMMITS; do
    COUNT=$((COUNT + 1))
    
    # Get commit info
    HASH=$(git rev-parse --short "$COMMIT")
    MESSAGE=$(git log -1 --pretty=format:"%s" "$COMMIT")
    AUTHOR=$(git log -1 --pretty=format:"%an" "$COMMIT")
    DATE=$(git log -1 --pretty=format:"%ad" --date=short "$COMMIT")
    
    # Store in arrays
    COMMIT_HASHES+=("$HASH")
    COMMIT_MESSAGES+=("$MESSAGE")
    COMMIT_AUTHORS+=("$AUTHOR")
    COMMIT_DATES+=("$DATE")
    
    # Generate filename
    FILENAME="${COUNT}-${HASH}-$(echo "$MESSAGE" | sed 's/[^a-zA-Z0-9]/-/g' | cut -c1-50).html"
    COMMIT_FILES+=("$FILENAME")
    
    echo -e "  ${COUNT}. Generating diff for ${HASH}: ${MESSAGE:0:60}..."
    
    # Generate diff HTML
    diff2html -s side -f html -F "$OUTPUT_DIR/$FILENAME" \
        -t "$HASH: $MESSAGE" \
        --summary open \
        --highlightCode \
        -- "$COMMIT^..$COMMIT" 2>/dev/null || {
            echo -e "    ${YELLOW}Warning: Could not generate diff for $HASH${NC}"
            continue
        }
done

echo ""
echo -e "${GREEN}Generating index.html...${NC}"

# Generate index.html
cat > "$OUTPUT_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commit Diff Index</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        h1 {
            color: #333;
            border-bottom: 2px solid #0366d6;
            padding-bottom: 10px;
        }
        
        .info {
            background-color: #e3f2fd;
            border-left: 4px solid #0366d6;
            padding: 10px 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        
        .commit-list {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .commit {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid #e1e4e8;
            transition: background-color 0.2s;
        }
        
        .commit:hover {
            background-color: #f6f8fa;
        }
        
        .commit:last-child {
            border-bottom: none;
        }
        
        .commit-number {
            flex-shrink: 0;
            width: 40px;
            height: 40px;
            background-color: #0366d6;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }
        
        .commit-details {
            flex-grow: 1;
            min-width: 0;
        }
        
        .commit-message {
            font-weight: 500;
            color: #0366d6;
            text-decoration: none;
            display: block;
            margin-bottom: 5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .commit-message:hover {
            text-decoration: underline;
        }
        
        .commit-meta {
            font-size: 14px;
            color: #586069;
        }
        
        .commit-hash {
            font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
            background-color: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 12px;
        }
        
        .stats {
            margin: 20px 0;
            display: flex;
            gap: 20px;
        }
        
        .stat {
            background-color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #0366d6;
        }
        
        .stat-label {
            font-size: 14px;
            color: #586069;
            margin-top: 5px;
        }
        
        .branch-info {
            background-color: #f3f4f6;
            padding: 8px 12px;
            border-radius: 4px;
            display: inline-block;
            font-family: monospace;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .commit {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .commit-number {
                margin-bottom: 10px;
            }
            
            .stats {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <h1>Commit Diff Index</h1>
    
    <div class="info">
        <strong>Branch:</strong> <span class="branch-info">BRANCH_NAME</span> → <span class="branch-info">BASE_BRANCH_NAME</span><br>
        <strong>Generated:</strong> GENERATION_DATE<br>
        <strong>Total Commits:</strong> TOTAL_COMMITS
    </div>
    
    <div class="stats">
        <div class="stat">
            <div class="stat-value">TOTAL_COMMITS</div>
            <div class="stat-label">Total Commits</div>
        </div>
        <div class="stat">
            <div class="stat-value">UNIQUE_AUTHORS</div>
            <div class="stat-label">Contributors</div>
        </div>
        <div class="stat">
            <div class="stat-value">DATE_RANGE</div>
            <div class="stat-label">Date Range</div>
        </div>
    </div>
    
    <div class="commit-list">
        <!-- Commits will be inserted here -->
    </div>
    
    <script>
        // Commit data
        const commits = [
            COMMIT_DATA
        ];
        
        // Populate commit list
        const commitList = document.querySelector('.commit-list');
        commits.forEach(commit => {
            const commitDiv = document.createElement('div');
            commitDiv.className = 'commit';
            commitDiv.innerHTML = `
                <div class="commit-number">${commit.number}</div>
                <div class="commit-details">
                    <a href="${commit.file}" class="commit-message" title="${commit.message}">${commit.message}</a>
                    <div class="commit-meta">
                        <span class="commit-hash">${commit.hash}</span>
                        by <strong>${commit.author}</strong>
                        on ${commit.date}
                    </div>
                </div>
            `;
            commitList.appendChild(commitDiv);
        });
    </script>
</body>
</html>
EOF

# Calculate stats
UNIQUE_AUTHORS=$(printf '%s\n' "${COMMIT_AUTHORS[@]}" | sort -u | wc -l)
if [ ${#COMMIT_DATES[@]} -gt 0 ]; then
    DATE_RANGE="${COMMIT_DATES[0]} - ${COMMIT_DATES[-1]}"
else
    DATE_RANGE="No commits"
fi

# Generate JavaScript array of commit data
COMMIT_DATA=""
for i in "${!COMMIT_HASHES[@]}"; do
    if [ $i -gt 0 ]; then
        COMMIT_DATA+=",\n            "
    fi
    # Escape quotes in message
    ESCAPED_MESSAGE=$(echo "${COMMIT_MESSAGES[$i]}" | sed 's/"/\\"/g')
    COMMIT_DATA+="{number: $((i+1)), hash: '${COMMIT_HASHES[$i]}', message: \"$ESCAPED_MESSAGE\", author: '${COMMIT_AUTHORS[$i]}', date: '${COMMIT_DATES[$i]}', file: '${COMMIT_FILES[$i]}'}"
done

# Get branch names
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" == "HEAD" ]; then
    BRANCH_DISPLAY="$CURRENT_BRANCH"
else
    BRANCH_DISPLAY="$BRANCH"
fi

# Replace placeholders in index.html
sed -i.bak \
    -e "s/BRANCH_NAME/$BRANCH_DISPLAY/g" \
    -e "s/BASE_BRANCH_NAME/$BASE_BRANCH/g" \
    -e "s/GENERATION_DATE/$(date '+%Y-%m-%d %H:%M:%S')/g" \
    -e "s/TOTAL_COMMITS/$COUNT/g" \
    -e "s/UNIQUE_AUTHORS/$UNIQUE_AUTHORS/g" \
    -e "s/DATE_RANGE/$DATE_RANGE/g" \
    -e "s/COMMIT_DATA/$COMMIT_DATA/g" \
    "$OUTPUT_DIR/index.html"

# Remove backup file
rm -f "$OUTPUT_DIR/index.html.bak"

echo ""
echo -e "${GREEN}✓ Generated $COUNT diff files${NC}"
echo -e "${GREEN}✓ Created index.html${NC}"
echo ""
echo -e "${BLUE}View the diffs by opening:${NC}"
echo -e "  ${YELLOW}$OUTPUT_DIR/index.html${NC}"
echo ""
echo -e "Or serve locally with:"
echo -e "  ${YELLOW}cd $OUTPUT_DIR && python -m http.server 8000${NC}"
echo -e "  Then visit: ${YELLOW}http://localhost:8000${NC}"