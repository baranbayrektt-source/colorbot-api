import os
import sys
import time
import ctypes
import psutil
import threading
import hashlib
import winreg
import subprocess
from typing import List, Optional, Dict, Any
import tempfile
import random

class RealSecurityManager:
    def __init__(self):
        self.is_protected = False
        self.monitoring_threads = []
        
        # REAL threat processes - EXTENDED VANGUARD DETECTION
        self.threat_processes = {
            'vanguard': ['vgc.exe', 'vgtray.exe', 'vanguard.exe', 'vgk.sys', 'vgc.sys'],
            'valorant': ['VALORANT.exe', 'VALORANT-Win64-Shipping.exe', 'RiotClientServices.exe'],
            'riot': ['RiotClient.exe', 'LeagueClient.exe', 'LeagueClientUx.exe'],
            'eac': ['EasyAntiCheat.exe', 'EACService.exe'],
            'battleye': ['BEService.exe', 'BEDaisy.exe', 'BattlEye.exe'],
            'faceit': ['faceitservice.exe', 'FACEITApp.exe'],
            'debugging': ['cheatengine.exe', 'x64dbg.exe', 'ollydbg.exe', 'procmon.exe'],
            'analysis': ['wireshark.exe', 'fiddler.exe', 'procexp.exe', 'procmon.exe']
        }
        
        self.legitimate_names = [
            "Windows Audio Device Graph Isolation",
            "Desktop Window Manager",
            "Windows Security Health Service",
            "Microsoft Edge WebView2",
            "Windows Update Medic Service"
        ]
        
        self.allocated_memory = []
