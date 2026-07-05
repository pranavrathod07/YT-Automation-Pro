# Ye script khud automatically 2 Windows Scheduled Tasks bana deta hai:
#   1) YT_Automation_Morning -> roz 12:00 AM
#   2) YT_Automation_Evening -> roz 7:00 PM
#
# Chalane ka tarika (VS Code terminal me, isi project folder ke andar):
#   powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1

$pythonPath = (Get-Command python).Source
$projectPath = (Get-Location).Path
$scriptPath = Join-Path $projectPath "main.py"

Write-Host "Python path: $pythonPath"
Write-Host "Project path: $projectPath"

# Purana task hoga to hata do (taaki dobara chalane par error na aaye)
schtasks /Delete /TN "YT_Automation_Morning" /F 2>$null
schtasks /Delete /TN "YT_Automation_Evening" /F 2>$null

# Morning task - 12:00 AM daily
schtasks /Create /TN "YT_Automation_Morning" `
  /TR "`"$pythonPath`" `"$scriptPath`"" `
  /SC DAILY /ST 00:00 `
  /F

# Evening task - 7:00 PM daily
schtasks /Create /TN "YT_Automation_Evening" `
  /TR "`"$pythonPath`" `"$scriptPath`"" `
  /SC DAILY /ST 19:00 `
  /F

Write-Host ""
Write-Host "Dono tasks ban gaye aur enabled hai:"
schtasks /Query /TN "YT_Automation_Morning"
schtasks /Query /TN "YT_Automation_Evening"

Write-Host ""
Write-Host "Ab test ke liye Morning task turant chala rahe hai..."
schtasks /Run /TN "YT_Automation_Morning"

Write-Host ""
Write-Host "Ho gaya! Task Scheduler app khol ke bhi in dono tasks ko dekh sakte ho (search 'Task Scheduler')."
