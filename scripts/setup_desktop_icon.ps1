$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Leo AI.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Target: powershell.exe with arguments to run the launcher script
# Use absolute paths for the shortcut to work from the desktop
$ProjectRoot = (Resolve-Path "$PSScriptRoot\..").Path
$LauncherPath = Join-Path $ProjectRoot "run_assistant.ps1"
$IconPath = Join-Path $ProjectRoot "assets\icon.ico"

$Shortcut.TargetPath = "python.exe"
$Shortcut.Arguments = "`"$ProjectRoot\app_launcher.py`""
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.IconLocation = $IconPath
$Shortcut.Description = "Launch Leo AI Assistant"
$Shortcut.Save()

Write-Host "✅ Leo AI Desktop shortcut created successfully!" -ForegroundColor Green
