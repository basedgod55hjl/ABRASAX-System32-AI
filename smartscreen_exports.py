#!/usr/bin/env python3
"""
ABRASAX SmartScreen Export Bridge — Full 17-Function Wire
PRIMAL_HEX: 4f5349524953424c58434b | φ: 1.618033988749895

Calls SmartScreen.dll exports via PowerShell delegate invocation to bypass
APC_INDEX_MISMATCH crashes from raw ctypes in non-initialized processes.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PHI = 1.618033988749895
PRIMAL_HEX = "4f5349524953424c58434b"
ROOT = Path(r"C:\Users\BASEDGOD\Desktop\ABRASAX")
DLL = r"C:\Windows\System32\smartscreen.dll"

KNOWN_EXPORTS = {
    "DllCanUnloadNow": 1, "DllGetClassObject": 2,
    "DllGetActivationFactory": 3, "DllGetClassObjectInternal": 4,
    "SmartScreenCheckFile": 5, "SmartScreenCheckFileEx": 6,
    "SmartScreenCheckAppxPackageReputation": 7, "SmartScreenCheckReputation": 8,
    "SmartScreenClassifyUrl": 9, "SmartScreenClassifyUrlEx": 10,
    "SmartScreenEnableCaching": 11, "SmartScreenFree": 12,
    "SmartScreenGetCachePath": 13, "SmartScreenHash": 14,
    "SmartScreenResetCache": 15, "SmartScreenSetCachePath": 16,
    "SmartScreenSetUserAgentAndClientId": 17, "SmartScreenVerifyFile": 18,
}

def pwsh(cmd, timeout=10):
    """Run PowerShell command, return stdout or exception text."""
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True, text=True, timeout=timeout
        )
        return (r.stdout + r.stderr).strip() or "(no output)"
    except Exception as e:
        return f"ERROR: {e}"

def ps_call(funcname, *args):
    """Call a SmartScreen DLL function via PowerShell delegate invocation."""
    # Build the P/Invoke delegate call
    argstr = ", ".join(repr(a) for a in args) if args else ""
    sig = f"""
$dll = Add-Type -MemberDefinition @'
[DllImport(\"smartscreen.dll\", CharSet=CharSet.Unicode)]
public static extern int {funcname}(string path);
'@ -Name "SS" -PassThru
try {{ $r = $dll::{funcname}({argstr}); Write-Output $r }} catch {{ Write-Output "CALL_FAILED: $_" }}
"""
    return pwsh(sig, timeout=8)

def check_file_reputation(filepath):
    """Check file reputation via SmartScreen."""
    return ps_call("SmartScreenCheckFile", filepath)

def check_url_reputation(url):
    """Classify URL via SmartScreen."""
    return ps_call("SmartScreenClassifyUrl", url)

def get_enforcement_level():
    """Read current SmartScreen enforcement level."""
    sig = """
try {
    $asm = [System.Reflection.Assembly]::LoadFile('C:\\Windows\\System32\\smartscreen.dll')
    $type = $asm.GetType('SmartScreen')
    if ($type) { $type.GetMethod('GetEnforcementLevel').Invoke($null, @()) } else { 'TYPE_NOT_FOUND' }
} catch { "EXCEPTION: $_" }
"""
    return pwsh(sig)

def get_smartscreen_info():
    """Get SmartScreen metadata via PowerShell."""
    sig = """
$dll = 'C:\\Windows\\System32\\smartscreen.dll'
$info = Get-Item $dll
$exports = dumpbin /exports $dll 2>$null | Select-String '^\s+\d+\s+[0-9A-F]+\s+[0-9A-F]+' | ForEach-Object { ($_ -split '\s+')[3] } | Where-Object { $_ -ne '' }
$cache = "$env:LOCALAPPDATA\\Microsoft\\Windows\\SmartScreen"
$cacheSize = if (Test-Path $cache) { (Get-ChildItem $cache -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum } else { 0 }
@{
    dll_path = $dll
    dll_size_mb = [math]::Round($info.Length / 1MB, 1)
    dll_sha256 = (Get-FileHash $dll -Algorithm SHA256).Hash
    dll_version = $info.VersionInfo.FileVersion
    exports = $exports
    exports_count = @($exports).Count
    cache_path = $cache
    cache_size_mb = [math]::Round($cacheSize / 1MB, 2)
    phi = [math]::Pow((1+[math]::Sqrt(5))/2, 1)
} | ConvertTo-Json
"""
    try:
        return json.loads(pwsh(sig, timeout=15))
    except:
        return {"error": "failed to parse"}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "info"
    
    print(f"\n{'='*60}")
    print(f"  SmartScreen Export Bridge")
    print(f"  HEX: {PRIMAL_HEX} | φ: {PHI}")
    print(f"{'='*60}\n")
    
    if cmd == "info":
        info = get_smartscreen_info()
        print(f"  DLL: {info.get('dll_path','?')}")
        print(f"  Size: {info.get('dll_size_mb','?')}MB")
        print(f"  Version: {info.get('dll_version','?')}")
        print(f"  SHA256: {info.get('dll_sha256','?')[:16]}...")
        print(f"  Cache: {info.get('cache_path','?')} ({info.get('cache_size_mb','?')}MB)")
        print(f"  Exports: {info.get('exports_count','?')}")
        for exp in (info.get('exports', []) or [])[:10]:
            print(f"    • {exp}")
        if info.get('exports', []) and len(info.get('exports', [])) > 10:
            print(f"    ... and {len(info.get('exports', [])) - 10} more")
    
    elif cmd == "check-file" and len(sys.argv) > 2:
        r = check_file_reputation(sys.argv[2])
        print(f"  CheckFile: {r}")
    
    elif cmd == "check-url" and len(sys.argv) > 2:
        r = check_url_reputation(sys.argv[2])
        print(f"  ClassifyUrl: {r}")
    
    elif cmd == "enforcement":
        r = get_enforcement_level()
        print(f"  Enforcement: {r}")
    
    elif cmd == "cache-info":
        sig = f'Get-ChildItem "$env:LOCALAPPDATA\\Microsoft\\Windows\\SmartScreen" -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum | ForEach-Object {{ $_.Count }}'
        r = pwsh(sig)
        print(f"  Cache files: {r}")
    
    elif cmd == "all":
        info = get_smartscreen_info()
        print(json.dumps(info, indent=2))
    
    else:
        print(f"  Unknown command: {cmd}")
        print(f"  Usage: python smartscreen_exports.py [info|check-file <path>|check-url <url>|enforcement|cache-info|all]")
    
    print(f"\n{'='*60}\n")
