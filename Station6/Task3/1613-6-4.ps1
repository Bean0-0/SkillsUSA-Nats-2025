# Security Event Log Analyzer

param(
    [string]$OutputFile = "SecurityAnalysis_$(Get-Date -Format 'yyyyMMdd_HHmmss').log",
    [int]$DaysBack = 7,
    [switch]$Verbose
)

# Initialize output file
$OutputPath = Join-Path $PWD $OutputFile
$StartTime = Get-Date

# Function to write to both console and log file
function Write-LogOutput {
    param([string]$Message, [string]$Level = "INFO")
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    
    Write-Host $LogEntry
    Add-Content -Path $OutputPath -Value $LogEntry
}

# Function to analyze failed login attempts
function Analyze-FailedLogins {
    Write-LogOutput "=== ANALYZING FAILED LOGIN ATTEMPTS ===" "HEADER"
    
    try {
        $FailedLogins = Get-WinEvent -FilterHashtable @{
            LogName = 'Security'
            ID = 4625  # Failed logon attempts
            StartTime = (Get-Date).AddDays(-$DaysBack)
        } -ErrorAction SilentlyContinue
        
        if ($FailedLogins) {
            Write-LogOutput "Found $($FailedLogins.Count) failed login attempts in the last $DaysBack days" "ALERT"
            
            # Group by username and count attempts
            $UserFailures = $FailedLogins | ForEach-Object {
                $Event = [xml]$_.ToXml()
                $Username = $Event.Event.EventData.Data | Where-Object {$_.Name -eq 'TargetUserName'} | Select-Object -ExpandProperty '#text'
                $SourceIP = $Event.Event.EventData.Data | Where-Object {$_.Name -eq 'IpAddress'} | Select-Object -ExpandProperty '#text'
                
                [PSCustomObject]@{
                    Username = $Username
                    SourceIP = $SourceIP
                    Time = $_.TimeCreated
                }
            } | Group-Object Username | Sort-Object Count -Descending
            
            foreach ($User in $UserFailures) {
                if ($User.Count -gt 5) {
                    Write-LogOutput "SUSPICIOUS: User '$($User.Name)' has $($User.Count) failed login attempts" "CRITICAL"
                    $User.Group | ForEach-Object {
                        Write-LogOutput "  - Failed login from $($_.SourceIP) at $($_.Time)" "DETAIL"
                    }
                }
            }
            
            # Check for brute force patterns (multiple failures from same IP)
            $IPFailures = $FailedLogins | ForEach-Object {
                $Event = [xml]$_.ToXml()
                $SourceIP = $Event.Event.EventData.Data | Where-Object {$_.Name -eq 'IpAddress'} | Select-Object -ExpandProperty '#text'
                $SourceIP
            } | Group-Object | Sort-Object Count -Descending
            
            foreach ($IP in $IPFailures) {
                if ($IP.Count -gt 10) {
                    Write-LogOutput "BRUTE FORCE DETECTED: IP $($IP.Name) attempted $($IP.Count) failed logins" "CRITICAL"
                }
            }
        } else {
            Write-LogOutput "No failed login attempts found in the specified timeframe" "INFO"
        }
    }
    catch {
        Write-LogOutput "Error analyzing failed logins: $($_.Exception.Message)" "ERROR"
    }
}

# Function to analyze service start/stop events
function Analyze-ServiceEvents {
    Write-LogOutput "`n=== ANALYZING SERVICE START/STOP EVENTS ===" "HEADER"
    
    try {
        # Service start events (Event ID 7036)
        $ServiceEvents = Get-WinEvent -FilterHashtable @{
            LogName = 'System'
            ID = 7036  # Service start/stop
            StartTime = (Get-Date).AddDays(-$DaysBack)
        } -ErrorAction SilentlyContinue
        
        if ($ServiceEvents) {
            Write-LogOutput "Found $($ServiceEvents.Count) service events in the last $DaysBack days" "INFO"
            
            # Look for unusual service starts (especially during odd hours)
            $SuspiciousServices = @('RemoteRegistry', 'Telnet', 'RemoteAccess', 'TermService')
            
            foreach ($Event in $ServiceEvents) {
                $Message = $Event.Message
                $Time = $Event.TimeCreated
                
                # Check for suspicious services
                foreach ($Service in $SuspiciousServices) {
                    if ($Message -like "*$Service*" -and $Message -like "*running*") {
                        Write-LogOutput "SUSPICIOUS: Service '$Service' started at $Time" "WARNING"
                        Write-LogOutput "  Message: $Message" "DETAIL"
                    }
                }
                
                # Check for services starting at unusual hours (between 11 PM and 6 AM)
                if (($Time.Hour -ge 23 -or $Time.Hour -le 6) -and $Message -like "*running*") {
                    Write-LogOutput "UNUSUAL TIME: Service started at unusual hour: $Time" "WARNING"
                    Write-LogOutput "  Message: $Message" "DETAIL"
                }
            }
        } else {
            Write-LogOutput "No service events found in the specified timeframe" "INFO"
        }
    }
    catch {
        Write-LogOutput "Error analyzing service events: $($_.Exception.Message)" "ERROR"
    }
}

# Function to analyze privilege escalation attempts
function Analyze-PrivilegeEscalation {
    Write-LogOutput "`n=== ANALYZING PRIVILEGE ESCALATION ATTEMPTS ===" "HEADER"
    
    try {
        # Special privileges assigned to new logon (Event ID 4672)
        $PrivEvents = Get-WinEvent -FilterHashtable @{
            LogName = 'Security'
            ID = 4672  # Special privileges assigned
            StartTime = (Get-Date).AddDays(-$DaysBack)
        } -ErrorAction SilentlyContinue
        
        if ($PrivEvents) {
            Write-LogOutput "Found $($PrivEvents.Count) privilege assignment events" "INFO"
            
            foreach ($Event in $PrivEvents) {
                $EventXml = [xml]$Event.ToXml()
                $Username = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'SubjectUserName'} | Select-Object -ExpandProperty '#text'
                $Privileges = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'PrivilegeList'} | Select-Object -ExpandProperty '#text'
                
                # Look for sensitive privileges
                $SensitivePrivs = @('SeDebugPrivilege', 'SeTakeOwnershipPrivilege', 'SeLoadDriverPrivilege', 'SeBackupPrivilege')
                
                foreach ($Priv in $SensitivePrivs) {
                    if ($Privileges -like "*$Priv*") {
                        Write-LogOutput "PRIVILEGE ESCALATION: User '$Username' assigned sensitive privilege '$Priv' at $($Event.TimeCreated)" "CRITICAL"
                    }
                }
            }
        }
        
        # Account logon with explicit credentials (Event ID 4648)
        $ExplicitLogons = Get-WinEvent -FilterHashtable @{
            LogName = 'Security'
            ID = 4648  # Logon with explicit credentials
            StartTime = (Get-Date).AddDays(-$DaysBack)
        } -ErrorAction SilentlyContinue
        
        if ($ExplicitLogons) {
            Write-LogOutput "Found $($ExplicitLogons.Count) explicit credential logon events" "INFO"
            
            # Group by user to find unusual patterns
            $ExplicitLogonUsers = $ExplicitLogons | ForEach-Object {
                $EventXml = [xml]$_.ToXml()
                $Username = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'SubjectUserName'} | Select-Object -ExpandProperty '#text'
                $TargetUser = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'TargetUserName'} | Select-Object -ExpandProperty '#text'
                
                [PSCustomObject]@{
                    SourceUser = $Username
                    TargetUser = $TargetUser
                    Time = $_.TimeCreated
                }
            } | Group-Object SourceUser | Sort-Object Count -Descending
            
            foreach ($User in $ExplicitLogonUsers) {
                if ($User.Count -gt 5) {
                    Write-LogOutput "SUSPICIOUS: User '$($User.Name)' used explicit credentials $($User.Count) times" "WARNING"
                }
            }
        }
    }
    catch {
        Write-LogOutput "Error analyzing privilege escalation: $($_.Exception.Message)" "ERROR"
    }
}

# Function to analyze unauthorized access attempts
function Analyze-UnauthorizedAccess {
    Write-LogOutput "`n=== ANALYZING UNAUTHORIZED ACCESS ATTEMPTS ===" "HEADER"
    
    try {
        # Access denied events (Event ID 4656)
        $AccessDenied = Get-WinEvent -FilterHashtable @{
            LogName = 'Security'
            ID = 4656  # Handle to object requested
            StartTime = (Get-Date).AddDays(-$DaysBack)
        } -ErrorAction SilentlyContinue | Where-Object { $_.Message -like "*failed*" -or $_.Message -like "*denied*" }
        
        if ($AccessDenied) {
            Write-LogOutput "Found $($AccessDenied.Count) access denied events" "INFO"
            
            foreach ($Event in $AccessDenied) {
                $EventXml = [xml]$Event.ToXml()
                $Username = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'SubjectUserName'} | Select-Object -ExpandProperty '#text'
                $ObjectName = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'ObjectName'} | Select-Object -ExpandProperty '#text'
                
                if ($ObjectName -and $Username) {
                    Write-LogOutput "ACCESS DENIED: User '$Username' denied access to '$ObjectName' at $($Event.TimeCreated)" "WARNING"
                }
            }
        }
        
        # Process creation events for suspicious processes (Event ID 4688)
        $ProcessEvents = Get-WinEvent -FilterHashtable @{
            LogName = 'Security'
            ID = 4688  # Process creation
            StartTime = (Get-Date).AddDays(-$DaysBack)
        } -ErrorAction SilentlyContinue
        
        if ($ProcessEvents) {
            $SuspiciousProcesses = @('cmd.exe', 'powershell.exe', 'psexec.exe', 'net.exe', 'netsh.exe')
            
            foreach ($Event in $ProcessEvents) {
                $EventXml = [xml]$Event.ToXml()
                $ProcessName = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'NewProcessName'} | Select-Object -ExpandProperty '#text'
                $Username = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'SubjectUserName'} | Select-Object -ExpandProperty '#text'
                
                foreach ($SuspProc in $SuspiciousProcesses) {
                    if ($ProcessName -like "*$SuspProc*") {
                        $Time = $Event.TimeCreated
                        if ($Time.Hour -ge 22 -or $Time.Hour -le 6) {
                            Write-LogOutput "SUSPICIOUS PROCESS: '$SuspProc' started by '$Username' at unusual time $Time" "WARNING"
                        }
                    }
                }
            }
        }
    }
    catch {
        Write-LogOutput "Error analyzing unauthorized access: $($_.Exception.Message)" "ERROR"
    }
}

# Function to analyze account management events
function Analyze-AccountManagement {
    Write-LogOutput "`n=== ANALYZING ACCOUNT MANAGEMENT EVENTS ===" "HEADER"
    
    try {
        # User account created (Event ID 4720)
        $AccountCreated = Get-WinEvent -FilterHashtable @{
            LogName = 'Security'
            ID = 4720
            StartTime = (Get-Date).AddDays(-$DaysBack)
        } -ErrorAction SilentlyContinue
        
        if ($AccountCreated) {
            Write-LogOutput "Found $($AccountCreated.Count) account creation events" "INFO"
            
            foreach ($Event in $AccountCreated) {
                $EventXml = [xml]$Event.ToXml()
                $NewUser = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'TargetUserName'} | Select-Object -ExpandProperty '#text'
                $Creator = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'SubjectUserName'} | Select-Object -ExpandProperty '#text'
                
                Write-LogOutput "ACCOUNT CREATED: '$NewUser' created by '$Creator' at $($Event.TimeCreated)" "WARNING"
            }
        }
        
        # User added to group (Event ID 4728)
        $GroupAdditions = Get-WinEvent -FilterHashtable @{
            LogName = 'Security'
            ID = 4728
            StartTime = (Get-Date).AddDays(-$DaysBack)
        } -ErrorAction SilentlyContinue
        
        if ($GroupAdditions) {
            foreach ($Event in $GroupAdditions) {
                $EventXml = [xml]$Event.ToXml()
                $Username = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'MemberName'} | Select-Object -ExpandProperty '#text'
                $GroupName = $EventXml.Event.EventData.Data | Where-Object {$_.Name -eq 'TargetUserName'} | Select-Object -ExpandProperty '#text'
                
                # Check for additions to privileged groups
                $PrivilegedGroups = @('Administrators', 'Domain Admins', 'Enterprise Admins', 'Backup Operators')
                
                foreach ($PrivGroup in $PrivilegedGroups) {
                    if ($GroupName -like "*$PrivGroup*") {
                        Write-LogOutput "PRIVILEGE ESCALATION: User added to privileged group '$GroupName' at $($Event.TimeCreated)" "CRITICAL"
                    }
                }
            }
        }
    }
    catch {
        Write-LogOutput "Error analyzing account management: $($_.Exception.Message)" "ERROR"
    }
}

# Main execution
Write-LogOutput "Security Event Log Analysis Started" "INFO"
Write-LogOutput "Analysis Parameters:"
Write-LogOutput "  - Output File: $OutputPath"
Write-LogOutput "  - Days Back: $DaysBack"
Write-LogOutput "  - Start Time: $StartTime"
Write-LogOutput "=========================================="

# Check if running with appropriate privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-LogOutput "WARNING: Script is not running with Administrator privileges. Some events may not be accessible." "WARNING"
}

# Execute analysis functions
Analyze-FailedLogins
Analyze-ServiceEvents
Analyze-PrivilegeEscalation
Analyze-UnauthorizedAccess
Analyze-AccountManagement

# Generate summary
$EndTime = Get-Date
$Duration = $EndTime - $StartTime

Write-LogOutput "`n=========================================="
Write-LogOutput "Security Event Log Analysis Completed" "INFO"
Write-LogOutput "Analysis Duration: $($Duration.TotalMinutes.ToString('F2')) minutes"
Write-LogOutput "Results saved to: $OutputPath"

# Display file size of output
$FileSize = (Get-Item $OutputPath).Length
Write-LogOutput "Output file size: $([math]::Round($FileSize/1KB, 2)) KB"

Write-Host "`nAnalysis complete. Check the log file for detailed results: $OutputPath" -ForegroundColor Green
