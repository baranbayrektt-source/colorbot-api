"""
🔥 QUARXV1 Final Stealth System
F12 SADECE CONSOLE AÇ/KAPAT - HİÇBİR ŞEY DEVRE DIŞI KALMAZ
"""

import os
import sys
import time
import ctypes
import threading
from ctypes import wintypes
import keyboard

class FinalStealthManager:
    """Final console stealth sistemi - SADECE CONSOLE TOGGLE"""
    
    def __init__(self):
        self.console_visible = True
        self.last_activity = time.time()
        self.stealth_thread = None
        self.keyboard_thread = None
        self.running = False
        self.auto_hide_delay = 20.0  # 20 saniye sonra gizle
        
        # Windows API functions
        self.kernel32 = ctypes.windll.kernel32
        self.user32 = ctypes.windll.user32
        
        # Get console window handle
        self.console_hwnd = self.kernel32.GetConsoleWindow()
        
    def start_stealth_monitoring(self):
        """Stealth monitoring başlat"""
        if self.running:
            return
            
        self.running = True
        
        # Start keyboard monitoring thread
        self.keyboard_thread = threading.Thread(target=self._keyboard_monitor, daemon=True)
        self.keyboard_thread.start()
        
        # Start auto-hide monitoring thread
        self.stealth_thread = threading.Thread(target=self._stealth_monitor, daemon=True)
        self.stealth_thread.start()
        
        print("👻 Final stealth system active")
        print("🔧 F12 to toggle console (ONLY CONSOLE - NOTHING ELSE)")
        print("⏰ Auto-hide after 5 seconds of inactivity") 
        print()
    
    def _keyboard_monitor(self):
        """Basit keyboard monitoring - sadece F12"""
        try:
            while self.running:
                try:
                    # F12 tuşunu dinle
                    if keyboard.is_pressed('f12'):
                        # Debounce - aynı tuşa çok hızlı basılmasını önle
                        time.sleep(0.2)
                        if keyboard.is_pressed('f12'):  # Hala basılı mı?
                            continue
                        
                        # Console toggle - SADECE BU!
                        self.toggle_console()
                        
                        # Kısa bekleme
                        time.sleep(0.5)
                    
                    time.sleep(0.1)
                    
                except Exception:
                    time.sleep(0.5)
                    
        except Exception as e:
            pass
    
    def _stealth_monitor(self):
        """Ana stealth monitoring loop"""
        while self.running:
            try:
                # Auto-hide after inactivity (SILENT - no messages)
                if self.console_visible and (time.time() - self.last_activity) > self.auto_hide_delay:
                    self.hide_console_silent()
                
                time.sleep(2.0)
                
            except Exception:
                time.sleep(1.0)
    
    def toggle_console(self):
        """Console görünürlüğünü değiştir - SADECE BU İŞLEM"""
        try:
            if self.console_visible:
                self.hide_console()
            else:
                self.show_console()
        except Exception:
            pass
    
    def hide_console(self):
        """Console'u gizle (F12 manual hide)"""
        if not self.console_visible:
            return
            
        try:
            # Hide console window
            self.user32.ShowWindow(self.console_hwnd, 0)  # SW_HIDE
            self.console_visible = False
            
        except Exception as e:
            pass
    
    def hide_console_silent(self):
        """Console'u sessizce gizle (auto-hide)"""
        if not self.console_visible:
            return
            
        try:
            # Hide console window silently
            self.user32.ShowWindow(self.console_hwnd, 0)  # SW_HIDE
            self.console_visible = False
            
        except Exception as e:
            pass
    
    def show_console(self):
        """Console'u göster"""
        if self.console_visible:
            return
            
        try:
            # Show console window
            self.user32.ShowWindow(self.console_hwnd, 1)  # SW_SHOWNORMAL
            
            # Bring to front
            self.user32.SetForegroundWindow(self.console_hwnd)
            
            self.console_visible = True
            self.last_activity = time.time()
            
            # Console revealed silently - no messages
            
        except Exception as e:
            pass
    
    def update_activity(self):
        """Aktivite zamanını güncelle"""
        self.last_activity = time.time()
        if not self.console_visible:
            self.show_console()
    
    def stop_stealth_monitoring(self):
        """Stealth monitoring'i durdur"""
        self.running = False
        
        # Stop threads
        if self.keyboard_thread and self.keyboard_thread.is_alive():
            self.keyboard_thread.join(timeout=1.0)
            
        if self.stealth_thread and self.stealth_thread.is_alive():
            self.stealth_thread.join(timeout=1.0)
        
        # Make sure console is visible when stopping
        if not self.console_visible:
            self.show_console()
    
    def emergency_hide(self):
        """Acil durum console gizleme"""
        self.hide_console()

# Global instance
final_stealth = FinalStealthManager()

def start_final_stealth():
    """Final stealth sistemini başlat"""
    final_stealth.start_stealth_monitoring()

def stop_final_stealth():
    """Final stealth sistemini durdur"""
    final_stealth.stop_stealth_monitoring()

def update_final_activity():
    """Final stealth aktivitesini güncelle"""
    final_stealth.update_activity()

def emergency_hide_final():
    """Acil console gizleme"""
    final_stealth.emergency_hide()

def show_console_final():
    """Manuel console gösterme"""
    final_stealth.show_console()