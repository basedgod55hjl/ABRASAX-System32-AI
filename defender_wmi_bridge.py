#!/usr/bin/env python3
"""
ABRASAX — Defender ML WMI Bridge (Safe Access)
PRIMAL_HEX: 4f5349524953424c58434b | φ: 1.618033988749895
Queries Defender via WMI — NO direct DLL hooks. No tamper trigger.
"""
from __future__ import annotations

import json, os, subprocess, sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

PHI: float = 1.618033988749895
PRIMAL_HEX: str = "4f5349524953424c58434b"
ROOT: Path = Path(r"C:\Users\BASEDGOD\Desktop\ABRASAX")

def query_wmi(cmd: str) -> str:
    try: return subprocess.check_output(cmd, shell=True, text=True, timeout=10).strip()
    except: return ""

def get_defender_status() -> Dict[str, Any]:
    """Get Defender health via WMI — safe query only."""
    r = {"engine": "windows defender", "mpengine_size_mb": 17.5}
    try:
        out = subprocess.check_output(
            'powershell -Command "Get-MpComputerStatus | Select-Object -Property AntivirusEnabled,AMProductVersion,AMEngineVersion,AMServiceEnabled,BehaviorMonitorEnabled,IsTamperProtected,RealTimeProtectionEnabled | ConvertTo-Json"',
            shell=True, text=True, timeout=15
        )
        r["wmi"] = json.loads(out.strip())
        return r
    except Exception as e:
        r["wmi_error"] = str(e)
        return r

def get_defender_threats() -> list:
    """Get Defender threat history via WMI."""
    try:
        out = subprocess.check_output(
            'powershell -Command "Get-MpThreatDetection | Select-Object -First 10 DomainUser,ProcessName,ThreatID,Resources,Severity,InitialDetectionTime | ConvertTo-Json"',
            shell=True, text=True, timeout=15
        )
        data = json.loads(out.strip())
        return data if isinstance(data, list) else [data]
    except:
        return []

def get_defender_mpengine_info() -> Dict[str, Any]:
    """Find and report mpengine.dll metadata — no DLL load."""
    paths = [
        Path(r"C:\ProgramData\Microsoft\Windows Defender\Platform"),
        Path(r"C:\ProgramData\Microsoft\Windows Defender\Definition Updates"),
    ]
    for base in paths:
        if base.exists():
            for f in base.rglob("mpengine.dll"):
                if f.exists():
                    return {
                        "path": str(f),
                        "size_mb": round(f.stat().st_size / (1024*1024), 1),
                        "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                    }
    return {"error": "mpengine.dll not found"}

def check_tamper_protection() -> Dict[str, Any]:
    """Check if tamper protection is on — if yes, ABRASAX must NOT hook Defender."""
    try:
        out = subprocess.check_output(
            'powershell -Command "$t = Get-MpComputerStatus | Select-Object -ExpandProperty IsTamperProtected; if ($t -eq $true) { write-host \'ENABLED\' } else { write-host \'DISABLED\' }"',
            shell=True, text=True, timeout=10
        ).strip()
        return {"tamper_protection": out, "warn": "DANGER: Do NOT hook Defender processes if tamper is enabled" if out == "ENABLED" else "Safe — can read WMI data"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if cmd == "status":
        s = get_defender_status()
        print(json.dumps(s, indent=2))
    elif cmd == "threats":
        t = get_defender_threats()
        print(json.dumps(t[:5], indent=2))
    elif cmd == "mpengine":
        e = get_defender_mpengine_info()
        print(json.dumps(e, indent=2))
    elif cmd == "tamper":
        t = check_tamper_protection()
        print(json.dumps(t, indent=2))
    else:
        s = get_defender_status()
        t = check_tamper_protection()
        e = get_defender_mpengine_info()
        print(f"Defender Status: {s.get('wmi',{}).get('AntivirusEnabled','?')}")
        print(f"Engine Version: {s.get('wmi',{}).get('AMEngineVersion','?')}")
        print(f"Tamper Protect: {t.get('tamper_protection','?')}")
        print(f"mpengine.dll: {e.get('size_mb','?')}MB at {e.get('path','?')}")
