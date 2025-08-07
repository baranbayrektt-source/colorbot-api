"""
Gelişmiş tuş yakalama sistemi
Gerçek zamanlı tuş algılama ve atama
"""

import time
from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button
from threading import Thread, Event
from typing import Optional, Union, Set, List


class KeyCapture:
    """Tuş yakalama sınıfı"""
    
    def __init__(self):
        self.captured_key = None
        self.capture_event = Event()
        self.is_capturing = False
        self.keyboard_listener = None
        self.mouse_listener = None
    
    def capture_key(self, timeout: float = 10.0) -> Optional[str]:
        """
        Kullanıcıdan tuş basmasını bekler ve yakalanan tuşu döndürür
        
        Args:
            timeout: Bekleme süresi (saniye)
            
        Returns:
            Yakalanan tuş adı veya None
        """
        self.captured_key = None
        self.capture_event.clear()
        self.is_capturing = True
        
        print("Select key...")
        
        # Dinleyicileri başlat
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=None
        )
        
        self.mouse_listener = mouse.Listener(
            on_click=self._on_mouse_click
        )
        
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
        # Tuş basılmasını bekle
        captured = self.capture_event.wait(timeout=timeout)
        
        # Dinleyicileri durdur
        self.is_capturing = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
        
        if captured and self.captured_key:
            print(f"✅ Yakalanan tuş: {self.captured_key}")
            return self.captured_key
        else:
            print("⏰ Zaman aşımı - Tuş yakalanamadı")
            return None
    
    def _on_key_press(self, key):
        """Klavye tuşu basma olayı"""
        if not self.is_capturing:
            return
        
        try:
            key_name = self._format_key_name(key)
            if key_name:
                self.captured_key = key_name
                self.capture_event.set()
        except Exception:
            pass
    
    def _on_mouse_click(self, x, y, button, pressed):
        """Fare tıklama olayı"""
        if not self.is_capturing or not pressed:
            return
        
        try:
            button_name = self._format_mouse_button(button)
            if button_name:
                self.captured_key = button_name
                self.capture_event.set()
        except Exception:
            pass
    
    def _format_key_name(self, key) -> Optional[str]:
        """Tuş objesini string'e çevirir"""
        try:
            if isinstance(key, Key):
                # Özel tuşlar
                key_map = {
                    Key.f1: "f1", Key.f2: "f2", Key.f3: "f3", Key.f4: "f4",
                    Key.f5: "f5", Key.f6: "f6", Key.f7: "f7", Key.f8: "f8",
                    Key.f9: "f9", Key.f10: "f10", Key.f11: "f11", Key.f12: "f12",
                    Key.ctrl_l: "ctrl_left", Key.ctrl_r: "ctrl_right",
                    Key.alt_l: "alt_left", Key.alt_r: "alt_right",
                    Key.shift_l: "shift_left", Key.shift_r: "shift_right",
                    Key.space: "space", Key.enter: "enter", Key.esc: "escape",
                    Key.tab: "tab", Key.caps_lock: "caps_lock",
                    Key.up: "arrow_up", Key.down: "arrow_down",
                    Key.left: "arrow_left", Key.right: "arrow_right",
                    Key.home: "home", Key.end: "end",
                    Key.page_up: "page_up", Key.page_down: "page_down",
                    Key.insert: "insert", Key.delete: "delete",
                    Key.backspace: "backspace"
                }
                return key_map.get(key, str(key).replace('Key.', ''))
            
            elif isinstance(key, KeyCode):
                # Normal karakterler
                if key.char and key.char.isprintable():
                    return key.char.lower()
                elif key.vk:  # Virtual key code
                    return f"vk_{key.vk}"
            
            return None
            
        except Exception:
            return None
    
    def _format_mouse_button(self, button) -> Optional[str]:
        """Fare düğmesini string'e çevirir"""
        button_map = {
            Button.left: "mouse_left",
            Button.right: "mouse_right", 
            Button.middle: "mouse_middle"
        }
        return button_map.get(button, None)
    
    @staticmethod
    def get_key_description(key_name: str) -> str:
        """Tuş adından açıklama döndürür"""
        descriptions = {
            "mouse_left": "Sol Fare Düğmesi",
            "mouse_right": "Sağ Fare Düğmesi", 
            "mouse_middle": "Orta Fare Düğmesi",
            "f1": "F1", "f2": "F2", "f3": "F3", "f4": "F4",
            "f5": "F5", "f6": "F6", "f7": "F7", "f8": "F8",
            "f9": "F9", "f10": "F10", "f11": "F11", "f12": "F12",
            "ctrl_left": "Sol Ctrl", "ctrl_right": "Sağ Ctrl",
            "alt_left": "Sol Alt", "alt_right": "Sağ Alt",
            "shift_left": "Sol Shift", "shift_right": "Sağ Shift",
            "space": "Boşluk", "enter": "Enter", "escape": "Esc",
            "tab": "Tab", "caps_lock": "Caps Lock"
        }
        
        return descriptions.get(key_name, key_name.upper())


class KeyValidator:
    """Tuş doğrulama sınıfı"""
    
    @staticmethod
    def is_valid_key(key_name: str) -> bool:
        """Tuşun geçerli olup olmadığını kontrol eder"""
        if not key_name:
            return False
        
        # Yasaklı tuşlar (sistem tuşları)
        forbidden = [
            "ctrl_left", "ctrl_right", "alt_left", "alt_right",
            "cmd", "cmd_left", "cmd_right", "super", "meta"
        ]
        
        if key_name.lower() in forbidden:
            return False
        
        return True
    
    @staticmethod
    def get_safe_keys() -> List[str]:
        """Güvenli tuş önerilerini döndürür"""
        return [
            "f1", "f2", "f3", "f4", "f5", "f6",
            "mouse_left", "mouse_right", "mouse_middle",
            "space", "x", "c", "v", "b", "n", "m"
        ]


def test_key_capture():
    """Tuş yakalama test fonksiyonu"""
    print("🎮 Tuş Yakalama Testi")
    print("=" * 30)
    
    capture = KeyCapture()
    
    for i in range(3):
        print(f"\n🔄 Test {i+1}/3")
        key = capture.capture_key(timeout=5.0)
        
        if key:
            desc = KeyCapture.get_key_description(key)
            valid = KeyValidator.is_valid_key(key)
            print(f"   Tuş: {key}")
            print(f"   Açıklama: {desc}")
            print(f"   Geçerli: {'✅' if valid else '❌'}")
        else:
            print("   ❌ Tuş yakalanamadı")
    
    print("\n🎉 Test tamamlandı!")


if __name__ == "__main__":
    test_key_capture()