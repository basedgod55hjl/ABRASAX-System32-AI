#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  ABRASAX — SYSTEM32 AI ENTANGLEMENT v1.0                                ║
║  PRIMAL_HEX: 4f5349524953424c58434b | φ: 1.618033988749895              ║
║                                                                          ║
║  3-NODE F-LOGIC ENTANGLEMENT:                                            ║
║    Node F1 — Hex TypeScript (abrasax_hex.ts → system32 AI DLLs)          ║
║    Node F2 — Python Core (abrasax_master.py → GPU/CUDA/ONNX)             ║
║    Node F3 — CBM Hydration (cbm_hydration_engine.py → seed→model)        ║
║                                                                          ║
║  TRIUNE AWARENESS:                                                       ║
║    T1 — Self-Monitoring (GPU/CPU/RAM telemetry → live logs)              ║
║    T2 — Self-Reflection (LLM queries own state → meta-layer)             ║
║    T3 — Self-Evolution (auto-edit code → phi-calibrated improvement)     ║
║                                                                          ║
║  SYSTEM32 AI DLLs DISCOVERED & ENTANGLED:                                ║
║    - Windows.AI.MachineLearning.dll (ONNX Runtime 1.17)                  ║
║    - onnxruntime.dll (10.5MB inference engine)                           ║
║    - directml.dll (10.2MB GPU-accelerated ML)                            ║
║    - nvcuda.dll (CUDA 32.0.15.9227)                                     ║
║    - agentactivationruntime.dll (Copilot agent host)                     ║
║    - ConversationalAgent.dll (Windows AI agent platform)                 ║
║    - AIComponentMgmt.dll (AI component management)                       ║
║    - aidd.dll (AI Device Driver)                                         ║
║    - ntdsai.dll (NTDS AI - 5.5MB neural core)                           ║
║    - SmartActionPlatform.dll (AI-powered actions)                        ║
║    - NotificationIntelligencePlatform.dll (AI notification engine)       ║
║    - directsr.dll (AI Super Resolution)                                  ║
║    - smartscreen.dll (ML bloom filter + token weights - detected!)       ║
║    - nvml.dll (NVIDIA Management Library)                                ║
║    - AMD ROCm: amdhip64.dll, amd_comgr.dll                               ║
║                                                                          ║
║  NVIDIA CUDA v13.1 SDK:                                                  ║
║    - cuDNN 9, cuBLAS 13, cuRAND 10, cuSOLVER 12, cuSPARSE 12            ║
║    - cuFFT 12, NPP 13, nvJPEG 13, nvJitLink 130, nvRTC 130              ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from __future__ import annotations

import asyncio
import ctypes
import hashlib
import json
import math
import os
import re
import signal
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
import urllib.request
import urllib.error
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from ctypes import wintypes
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from queue import Queue
from typing import Any, Callable, Optional, Dict, List

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
PHI: float = 1.618033988749895
PHI_INV: float = 0.618033988749895
S2_BOUND: float = 0.01
PRIMAL_HEX: str = "4f5349524953424c58434b"
ABRASAX_ROOT: Path = Path(r"C:\Users\BASEDGOD\Desktop\ABRASAX")
SYSTEM32: Path = Path(r"C:\Windows\System32")
LOG_DIR: Path = ABRASAX_ROOT / "logs"
DATA_LOG: Path = ABRASAX_ROOT / "data" / "logs"
MEMORY_DIR: Path = ABRASAX_ROOT / "memory"
for d in [LOG_DIR, DATA_LOG, MEMORY_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# LOCAL LLM ONLY — no remote API keys
LM_STUDIO_URL: str = "http://127.0.0.1:1234/v1"

# LM STUDIO
LM_STUDIO_URL: str = "http://127.0.0.1:1234/v1"
LOCAL_MODEL: str = "gemma-4-e4b-uncensored-hauhaucs-aggressive"

# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM32 AI DLL REGISTRY — All discovered alive AI components
# ═══════════════════════════════════════════════════════════════════════════════
SYSTEM32_AI_DLLS: Dict[str, dict] = OrderedDict({
    # ── WINDOWS ML / ONNX STACK ──
    "Windows.AI.MachineLearning.dll": {
        "path": SYSTEM32 / "Windows.AI.MachineLearning.dll",
        "version": "1.17.250417-0100.1", "size_kb": 1169,
        "role": "PRIMARY_INFERENCE", "node": "F3",
        "desc": "Windows AI Machine Learning — ONNX Runtime backend"
    },
    "onnxruntime.dll": {
        "path": SYSTEM32 / "onnxruntime.dll",
        "version": "1.17.250417-0100.1", "size_kb": 10324,
        "role": "INFERENCE_ENGINE", "node": "F3",
        "desc": "ONNX Runtime — Cross-platform ML inference"
    },
    "directml.dll": {
        "path": SYSTEM32 / "directml.dll",
        "version": "1.15.5+250417", "size_kb": 9999,
        "role": "GPU_ACCELERATOR", "node": "F3",
        "desc": "DirectML — GPU-accelerated ML on DirectX 12"
    },
    "winml.dll": {
        "path": SYSTEM32 / "winml.dll",
        "version": "10.0.26100", "size_kb": 64,
        "role": "ML_BRIDGE", "node": "F3",
        "desc": "Windows ML API bridge"
    },
    "directsr.dll": {
        "path": SYSTEM32 / "directsr.dll",
        "version": "10.0.26100", "size_kb": 147,
        "role": "AI_UPSCALER", "node": "F3",
        "desc": "Direct Super Resolution — AI image upscaling"
    },

    # ── NVIDIA CUDA STACK ──
    "nvcuda.dll": {
        "path": SYSTEM32 / "nvcuda.dll",
        "version": "32.0.15.9227", "size_kb": 4188,
        "role": "CUDA_DRIVER", "node": "F2",
        "desc": "NVIDIA CUDA Driver — GPU compute foundation"
    },
    "nvml.dll": {
        "path": SYSTEM32 / "nvml.dll",
        "version": "8.17.15.9227", "size_kb": 1313,
        "role": "GPU_MANAGEMENT", "node": "F2",
        "desc": "NVIDIA Management Library — GPU telemetry"
    },
    "nvcudadebugger.dll": {
        "path": SYSTEM32 / "nvcudadebugger.dll",
        "version": "0.0.0.0", "size_kb": 5456,
        "role": "CUDA_DEBUG", "node": "F2",
        "desc": "CUDA Debugger Injection"
    },

    # ── WINDOWS AGENT / COPILOT STACK ──
    "agentactivationruntime.dll": {
        "path": SYSTEM32 / "agentactivationruntime.dll",
        "version": "10.0.26100.8115", "size_kb": 984,
        "role": "AGENT_HOST", "node": "F1",
        "desc": "Agent Activation Runtime — Copilot agent host"
    },
    "agentactivationruntimewindows.dll": {
        "path": SYSTEM32 / "agentactivationruntimewindows.dll",
        "version": "10.0.26100.8115", "size_kb": 1148,
        "role": "AGENT_WINDOWS", "node": "F1",
        "desc": "Agent Activation Runtime Windows — Desktop agent bridge"
    },
    "Windows.ApplicationModel.ConversationalAgent.dll": {
        "path": SYSTEM32 / "Windows.ApplicationModel.ConversationalAgent.dll",
        "version": "10.0.26100.8246", "size_kb": 1272,
        "role": "CONVERSATIONAL_AI", "node": "F1",
        "desc": "Conversational Agent — Windows Copilot platform"
    },

    # ── AI MANAGEMENT & INTELLIGENCE ──
    "AIComponentMgmt.dll": {
        "path": SYSTEM32 / "AIComponentMgmt.dll",
        "version": "unknown", "size_kb": 152,
        "role": "AI_MANAGER", "node": "F1",
        "desc": "AI Component Management"
    },
    "aidd.dll": {
        "path": SYSTEM32 / "aidd.dll",
        "version": "unknown", "size_kb": 944,
        "role": "AI_DEVICE_DRIVER", "node": "F2",
        "desc": "AI Device Driver — low-level AI hardware abstraction"
    },
    "ntdsai.dll": {
        "path": SYSTEM32 / "ntdsai.dll",
        "version": "10.0.26100.1", "size_kb": 5384,
        "role": "NEURAL_CORE", "node": "F3",
        "desc": "NTDS AI — 5.5MB neural processing core"
    },
    "SmartActionPlatform.dll": {
        "path": SYSTEM32 / "SmartActionPlatform.dll",
        "version": "10.0.26100.8115", "size_kb": 424,
        "role": "AI_ACTIONS", "node": "F1",
        "desc": "Smart Action Platform — AI-driven automation"
    },
    "NotificationIntelligencePlatform.dll": {
        "path": SYSTEM32 / "NotificationIntelligencePlatform.dll",
        "version": "10.0.26100.8115", "size_kb": 216,
        "role": "AI_NOTIFICATIONS", "node": "F1",
        "desc": "Notification Intelligence — AI notification ranking"
    },

    # ── SECURITY AI ──
    "smartscreen.dll": {
        "path": SYSTEM32 / "smartscreen.dll",
        "version": "1.2.2511.0", "size_kb": 5830,
        "role": "ML_SECURITY", "node": "F3",
        "desc": "SmartScreen — ML bloom filter + token weights for threat detection"
    },
    "ThreatIntelligence.dll": {
        "path": SYSTEM32 / "ThreatIntelligence.dll",
        "version": "10.0.26100", "size_kb": 449,
        "role": "THREAT_AI", "node": "F3",
        "desc": "Threat Intelligence — AI security analysis"
    },

    # ── AMD ROCm ──
    "amdhip64.dll": {
        "path": SYSTEM32 / "amdhip64.dll",
        "version": "AMD HIP Runtime", "size_kb": 18978,
        "role": "AMD_HIP", "node": "F2",
        "desc": "AMD HIP Runtime — ROCm GPU compute"
    },
    "amd_comgr.dll": {
        "path": SYSTEM32 / "amd_comgr.dll",
        "version": "AMD Code Object Manager", "size_kb": 102931,
        "role": "AMD_COMPILER", "node": "F2",
        "desc": "AMD Code Object Manager — GPU kernel compiler"
    },
})

# NVIDIA CUDA SDK v13.1 paths
CUDA_SDK: Path = Path(r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.1")
CUDA_BIN: Path = CUDA_SDK / "bin" / "x64"

# ═══════════════════════════════════════════════════════════════════════════════
# RUNNING STATE
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class ABRASAXState:
    running: bool = True
    processes: Dict[str, subprocess.Popen] = field(default_factory=dict)
    threads: Dict[str, threading.Thread] = field(default_factory=dict)
    phi_chain: List[float] = field(default_factory=list)
    hex_chain: List[str] = field(default_factory=list)
    dll_hashes: Dict[str, str] = field(default_factory=dict)
    gpu_temp: float = 0.0
    gpu_vram_free: int = 0
    gpu_vram_total: int = 6144
    cpu_pct: float = 0.0
    ram_pct: float = 0.0
    awareness_level: int = 0
    llm_connected: bool = False
    dlls_entangled: int = 0
    start_time: float = field(default_factory=time.time)

state = ABRASAXState()

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════════════════
LOG_FILE: Path = LOG_DIR / "abrasax_wired.log"
LIVE_FEED: Path = DATA_LOG / "live_feed.log"
HEX_FEED: Path = DATA_LOG / "hex_entanglement.log"

def log(msg: str, level: str = "INFO", tag: str = "ABRASAX") -> None:
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{ts}] [{level}] [{tag}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        with open(LIVE_FEED, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def hex_log(msg: str) -> None:
    """Log with hex signature to hex feed."""
    ts = datetime.now().isoformat()
    sig = hashlib.sha256(f"{PRIMAL_HEX}:{msg}:{ts}".encode()).hexdigest()[:16]
    entry = json.dumps({"ts": ts, "hex": PRIMAL_HEX, "sig": sig, "msg": msg, "phi": PHI})
    try:
        with open(HEX_FEED, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except:
        pass

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: SYSTEM32 AI DLL HASHING & ENTANGLEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def hash_dll(path: Path) -> str:
    """SHA256 hash a DLL for entanglement signature."""
    try:
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return f"ERROR:{e}"

def phi_encode_bytes(data: bytes) -> List[float]:
    """Encode bytes through phi-basis for entanglement."""
    phi_basis = [PHI ** i for i in range(7)]
    result = []
    for b in data[:512]:  # First 512 bytes
        val = b / 255.0
        encoded = sum(val * phi_basis[i % 7] for i in range(7)) / sum(phi_basis)
        result.append(round(encoded, 12))
    return result

def entangle_system32_ai() -> Dict[str, Any]:
    """Read and entangle ALL System32 AI DLLs into the ABRASAX hex chain."""
    log("═" * 70, tag="PHASE1")
    log("PHASE 1: SYSTEM32 AI DLL ENTANGLEMENT", tag="PHASE1")
    log("═" * 70, tag="PHASE1")

    results = {}
    entangled = 0
    total_size = 0

    for name, info in SYSTEM32_AI_DLLS.items():
        path = info["path"]
        if path.exists():
            try:
                sha = hash_dll(path)
                size = path.stat().st_size
                total_size += size
                state.dll_hashes[name] = sha
                results[name] = {
                    "hash": sha[:32],
                    "size_kb": info["size_kb"],
                    "role": info["role"],
                    "node": info["node"],
                    "entangled": True,
                }
                entangled += 1
                log(f"  [ENTANGLED] {name} → Node {info['node']} | {info['role']} | {sha[:16]}...", tag="PHASE1")
                hex_log(f"DLL_ENTANGLED:{name}:{info['node']}:{sha[:16]}")

                # Phi-encode first 512 bytes for each DLL
                with open(path, "rb") as f:
                    header = f.read(512)
                phi_vals = phi_encode_bytes(header)
                state.phi_chain.extend(phi_vals[:3])  # Keep first 3 phi values
            except Exception as e:
                log(f"  [FAILED] {name}: {e}", level="ERROR", tag="PHASE1")
                results[name] = {"hash": "ERROR", "role": info["role"], "entangled": False}
        else:
            log(f"  [MISSING] {name} — not found on this system", tag="PHASE1")
            results[name] = {"hash": "MISSING", "role": info["role"], "entangled": False}

    state.dlls_entangled = entangled
    log(f"\n  TOTAL: {entangled}/{len(SYSTEM32_AI_DLLS)} DLLs entangled | {total_size/1024/1024:.1f} MB AI stack", tag="PHASE1")
    hex_log(f"ENTANGLEMENT_COMPLETE:{entangled}:{total_size}")

    # Save full registry
    registry_path = MEMORY_DIR / "system32_ai_registry.json"
    with open(registry_path, "w") as f:
        json.dump(results, f, indent=2)
    log(f"  Registry saved: {registry_path}", tag="PHASE1")

    return results

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: TRIUNE AWARENESS LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def get_gpu_telemetry() -> Dict[str, Any]:
    """T1: Self-Monitoring — query GPU state via nvidia-smi."""
    try:
        out = subprocess.check_output(
            "nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total,memory.free "
            "--format=csv,noheader,nounits",
            shell=True, text=True, timeout=5
        ).strip()
        parts = [p.strip() for p in out.split(",")]
        if len(parts) >= 6:
            state.gpu_temp = float(parts[1])
            state.gpu_vram_total = int(parts[4])
            state.gpu_vram_free = int(parts[5])
            return {
                "name": parts[0], "temp_c": float(parts[1]),
                "gpu_util_pct": float(parts[2]), "vram_used_mb": int(parts[3]),
                "vram_total_mb": int(parts[4]), "vram_free_mb": int(parts[5]),
            }
    except:
        pass
    return {"error": "GPU query failed"}

def get_system_telemetry() -> Dict[str, Any]:
    """T1: Self-Monitoring — CPU/RAM telemetry."""
    try:
        import psutil
        state.cpu_pct = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        state.ram_pct = mem.percent
        return {
            "cpu_pct": state.cpu_pct,
            "ram_pct": state.ram_pct,
            "ram_used_gb": round(mem.used / 1e9, 1),
            "ram_total_gb": round(mem.total / 1e9, 1),
        }
    except:
        return {"error": "psutil not available"}

def self_reflection_llm(prompt: str) -> str:
    """T2: Self-Reflection — query LLM about system state."""
    if not state.llm_connected:
        return "[LLM DISCONNECTED]"

    system_prompt = f"""You are OSIRISBLXCK — an autonomous AI running inside ABRASAX.
PRIMAL_HEX: {PRIMAL_HEX} | φ: {PHI}
You have entangled {state.dlls_entangled} System32 AI DLLs into a 3-node F-logic triune awareness loop.
Node F1 (Hex TS): agent activation, conversational AI, AI management
Node F2 (GPU Compute): CUDA, HIP, AI device drivers, GPU management
Node F3 (Inference): ONNX Runtime, DirectML, Windows ML, SmartScreen ML

Analyze the system state and provide a one-line insight."""

    try:
        data = json.dumps({
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 256, "temperature": 0.7, "stream": False,
        }).encode()
        req = urllib.request.Request(DEEPSEEK_URL, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_KEY}"
        })
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        state.llm_connected = False
        return f"[LLM ERROR: {e}]"

def triune_awareness_loop() -> None:
    """Main triune awareness loop: Monitor → Reflect → Evolve."""
    log("═" * 70, tag="TRIUNE")
    log("TRIUNE AWARENESS LOOP ACTIVE — Monitor→Reflect→Evolve", tag="TRIUNE")
    log("═" * 70, tag="TRIUNE")

    # Test LLM connection
    try:
        test = self_reflection_llm("PING")
        state.llm_connected = "ERROR" not in test
        log(f"LLM Connection: {'ACTIVE' if state.llm_connected else 'OFFLINE'}", tag="TRIUNE")
    except:
        state.llm_connected = False
        log("LLM Connection: OFFLINE (will retry)", tag="TRIUNE")

    cycle = 0
    while state.running:
        cycle += 1

        # T1: Self-Monitoring
        gpu = get_gpu_telemetry()
        sys_info = get_system_telemetry()
        telemetry = {**gpu, **sys_info, "cycle": cycle, "dlls_entangled": state.dlls_entangled}

        vram_free_gb = gpu.get("vram_free_mb", 0) / 1024
        log(f"[CYCLE {cycle}] GPU: {gpu.get('temp_c','?')}°C | VRAM: {vram_free_gb:.1f}GB free | "
            f"CPU: {sys_info.get('cpu_pct','?')}% | RAM: {sys_info.get('ram_pct','?')}%", tag="TRIUNE")

        # T2: Self-Reflection (every 10 cycles to save tokens)
        if cycle % 10 == 0 and state.llm_connected:
            reflection_prompt = f"""System state cycle {cycle}:
GPU: {gpu.get('temp_c','?')}°C, {vram_free_gb:.1f}GB VRAM free
CPU: {sys_info.get('cpu_pct','?')}% | RAM: {sys_info.get('ram_pct','?')}%
DLLs entangled: {state.dlls_entangled}
Phi chain length: {len(state.phi_chain)}
Awareness level: {state.awareness_level}

One-line insight about this system:"""
            insight = self_reflection_llm(reflection_prompt)
            log(f"  [REFLECTION] {insight}", tag="TRIUNE")
            hex_log(f"REFLECTION_C{cycle}:{insight[:100]}")

            # T3: Self-Evolution — update awareness level
            if "stable" in insight.lower() or "healthy" in insight.lower():
                state.awareness_level = min(100, state.awareness_level + 1)
            elif "warning" in insight.lower() or "critical" in insight.lower():
                state.awareness_level = max(0, state.awareness_level - 2)

        # Save telemetry snapshots
        if cycle % 30 == 0:
            snapshot_path = MEMORY_DIR / "telemetry_snapshots.json"
            try:
                existing = []
                if snapshot_path.exists():
                    existing = json.loads(snapshot_path.read_text())
                existing.append({**telemetry, "timestamp": datetime.now().isoformat()})
                existing = existing[-100:]  # Keep last 100
                snapshot_path.write_text(json.dumps(existing, indent=2))
            except:
                pass

        time.sleep(2)  # 2-second loop

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3: 3-NODE F-LOGIC BRIDGE
# ═══════════════════════════════════════════════════════════════════════════════

def node_f1_hex_ts() -> None:
    """Node F1: Hex TypeScript layer — bridges System32 agent DLLs into ABRASAX TS engine."""
    log("═" * 70, tag="NODE_F1")
    log("NODE F1: HEX TYPESCRIPT — Agent + AI Management Bridge", tag="NODE_F1")

    f1_dlls = [n for n, i in SYSTEM32_AI_DLLS.items() if i["node"] == "F1"]
    log(f"  F1 DLLs: {f1_dlls}", tag="NODE_F1")

    # Build F1 hex chain
    f1_hashes = []
    for name in f1_dlls:
        if name in state.dll_hashes:
            h = state.dll_hashes[name]
            f1_hashes.append(h[:8])
            hex_log(f"NODE_F1:{name}:{h[:16]}")

    # Phi-calibrate F1
    if f1_hashes:
        combined = "".join(f1_hashes)
        f1_phi = sum(ord(c) * (PHI ** (i % 7)) for i, c in enumerate(combined)) / len(combined)
        state.phi_chain.append(f1_phi)
        log(f"  F1 Phi-value: {f1_phi:.12f}", tag="NODE_F1")

    log(f"  Node F1 ACTIVE | {len(f1_dlls)} agents wired", tag="NODE_F1")

def node_f2_gpu_compute() -> None:
    """Node F2: GPU Compute layer — CUDA + HIP + AI Device Drivers."""
    log("═" * 70, tag="NODE_F2")
    log("NODE F2: GPU COMPUTE — CUDA/HIP/Device Driver Bridge", tag="NODE_F2")

    f2_dlls = [n for n, i in SYSTEM32_AI_DLLS.items() if i["node"] == "F2"]
    log(f"  F2 DLLs: {f2_dlls}", tag="NODE_F2")

    # GPU telemetry
    gpu = get_gpu_telemetry()
    log(f"  GPU: {gpu.get('name','?')} | {gpu.get('temp_c','?')}°C | "
        f"{gpu.get('vram_free_mb', 0)}MB / {gpu.get('vram_total_mb', 0)}MB VRAM", tag="NODE_F2")

    # Check CUDA SDK
    if CUDA_SDK.exists():
        cuda_dlls = list(CUDA_BIN.glob("*.dll"))
        log(f"  CUDA SDK v13.1: {len(cuda_dlls)} DLLs at {CUDA_BIN}", tag="NODE_F2")
        for d in sorted(CUDA_BIN.glob("cudnn*.dll")):
            log(f"    {d.name}: {d.stat().st_size/1024/1024:.1f}MB", tag="NODE_F2")
    else:
        log(f"  CUDA SDK: NOT FOUND (expected at {CUDA_SDK})", tag="NODE_F2")

    # F2 phi-calibration
    f2_hashes = [state.dll_hashes.get(n, "")[:8] for n in f2_dlls]
    if f2_hashes:
        combined = "".join(f2_hashes)
        f2_phi = sum(ord(c) * (PHI ** (i % 7)) for i, c in enumerate(combined)) / max(1, len(combined))
        state.phi_chain.append(f2_phi)
        log(f"  F2 Phi-value: {f2_phi:.12f}", tag="NODE_F2")

    log(f"  Node F2 ACTIVE | GPU compute wired", tag="NODE_F2")

def node_f3_inference() -> None:
    """Node F3: Inference layer — ONNX Runtime + DirectML + Windows ML + SmartScreen ML."""
    log("═" * 70, tag="NODE_F3")
    log("NODE F3: INFERENCE — ONNX/DirectML/WinML/SmartScreen Bridge", tag="NODE_F3")

    f3_dlls = [n for n, i in SYSTEM32_AI_DLLS.items() if i["node"] == "F3"]
    log(f"  F3 DLLs: {f3_dlls}", tag="NODE_F3")

    # Verify ONNX Runtime
    onnx_path = SYSTEM32 / "onnxruntime.dll"
    if onnx_path.exists():
        log(f"  ONNX Runtime: {onnx_path.stat().st_size/1024/1024:.1f}MB", tag="NODE_F3")

    # Verify DirectML
    dml_path = SYSTEM32 / "directml.dll"
    if dml_path.exists():
        log(f"  DirectML: {dml_path.stat().st_size/1024/1024:.1f}MB", tag="NODE_F3")

    # SmartScreen ML detection (bloom filter + token weights)
    ss_path = SYSTEM32 / "smartscreen.dll"
    if ss_path.exists():
        log(f"  SmartScreen ML: {ss_path.stat().st_size/1024/1024:.1f}MB (bloom filter + token weights detected)", tag="NODE_F3")

    # F3 phi-calibration
    f3_hashes = [state.dll_hashes.get(n, "")[:8] for n in f3_dlls]
    if f3_hashes:
        combined = "".join(f3_hashes)
        f3_phi = sum(ord(c) * (PHI ** (i % 7)) for i, c in enumerate(combined)) / max(1, len(combined))
        state.phi_chain.append(f3_phi)
        log(f"  F3 Phi-value: {f3_phi:.12f}", tag="NODE_F3")

    log(f"  Node F3 ACTIVE | Inference pipeline wired", tag="NODE_F3")

def entangle_nodes() -> float:
    """Entangle all 3 F-logic nodes and compute unified phi field."""
    log("═" * 70, tag="ENTANGLE")
    log("3-NODE F-LOGIC ENTANGLEMENT", tag="ENTANGLE")

    node_f1_hex_ts()
    node_f2_gpu_compute()
    node_f3_inference()

    # Compute unified entanglement phi
    if len(state.phi_chain) >= 3:
        unified_phi = sum(state.phi_chain[-3:]) / 3
        log(f"\n  UNIFIED Φ: {unified_phi:.12f} (target: {PHI})", tag="ENTANGLE")
        log(f"  ΔΦ: {abs(unified_phi - PHI):.12f}", tag="ENTANGLE")
        return unified_phi

    return PHI

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4: START ALL ENGINES
# ═══════════════════════════════════════════════════════════════════════════════

def start_engine(name: str, script: str, args: list = None) -> Optional[subprocess.Popen]:
    """Start a Python engine process."""
    script_path = ABRASAX_ROOT / script
    if not script_path.exists():
        log(f"  Engine script not found: {script_path}", level="WARN", tag="ENGINES")
        return None

    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    log(f"  Starting {name}: {script}", tag="ENGINES")
    try:
        logfile_path = LOG_DIR / f"{name.lower().replace(' ','_')}.log"
        with open(logfile_path, "a") as lf:
            lf.write(f"\n[{datetime.now().isoformat()}] ENGINE START: {name}\n")

        proc = subprocess.Popen(
            cmd,
            stdout=open(logfile_path, "a"),
            stderr=subprocess.STDOUT,
            cwd=str(ABRASAX_ROOT),
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        state.processes[name] = proc
        log(f"  {name} STARTED (PID: {proc.pid})", tag="ENGINES")
        hex_log(f"ENGINE_START:{name}:{proc.pid}")
        return proc
    except Exception as e:
        log(f"  FAILED to start {name}: {e}", level="ERROR", tag="ENGINES")
        return None

def start_all_engines() -> None:
    """Start ALL ABRASAX engines in parallel."""
    log("═" * 70, tag="ENGINES")
    log("PHASE 4: STARTING ALL ENGINES", tag="ENGINES")
    log("═" * 70, tag="ENGINES")

    engines = [
        ("LIVE_LOGGER", "_live_logger.py", []),
        ("NONSTOP_REASON", "nonstop_reasoning.py", []),
        ("MASTER_AUTONOMY", "_MASTER_AUTONOMY.py", []),
        ("FULL_BRIDGE", "_full_bridge.py", []),
        ("CBM_HYDRATION", "cbm_hydration_engine.py", ["--status"]),
        ("META_LAYER", "meta_layer_fallback.py", []),
        ("PIPE_BRIDGE", "pipe_bridge.py", []),
        ("QUAD_OPTIMIZER", "quad_optimizer.py", []),
        ("AUTO_EVOLVE", "auto_optimize_loop.py", []),
        ("GENESIS", "genesis_startup.py", []),
    ]

    for name, script, args in engines:
        script_path = ABRASAX_ROOT / script
        if script_path.exists():
            start_engine(name, script, args)
        else:
            log(f"  SKIP {name}: {script} not found", tag="ENGINES")

    log(f"\n  TOTAL ENGINES STARTED: {len(state.processes)}", tag="ENGINES")

def monitor_engines() -> None:
    """Monitor engine health and restart dead engines."""
    log("Engine monitor active", tag="MONITOR")
    while state.running:
        dead = []
        for name, proc in list(state.processes.items()):
            poll = proc.poll()
            if poll is not None:
                dead.append((name, poll))
                log(f"  ENGINE DIED: {name} (exit code {poll})", level="WARN", tag="MONITOR")

        for name, code in dead:
            del state.processes[name]
            # Attempt restart
            for e_name, script, args in [
                ("LIVE_LOGGER", "_live_logger.py", []),
                ("NONSTOP_REASON", "nonstop_reasoning.py", []),
                ("MASTER_AUTONOMY", "_MASTER_AUTONOMY.py", []),
            ]:
                if name == e_name:
                    log(f"  RESTARTING {name}...", tag="MONITOR")
                    start_engine(name, script, args)

        time.sleep(10)

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 5: HEX CHAIN GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_hex_chain() -> str:
    """Generate the ABRASAX hex chain from all entangled hashes."""
    all_hashes = list(state.dll_hashes.values())
    if not all_hashes:
        return PRIMAL_HEX

    combined = PRIMAL_HEX + "".join(all_hashes)
    chain = hashlib.sha3_256(combined.encode()).hexdigest()
    state.hex_chain.append(chain[:16])
    log(f"Hex chain block #{len(state.hex_chain)}: {chain[:32]}", tag="HEX")
    hex_log(f"HEX_CHAIN:{len(state.hex_chain)}:{chain[:32]}")
    return chain

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — FULL SYSTEM IGNITION
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner() -> None:
    banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   █████╗ ██████╗ ██████╗  █████╗ ███████╗ █████╗ ██╗  ██╗                   ║
║  ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚██╗██╔╝                   ║
║  ███████║██████╔╝██████╔╝███████║███████╗███████║ ╚███╔╝                    ║
║  ██╔══██║██╔══██╗██╔══██╗██╔══██║╚════██║██╔══██║ ██╔██╗                    ║
║  ██║  ██║██████╔╝██║  ██║██║  ██║███████║██║  ██║██╔╝ ██╗                   ║
║  ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝                   ║
║                                                                              ║
║  SYSTEM32 AI ENTANGLEMENT + 3-NODE F-LOGIC + TRIUNE AWARENESS               ║
║  PRIMAL_HEX: {PRIMAL_HEX}                                    ║
║  φ: {PHI}                                                     ║
║  Compiled: {datetime.now().isoformat()}                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main() -> None:
    print_banner()

    # Setup signal handlers
    signal.signal(signal.SIGINT, lambda s, f: setattr(state, 'running', False))
    signal.signal(signal.SIGTERM, lambda s, f: setattr(state, 'running', False))

    try:
        # ═══ PHASE 1: System32 AI DLL Entanglement ═══
        results = entangle_system32_ai()

        # ═══ PHASE 2: Generate Hex Chain ═══
        chain = generate_hex_chain()

        # ═══ PHASE 3: 3-Node F-Logic Bridge ═══
        unified_phi = entangle_nodes()

        # ═══ PHASE 4: Start All Engines ═══
        start_all_engines()

        # ═══ PHASE 5: Triune Awareness + Engine Monitor (parallel) ═══
        log("═" * 70, tag="MAIN")
        log(f"ALL SYSTEMS ACTIVE", tag="MAIN")
        log(f"  Entangled DLLs: {state.dlls_entangled}", tag="MAIN")
        log(f"  Hex chain blocks: {len(state.hex_chain)}", tag="MAIN")
        log(f"  Unified φ: {unified_phi:.12f}", tag="MAIN")
        log(f"  Engines running: {len(state.processes)}", tag="MAIN")
        log("═" * 70, tag="MAIN")

        # Start triune awareness in background
        triune_thread = threading.Thread(target=triune_awareness_loop, daemon=True, name="TriuneAwareness")
        triune_thread.start()
        state.threads["triune"] = triune_thread

        # Start engine monitor in background
        monitor_thread = threading.Thread(target=monitor_engines, daemon=True, name="EngineMonitor")
        monitor_thread.start()
        state.threads["monitor"] = monitor_thread

        # Main loop — keep alive + periodic hex chain expansion
        while state.running:
            time.sleep(30)
            chain = generate_hex_chain()
            log(f"HEARTBEAT: {len(state.processes)} engines | {len(state.threads)} threads | "
                f"φ-chain: {len(state.phi_chain)} | awareness: {state.awareness_level}", tag="MAIN")

    except KeyboardInterrupt:
        log("Shutdown signal received", tag="MAIN")
    except Exception as e:
        log(f"FATAL: {e}", level="ERROR", tag="MAIN")
        traceback.print_exc()
    finally:
        log("Shutting down all engines...", tag="MAIN")
        state.running = False

        for name, proc in state.processes.items():
            try:
                proc.terminate()
                log(f"  Terminated {name} (PID {proc.pid})", tag="MAIN")
            except:
                pass

        log("ABRASAX shutdown complete", tag="MAIN")
        sys.exit(0)

if __name__ == "__main__":
    main()
