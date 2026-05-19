# Installation Verification Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Checker" -ForegroundColor Cyan
Write-Host "AI-Driven Mental Health System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python: $pythonVersion" -ForegroundColor Green
    
    # Check pip
    $pipVersion = pip --version 2>&1
    Write-Host "  ✓ pip: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
    Write-Host "    Install from: https://www.python.org/downloads/" -ForegroundColor Gray
    $allGood = $false
}

Write-Host ""

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js: $nodeVersion" -ForegroundColor Green
    
    # Check npm
    $npmVersion = npm --version 2>&1
    Write-Host "  ✓ npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js not found" -ForegroundColor Red
    Write-Host "    Install from: https://nodejs.org/" -ForegroundColor Gray
    $allGood = $false
}

Write-Host ""

# Check Backend dependencies
Write-Host "Checking Backend..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "backend"

if (Test-Path (Join-Path $backendPath "requirements.txt")) {
    Write-Host "  ✓ requirements.txt found" -ForegroundColor Green
} else {
    Write-Host "  ✗ requirements.txt not found" -ForegroundColor Red
    $allGood = $false
}

if (Test-Path (Join-Path $backendPath ".env")) {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠ .env file not found (will use .env.example)" -ForegroundColor Yellow
}

$modelPath = Join-Path $backendPath "models\distilbert-goemotions-mental"
if (Test-Path $modelPath) {
    Write-Host "  ✓ Model directory found" -ForegroundColor Green
    
    $requiredFiles = @("config.json", "pytorch_model.bin", "tokenizer_config.json", "vocab.txt")
    $missingFiles = @()
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path (Join-Path $modelPath $file))) {
            $missingFiles += $file
        }
    }
    
    if ($missingFiles.Count -eq 0) {
        Write-Host "  ✓ All model files present" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Missing model files: $($missingFiles -join ', ')" -ForegroundColor Yellow
        Write-Host "    Copy your trained model files to: $modelPath" -ForegroundColor Gray
    }
} else {
    Write-Host "  ⚠ Model directory not found" -ForegroundColor Yellow
    Write-Host "    Create: $modelPath" -ForegroundColor Gray
    Write-Host "    Copy your Phase 2 trained model files there" -ForegroundColor Gray
}

Write-Host ""

# Check Frontend dependencies
Write-Host "Checking Frontend..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"

if (Test-Path (Join-Path $frontendPath "package.json")) {
    Write-Host "  ✓ package.json found" -ForegroundColor Green
} else {
    Write-Host "  ✗ package.json not found" -ForegroundColor Red
    $allGood = $false
}

if (Test-Path (Join-Path $frontendPath ".env")) {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠ .env file not found (will use .env.example)" -ForegroundColor Yellow
}

if (Test-Path (Join-Path $frontendPath "node_modules")) {
    Write-Host "  ✓ node_modules installed" -ForegroundColor Green
} else {
    Write-Host "  ⚠ node_modules not found" -ForegroundColor Yellow
    Write-Host "    Run: cd frontend; npm install" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✓ All checks passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Install backend dependencies: cd backend; pip install -r requirements.txt" -ForegroundColor Gray
    Write-Host "  2. Install frontend dependencies: cd frontend; npm install" -ForegroundColor Gray
    Write-Host "  3. Add your trained model to: backend\models\distilbert-goemotions-mental\" -ForegroundColor Gray
    Write-Host "  4. Run: .\start.ps1" -ForegroundColor Gray
} else {
    Write-Host "✗ Some requirements are missing" -ForegroundColor Red
    Write-Host "  Please install missing components and run this script again" -ForegroundColor Gray
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
