// .github/scripts/post-pr-comment.js
const fs = require('fs');

async function run({ github, context, core }) {
  const reportPath = process.env.REPORT_PATH;
  const commentTitle = process.env.COMMENT_TITLE || "🔍 Security Scan Report";
  const maxChars = 60000;

  if (!reportPath || !fs.existsSync(reportPath)) {
    console.log(`Report not found at: ${reportPath}`);
    return;
  }

  const content = fs.readFileSync(reportPath, 'utf8');
  const truncated = content.length > maxChars
    ? content.slice(0, maxChars) + "\n\n...truncated"
    : content;

  const comments = await github.rest.issues.listComments({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: context.issue.number,
  });

  const existing = comments.data.find(c =>
    c.user.type === 'Bot' &&
    c.body.startsWith(`## ${commentTitle}`)
  );

  if (existing) {
    await github.rest.issues.updateComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      comment_id: existing.id,
      body: `## ${commentTitle}\n\n${truncated}`,
    });
    console.log(`Updated existing comment: ${commentTitle}`);
  } else {
    await github.rest.issues.createComment({
      issue_number: context.issue.number,
      owner: context.repo.owner,
      repo: context.repo.repo,
      body: `## ${commentTitle}\n\n${truncated}`,
    });
    console.log(`Created new comment: ${commentTitle}`);
  }
}

module.exports = run;
