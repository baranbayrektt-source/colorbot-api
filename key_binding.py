"""
Tuş atama ve aktivasyon sistemi
Bu modül, kullanıcı girişlerini dinler ve nişan alma sistemini kontrol eder.
"""

import time
import json
import os
from typing import Callable, Dict, Any, Optional, Set
from threading import Thread, Lock, Event
from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode, Listener as KeyboardListener
from pynput.mouse import Button, Listener as MouseListener
import logging


class KeyBinding:
    """Tuş atama sınıfı"""
    
    def __init__(self):
        # Dinleyiciler
        self.keyboard_listener = None
        self.mouse_listener = None
        
        # Durum kontrolü
        self.is_listening = False
        self.is_active = False  # Aimbot aktif mi?
        self.listener_lock = Lock()
        
        # Tuş atamaları
        self.activation_keys = set()  # Aktivasyon tuşları
        self.toggle_key = None  # Toggle tuşu
        self.config_key = None  # Ayar menüsü tuşu
        self.exit_key = None  # Çıkış tuşu
        
        # Callback fonksiyonları
        self.on_activate = None  # Aktivasyon callback'i
        self.on_deactivate = None  # Deaktivasyon callback'i
        self.on_toggle = None  # Toggle callback'i
        self.on_config = None  # Config callback'i
        self.on_exit = None  # Exit callback'i
        
        # Tuş durumu
        self.pressed_keys = set()
        self.mouse_pressed = set()
        
        # Ayarlar
        self.config_file = "key_config.json"
        self.hold_mode = True  # True: basılı tutma, False: toggle
        
        # Logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Varsayılan tuş atamaları
        self._set_default_keys()
        self.load_config()
    
    def _set_default_keys(self):
        """Varsayılan tuş atamalarını ayarlar"""
        # Varsayılan olarak sol fare düğmesi + Alt
        self.activation_keys = {Button.left, Key.alt_l}
        self.toggle_key = Key.f1
        self.config_key = Key.f2
        self.exit_key = Key.f12
    
    def load_config(self):
        """Tuş ayarlarını dosyadan yükler"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Tuş atamalarını yükle
                self._load_keys_from_config(config)
                self.hold_mode = config.get('hold_mode', True)
                
                self.logger.info("Tuş ayarları yüklendi")
        except Exception as e:
            self.logger.error(f"Config yükleme hatası: {e}")
            self._set_default_keys()
    
    def save_config(self):
        """Tuş ayarlarını dosyaya kaydeder"""
        try:
            config = {
                'activation_keys': self._keys_to_config(self.activation_keys),
                'toggle_key': self._key_to_config(self.toggle_key),
                'config_key': self._key_to_config(self.config_key),
                'exit_key': self._key_to_config(self.exit_key),
                'hold_mode': self.hold_mode
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.logger.info("Tuş ayarları kaydedildi")
        except Exception as e:
            self.logger.error(f"Config kaydetme hatası: {e}")
    
    def _keys_to_config(self, keys: Set) -> list:
        """Tuş setini config formatına çevirir"""
        config_keys = []
        for key in keys:
            config_keys.append(self._key_to_config(key))
        return config_keys
    
    def _key_to_config(self, key) -> Dict[str, Any]:
        """Tek tuşu config formatına çevirir"""
        if key is None:
            return None
        
        if isinstance(key, Key):
            return {'type': 'special', 'name': key.name}
        elif isinstance(key, KeyCode):
            return {'type': 'char', 'char': key.char}
        elif isinstance(key, Button):
            return {'type': 'mouse', 'name': key.name}
        else:
            return {'type': 'unknown', 'value': str(key)}
    
    def _load_keys_from_config(self, config: Dict[str, Any]):
        """Config'den tuş atamalarını yükler"""
        # Aktivasyon tuşları
        activation_config = config.get('activation_keys', [])
        self.activation_keys = set()
        for key_config in activation_config:
            key = self._config_to_key(key_config)
            if key:
                self.activation_keys.add(key)
        
        # Diğer tuşlar
        self.toggle_key = self._config_to_key(config.get('toggle_key'))
        self.config_key = self._config_to_key(config.get('config_key'))
        self.exit_key = self._config_to_key(config.get('exit_key'))
    
    def _config_to_key(self, config):
        """Config formatından tuşa çevirir"""
        if not config:
            return None
        
        key_type = config.get('type')
        
        if key_type == 'special':
            return getattr(Key, config['name'], None)
        elif key_type == 'char':
            return KeyCode.from_char(config['char'])
        elif key_type == 'mouse':
            return getattr(Button, config['name'], None)
        
        return None
    
    def set_activation_keys(self, keys: Set):
        """Aktivasyon tuşlarını ayarlar"""
        self.activation_keys = set(keys)
        self.save_config()
    
    def set_activation_key(self, key_string: str):
        """Tek aktivasyon tuşu ayarlar (string formatında)"""
        key = self._string_to_key(key_string)
        if key:
            self.activation_keys = {key}
            self.save_config()
    
    def set_exit_key(self, key_string: str):
        """Çıkış tuşunu ayarlar (string formatında)"""
        key = self._string_to_key(key_string)
        if key:
            self.exit_key = key
            self.save_config()
    
    def _string_to_key(self, key_string: str):
        """String formatındaki tuşu pynput formatına çevirir"""
        key_string = key_string.lower()
        
        # Fare tuşları
        if key_string == "mouse_left":
            return Button.left
        elif key_string == "mouse_right":
            return Button.right
        elif key_string == "mouse_middle":
            return Button.middle
        
        # F tuşları
        elif key_string.startswith("f") and key_string[1:].isdigit():
            f_num = int(key_string[1:])
            if 1 <= f_num <= 12:
                return getattr(Key, f"f{f_num}", None)
        
        # Özel tuşlar
        elif key_string == "space":
            return Key.space
        elif key_string == "enter":
            return Key.enter
        elif key_string == "ctrl":
            return Key.ctrl_l
        elif key_string == "alt":
            return Key.alt_l
        elif key_string == "shift":
            return Key.shift_l
        
        # Normal karakterler
        elif len(key_string) == 1 and key_string.isalpha():
            return KeyCode.from_char(key_string)
        
        return None
    
    def set_toggle_key(self, key):
        """Toggle tuşunu ayarlar"""
        self.toggle_key = key
        self.save_config()
    
    def set_hold_mode(self, hold_mode: bool):
        """Mod ayarlar (True: basılı tutma, False: toggle)"""
        self.hold_mode = hold_mode
        self.save_config()
    
    def set_callbacks(self, 
                     on_activate: Optional[Callable] = None,
                     on_deactivate: Optional[Callable] = None,
                     on_toggle: Optional[Callable] = None,
                     on_config: Optional[Callable] = None,
                     on_exit: Optional[Callable] = None):
        """Callback fonksiyonlarını ayarlar"""
        if on_activate:
            self.on_activate = on_activate
        if on_deactivate:
            self.on_deactivate = on_deactivate
        if on_toggle:
            self.on_toggle = on_toggle
        if on_config:
            self.on_config = on_config
        if on_exit:
            self.on_exit = on_exit
    
    def _check_activation_keys(self) -> bool:
        """Aktivasyon tuşlarının basılı olup olmadığını kontrol eder"""
        if not self.activation_keys:
            return False
        
        all_keys = self.pressed_keys.union(self.mouse_pressed)
        return self.activation_keys.issubset(all_keys)
    
    def _on_key_press(self, key):
        """Klavye tuşu basma olayı"""
        try:
            self.pressed_keys.add(key)
            
            # Toggle tuşu kontrolü
            if key == self.toggle_key and self.toggle_key:
                if self.on_toggle:
                    self.on_toggle()
                return
            
            # Config tuşu kontrolü
            if key == self.config_key and self.config_key:
                if self.on_config:
                    self.on_config()
                return
            
            # Exit tuşu kontrolü
            if key == self.exit_key and self.exit_key:
                if self.on_exit:
                    self.on_exit()
                return
            
            # Aktivasyon kontrolü (hold mode için)
            if self.hold_mode and self._check_activation_keys():
                if not self.is_active:
                    self.is_active = True
                    if self.on_activate:
                        self.on_activate()
        
        except Exception as e:
            self.logger.error(f"Key press error: {e}")
    
    def _on_key_release(self, key):
        """Klavye tuşu bırakma olayı"""
        try:
            self.pressed_keys.discard(key)
            
            # Aktivasyon kontrolü (hold mode için)
            if self.hold_mode and self.is_active:
                if not self._check_activation_keys():
                    self.is_active = False
                    if self.on_deactivate:
                        self.on_deactivate()
        
        except Exception as e:
            self.logger.error(f"Key release error: {e}")
    
    def _on_mouse_press(self, x, y, button, pressed):
        """Fare düğmesi basma olayı"""
        try:
            if pressed:
                self.mouse_pressed.add(button)
                
                # Aktivasyon kontrolü (hold mode için)
                if self.hold_mode and self._check_activation_keys():
                    if not self.is_active:
                        self.is_active = True
                        if self.on_activate:
                            self.on_activate()
            else:
                self.mouse_pressed.discard(button)
                
                # Aktivasyon kontrolü (hold mode için)
                if self.hold_mode and self.is_active:
                    if not self._check_activation_keys():
                        self.is_active = False
                        if self.on_deactivate:
                            self.on_deactivate()
        
        except Exception as e:
            self.logger.error(f"Mouse event error: {e}")
    
    def start_listening(self):
        """Tuş dinlemeyi başlatır"""
        with self.listener_lock:
            if self.is_listening:
                return
            
            try:
                # Klavye dinleyicisi
                self.keyboard_listener = KeyboardListener(
                    on_press=self._on_key_press,
                    on_release=self._on_key_release
                )
                
                # Fare dinleyicisi
                self.mouse_listener = MouseListener(
                    on_click=self._on_mouse_press
                )
                
                # Dinleyicileri başlat
                self.keyboard_listener.start()
                self.mouse_listener.start()
                
                self.is_listening = True
                self.logger.info("Tuş dinleme başlatıldı")
                
            except Exception as e:
                self.logger.error(f"Dinleme başlatma hatası: {e}")
    
    def stop_listening(self):
        """Tuş dinlemeyi durdurur"""
        with self.listener_lock:
            if not self.is_listening:
                return
            
            try:
                if self.keyboard_listener:
                    self.keyboard_listener.stop()
                    self.keyboard_listener = None
                
                if self.mouse_listener:
                    self.mouse_listener.stop()
                    self.mouse_listener = None
                
                self.is_listening = False
                self.is_active = False
                self.pressed_keys.clear()
                self.mouse_pressed.clear()
                
                self.logger.info("Tuş dinleme durduruldu")
                
            except Exception as e:
                self.logger.error(f"Dinleme durdurma hatası: {e}")
    
    def is_aimbot_active(self) -> bool:
        """Aimbot'un aktif olup olmadığını döndürür"""
        return self.is_active
    
    def manual_activate(self):
        """Manuel aktivasyon (toggle mode için)"""
        if not self.hold_mode:
            self.is_active = not self.is_active
            if self.is_active and self.on_activate:
                self.on_activate()
            elif not self.is_active and self.on_deactivate:
                self.on_deactivate()
    
    def get_key_description(self, key) -> str:
        """Tuş açıklamasını döndürür"""
        if key is None:
            return "Atanmamış"
        
        if isinstance(key, Key):
            key_names = {
                Key.ctrl_l: "Sol Ctrl",
                Key.ctrl_r: "Sağ Ctrl",
                Key.alt_l: "Sol Alt",
                Key.alt_r: "Sağ Alt",
                Key.shift_l: "Sol Shift",
                Key.shift_r: "Sağ Shift",
                Key.space: "Boşluk",
                Key.enter: "Enter",
                Key.esc: "Esc",
                Key.tab: "Tab",
                Key.f1: "F1", Key.f2: "F2", Key.f3: "F3", Key.f4: "F4",
                Key.f5: "F5", Key.f6: "F6", Key.f7: "F7", Key.f8: "F8",
                Key.f9: "F9", Key.f10: "F10", Key.f11: "F11", Key.f12: "F12"
            }
            return key_names.get(key, str(key).replace('Key.', '').title())
        
        elif isinstance(key, KeyCode):
            return f"'{key.char}'" if key.char else str(key)
        
        elif isinstance(key, Button):
            button_names = {
                Button.left: "Sol Fare",
                Button.right: "Sağ Fare",
                Button.middle: "Orta Fare"
            }
            return button_names.get(key, str(key).replace('Button.', '').title())
        
        return str(key)
    
    def get_activation_description(self) -> str:
        """Aktivasyon tuşlarının açıklamasını döndürür"""
        if not self.activation_keys:
            return "Atanmamış"
        
        descriptions = [self.get_key_description(key) for key in self.activation_keys]
        return " + ".join(descriptions)
    
    def get_status_info(self) -> Dict[str, Any]:
        """Durum bilgilerini döndürür"""
        return {
            'is_listening': self.is_listening,
            'is_active': self.is_active,
            'hold_mode': self.hold_mode,
            'activation_keys': self.get_activation_description(),
            'toggle_key': self.get_key_description(self.toggle_key),
            'config_key': self.get_key_description(self.config_key),
            'exit_key': self.get_key_description(self.exit_key),
            'pressed_keys': len(self.pressed_keys),
            'mouse_pressed': len(self.mouse_pressed)
        }


class KeyRecorder:
    """Tuş kaydedici - yeni tuş atamaları için"""
    
    def __init__(self):
        self.recorded_keys = set()
        self.is_recording = False
        self.listener = None
        self.timeout = 5.0  # 5 saniye timeout
        self.record_event = Event()
    
    def start_recording(self, timeout: float = 5.0) -> Set:
        """Tuş kaydını başlatır ve belirlenen süre bekler"""
        self.timeout = timeout
        self.recorded_keys.clear()
        self.is_recording = True
        self.record_event.clear()
        
        def on_key_press(key):
            if self.is_recording:
                self.recorded_keys.add(key)
                self.record_event.set()
        
        def on_mouse_click(x, y, button, pressed):
            if self.is_recording and pressed:
                self.recorded_keys.add(button)
                self.record_event.set()
        
        # Dinleyicileri başlat
        keyboard_listener = KeyboardListener(on_press=on_key_press)
        mouse_listener = MouseListener(on_click=on_mouse_click)
        
        keyboard_listener.start()
        mouse_listener.start()
        
        # Tuş basılmasını bekle
        self.record_event.wait(timeout=timeout)
        
        # Dinleyicileri durdur
        keyboard_listener.stop()
        mouse_listener.stop()
        
        self.is_recording = False
        return self.recorded_keys.copy()


def test_key_binding():
    """Tuş atama sistemi test fonksiyonu"""
    print("Tuş atama sistemi test ediliyor...")
    
    # Test callback fonksiyonları
    def on_activate():
        print("🎯 AIMBOT AKTİF!")
    
    def on_deactivate():
        print("⏹️ Aimbot deaktif")
    
    def on_toggle():
        print("🔄 Toggle işlemi")
    
    def on_config():
        print("⚙️ Ayarlar menüsü")
    
    def on_exit():
        print("🚪 Çıkış")
        return False  # Test döngüsünü durdur
    
    # KeyBinding oluştur
    key_binding = KeyBinding()
    key_binding.set_callbacks(
        on_activate=on_activate,
        on_deactivate=on_deactivate,
        on_toggle=on_toggle,
        on_config=on_config,
        on_exit=on_exit
    )
    
    # Dinlemeyi başlat
    key_binding.start_listening()
    
    print("Test başlatıldı!")
    print(f"Aktivasyon: {key_binding.get_activation_description()}")
    print(f"Toggle: {key_binding.get_key_description(key_binding.toggle_key)}")
    print(f"Ayarlar: {key_binding.get_key_description(key_binding.config_key)}")
    print(f"Çıkış: {key_binding.get_key_description(key_binding.exit_key)}")
    print("Tuşlara basarak test edin. Çıkmak için F12'ye basın.")
    
    # Test döngüsü
    try:
        while True:
            time.sleep(0.1)
            
            # Durum bilgilerini göster
            if key_binding.is_aimbot_active():
                print(".", end="", flush=True)
            
    except KeyboardInterrupt:
        print("\\nTest sonlandırılıyor...")
    
    finally:
        key_binding.stop_listening()
        print("Test tamamlandı!")


if __name__ == "__main__":
    test_key_binding()