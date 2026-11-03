param (
    [string]$Token = $env:VERCEL_TOKEN,
    [string]$ProjectName = "realtime-leaderboard"
)

if (-not $Token) {
    Write-Host "No token provided." -ForegroundColor Red
    exit 1
}

$Token = $Token.Trim()

Write-Host "Packaging project files for Vercel deployment..." -ForegroundColor Cyan

$baseDir = $PSScriptRoot
$relativeFiles = @(
    "vercel.json",
    "requirements.txt",
    "api/index.py",
    "core/__init__.py",
    "core/models.py",
    "core/storage.py",
    "core/leaderboard.py",
    "core/static_assets.py",
    "data/leaderboard.json",
    "public/index.html",
    "public/style.css",
    "public/app.js"
)

$fileList = @()
foreach ($rel in $relativeFiles) {
    $fullPath = Join-Path $baseDir $rel
    if (Test-Path $fullPath) {
        $bytes = [System.IO.File]::ReadAllBytes($fullPath)
        $b64 = [Convert]::ToBase64String($bytes)
        $fileList += @{
            file = $rel.Replace('\', '/')
            data = $b64
            encoding = "base64"
        }
        Write-Host "  + Included: $rel" -ForegroundColor Gray
    } else {
        Write-Host "  ! Warning: $rel not found, skipping" -ForegroundColor Yellow
    }
}

$payloadObj = @{
    name = $ProjectName
    target = "production"
    files = $fileList
    projectSettings = @{
        framework = $null
    }
}

$payload = $payloadObj | ConvertTo-Json -Depth 10

Write-Host "Sending deployment to Vercel API..." -ForegroundColor Cyan

$headers = @{
    "Authorization" = "Bearer $Token"
    "Content-Type"  = "application/json"
}

try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $response = Invoke-RestMethod -Uri "https://api.vercel.com/v13/deployments" -Method Post -Headers $headers -Body $payload
    
    Write-Host ""
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "DEPLOYMENT INITIATED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "Deployment Name : $($response.name)" -ForegroundColor White
    Write-Host "Deployment ID   : $($response.id)" -ForegroundColor White
    Write-Host "Deployment URL  : https://$($response.url)" -ForegroundColor Cyan
    Write-Host "Status          : $($response.readyState)" -ForegroundColor White
    Write-Host "==========================================================" -ForegroundColor Green
    
    $resultObj = @{
        id = $response.id
        url = "https://$($response.url)"
        name = $response.name
    } | ConvertTo-Json

    $resultObj | Out-File (Join-Path $baseDir "deployment-result.json") -Encoding utf8
    Write-Host "Result saved to deployment-result.json" -ForegroundColor Gray
} catch {
    Write-Host ""
    Write-Host "Error during deployment:" -ForegroundColor Red
    if ($_.Exception.Response) {
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $errBody = $reader.ReadToEnd()
        Write-Host $errBody -ForegroundColor Red
    } else {
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
    exit 1
}
