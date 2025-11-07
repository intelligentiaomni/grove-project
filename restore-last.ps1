# --- Grove Project Restore Script ---
param([string]\)

if (-not \) {
    Write-Host 'Usage: ./restore-last.ps1 <branch-name>'
    Write-Host 'Example: ./restore-last.ps1 backup-main-20251107-2210'
    exit
}

Write-Host "⏪ Restoring from backup branch: \"
git checkout main
git reset --hard \
git push origin main --force
Write-Host "✅ Restore complete. main reset to \"
