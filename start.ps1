# Quick Start Script for Windows

Write-Host "PRA COREP Assistant - Quick Start" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub token is set
if (-not $env:GITHUB_TOKEN) {
    Write-Host "ERROR: GITHUB_TOKEN environment variable not set!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set your GitHub token:" -ForegroundColor Yellow
    Write-Host '  $Env:GITHUB_TOKEN="your-github-token-here"' -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Get a token at: https://github.com/settings/tokens" -ForegroundColor Yellow
    Write-Host "Required permission: models:read" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ GitHub token found" -ForegroundColor Green
Write-Host ""

# Start backend
Write-Host "Starting backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m venv venv; .\venv\Scripts\activate; pip install -r requirements.txt; uvicorn app.main:app --reload"

Start-Sleep -Seconds 3

# Start frontend
Write-Host "Starting frontend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm install; npm run dev"

Write-Host ""
Write-Host "✓ Servers starting..." -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
