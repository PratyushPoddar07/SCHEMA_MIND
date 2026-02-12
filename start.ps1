# QueryMind AI Start Script for Windows

Write-Host "[*] Starting QueryMind AI Setup..." -ForegroundColor Cyan

# Check for Docker
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Docker is not installed. Please install Docker Desktop." -ForegroundColor Red
    exit
}

# Create .env if it doesn't exist
if (!(Test-Path .env)) {
    Write-Host "[+] Creating .env file..." -ForegroundColor Yellow
    $secret = [Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
    "ANTHROPIC_API_KEY=your_anthropic_api_key_here`nSECRET_KEY=$secret" | Out-File -FilePath .env -Encoding utf8
    Write-Host "[!] Please edit .env file and add your Anthropic API key." -ForegroundColor Yellow
    Pause
}

# Start Docker services
Write-Host "[*] Building and starting services..." -ForegroundColor Cyan
docker compose up -d --build

Write-Host ""
Write-Host "[+] Services are starting!" -ForegroundColor Green
Write-Host "--- Access the application ---" -ForegroundColor White
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor Green
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor Green
Write-Host "   API Docs:  http://localhost:8000/api/docs" -ForegroundColor Green
Write-Host ""
Write-Host "[*] View logs with: docker compose logs -f" -ForegroundColor White
