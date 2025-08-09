const fs = require('fs');
const { Octokit } = require('@octokit/rest');

async function main() {
  const token = process.env.GITHUB_TOKEN;
  if (!token) {
    console.error("GITHUB_TOKEN is not set in environment variables.");
    process.exit(1);
  }

  const octokit = new Octokit({ auth: token });

  // Get required info from env variables (GitHub Actions sets these automatically)
  const owner = process.env.GITHUB_REPOSITORY_OWNER;
  const repo = process.env.GITHUB_REPOSITORY.split('/')[1];
  const prNumber = process.env.PR_NUMBER;

  if (!owner || !repo || !prNumber) {
    console.error("Missing owner, repo, or PR number environment variables.");
    process.exit(1);
  }

  const reportPath = 'security-reports/summary_report.md';
  if (!fs.existsSync(reportPath)) {
    console.log("Summary report not found, skipping comment.");
    return;
  }

  const reportContent = fs.readFileSync(reportPath, 'utf8');
  const MAX_CHARS = 60000;
  const truncatedContent = reportContent.length > MAX_CHARS
    ? reportContent.slice(0, MAX_CHARS) + "\n\n...truncated"
    : reportContent;

  // List comments on the PR
  const { data: comments } = await octokit.rest.issues.listComments({
    owner,
    repo,
    issue_number: prNumber,
  });

  // Find existing bot comment starting with report header
  const existingComment = comments.find(
    c => c.user.type === 'Bot' && c.body.startsWith('## 🔐 Security Scan Report')
  );

  if (existingComment) {
    // Update the existing comment
    await octokit.rest.issues.updateComment({
      owner,
      repo,
      comment_id: existingComment.id,
      body: `## 🔐 Security Scan Report\n\n${truncatedContent}`,
    });
    console.log("Updated existing security scan comment.");
  } else {
    // Create new comment
    await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: prNumber,
      body: `## 🔐 Security Scan Report\n\n${truncatedContent}`,
    });
    console.log("Created new security scan comment.");
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
