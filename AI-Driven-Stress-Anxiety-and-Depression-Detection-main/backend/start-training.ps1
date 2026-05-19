# Model Training Launcher
# Starts the model training process with progress tracking

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Mental Health System" -ForegroundColor Cyan
Write-Host "Model Training Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "train_model.py")) {
    Write-Host "❌ Error: Training scripts not found" -ForegroundColor Red
    Write-Host "   Please run this script from the backend directory" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   cd backend" -ForegroundColor Yellow
    Write-Host "   .\start-training.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Check Python
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if dependencies are installed
Write-Host "Checking training dependencies..." -ForegroundColor Yellow
$packagesInstalled = $true

$requiredPackages = @("datasets", "transformers", "torch", "accelerate")
foreach ($package in $requiredPackages) {
    try {
        python -c "import $package" 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ $package installed" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $package not found" -ForegroundColor Red
            $packagesInstalled = $false
        }
    } catch {
        Write-Host "  ✗ $package not found" -ForegroundColor Red
        $packagesInstalled = $false
    }
}

if (-not $packagesInstalled) {
    Write-Host ""
    Write-Host "⚠️  Missing dependencies!" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Install training dependencies now? (y/n)"
    
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host ""
        Write-Host "Installing dependencies..." -ForegroundColor Cyan
        pip install -r requirements-training.txt
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "Please install dependencies first:" -ForegroundColor Yellow
        Write-Host "  pip install -r requirements-training.txt" -ForegroundColor Gray
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Training Mode Selection" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Quick Training (Recommended for first time)" -ForegroundColor Yellow
Write-Host "   - Uses subset of data (5,000 samples)" -ForegroundColor Gray
Write-Host "   - 1 epoch only" -ForegroundColor Gray
Write-Host "   - Time: 5-10 minutes (CPU), 2-3 minutes (GPU)" -ForegroundColor Gray
Write-Host "   - Perfect for testing the setup" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Full Training (For production)" -ForegroundColor Yellow
Write-Host "   - Complete dataset (43,000+ samples)" -ForegroundColor Gray
Write-Host "   - 3 epochs with early stopping" -ForegroundColor Gray
Write-Host "   - Time: 1-3 hours (CPU), 30-60 minutes (GPU)" -ForegroundColor Gray
Write-Host "   - Achieves ~96% F1 score" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Select training mode (1 or 2)"

Write-Host ""

if ($choice -eq "1") {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Starting Quick Training" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This will take approximately 5-10 minutes..." -ForegroundColor Yellow
    Write-Host ""
    
    python train_model_quick.py
    
} elseif ($choice -eq "2") {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Starting Full Training" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  This will take 1-3 hours depending on your hardware" -ForegroundColor Yellow
    Write-Host ""
    $confirm = Read-Host "Continue? (y/n)"
    
    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        Write-Host ""
        python train_model.py
    } else {
        Write-Host "Training cancelled." -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "Invalid choice. Please select 1 or 2." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Training completed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Model saved to: backend\models\distilbert-goemotions-mental" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Start the backend server: python app.py" -ForegroundColor Gray
    Write-Host "  2. The model will load automatically" -ForegroundColor Gray
    Write-Host "  3. Test with your frontend application" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "❌ Training failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Check the error messages above for details." -ForegroundColor Yellow
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  - Out of memory: Try quick training or reduce batch size" -ForegroundColor Gray
    Write-Host "  - Download failed: Check internet connection" -ForegroundColor Gray
    Write-Host "  - Missing packages: Run 'pip install -r requirements-training.txt'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "See TRAINING_GUIDE.md for detailed troubleshooting" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
