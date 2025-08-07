"""
Otomatik fare kontrolü ve nişan alma sistemi
Bu modül, tespit edilen hedeflere otomatik nişan alma işlemlerini gerçekleştirir.
"""

import pyautogui
import time
import math
import numpy as np
import os
from typing import Tuple, Optional, Dict, Any, List
from threading import Thread, Lock
import json


class MouseController:
    """Fare kontrolü ve nişan alma sınıfı"""
    
    def __init__(self):
        # PyAutoGUI ayarları
        pyautogui.FAILSAFE = True  # Köşeye fare götürürse dur
        pyautogui.PAUSE = 0.01  # İşlemler arası bekleme
        
        # Nişan alma ayarları
        self.sensitivity = 1.0  # Hareket hassasiyeti
        self.smoothing = 0.3  # Hareket yumuşaklığı (0-1)
        self.aim_speed = 5.0  # Nişan alma hızı
        self.max_movement_per_step = 50  # Adım başına maksimum hareket
        
        # Güvenlik ayarları
        self.screen_bounds_margin = 10  # Ekran kenarlarından uzak dur
        self.max_distance_per_move = 200  # Tek harekette maksimum mesafe
        
        # Durum takibi
        self.is_aiming = False
        self.last_target_position = None
        self.aim_lock = Lock()
        
        # İstatistikler
        self.total_moves = 0
        self.successful_aims = 0
        
        # Ekran bilgileri
        self.screen_width, self.screen_height = pyautogui.size()
        self.screen_center = (self.screen_width // 2, self.screen_height // 2)
        
        # Ayar dosyası
        self.config_file = "mouse_config.json"
        self.load_config()
    
    def load_config(self):
        """Fare ayarlarını dosyadan yükler"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                self.sensitivity = config.get('sensitivity', 1.0)
                self.smoothing = config.get('smoothing', 0.3)
                self.aim_speed = config.get('aim_speed', 5.0)
                self.max_movement_per_step = config.get('max_movement_per_step', 50)
                print("Fare ayarları yüklendi")
        except Exception as e:
            print(f"Fare config yükleme hatası: {e}")
    
    def save_config(self):
        """Fare ayarlarını dosyaya kaydeder"""
        try:
            config = {
                'sensitivity': self.sensitivity,
                'smoothing': self.smoothing,
                'aim_speed': self.aim_speed,
                'max_movement_per_step': self.max_movement_per_step
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Fare config kaydetme hatası: {e}")
    
    def get_current_mouse_position(self) -> Tuple[int, int]:
        """Mevcut fare konumunu döndürür"""
        return pyautogui.position()
    
    def calculate_movement_vector(self, current_pos: Tuple[int, int], target_pos: Tuple[int, int]) -> Tuple[float, float]:
        """Hareket vektörünü hesaplar"""
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        
        # Mesafeyi hesapla
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            return (0, 0)
        
        # Hız kontrolü
        if distance > self.max_distance_per_move:
            # Çok uzaksa, adım adım git
            scale = self.max_distance_per_move / distance
            dx *= scale
            dy *= scale
        
        # Hassasiyet uygula
        dx *= self.sensitivity
        dy *= self.sensitivity
        
        return (dx, dy)
    
    def smooth_movement(self, current_pos: Tuple[int, int], target_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Yumuşak hareket için ara noktalar oluşturur"""
        dx, dy = self.calculate_movement_vector(current_pos, target_pos)
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < 5:  # Çok yakınsa direkt git
            return [target_pos]
        
        # Adım sayısını hesapla
        steps = max(1, int(distance / self.max_movement_per_step))
        steps = min(steps, 10)  # Maksimum 10 adım
        
        # Ara noktaları oluştur
        points = []
        for i in range(1, steps + 1):
            progress = i / steps
            # Ease-out easing function
            progress = 1 - (1 - progress) ** 2
            
            x = current_pos[0] + dx * progress
            y = current_pos[1] + dy * progress
            points.append((int(x), int(y)))
        
        return points
    
    def is_position_safe(self, pos: Tuple[int, int]) -> bool:
        """Pozisyonun güvenli olup olmadığını kontrol eder"""
        x, y = pos
        margin = self.screen_bounds_margin
        
        return (margin <= x <= self.screen_width - margin and 
                margin <= y <= self.screen_height - margin)
    
    def move_to_target(self, target_pos: Tuple[int, int], smooth: bool = True) -> bool:
        """Hedefe fare imlecini hareket ettirir"""
        try:
            with self.aim_lock:
                current_pos = self.get_current_mouse_position()
                
                # Güvenlik kontrolü
                if not self.is_position_safe(target_pos):
                    print(f"Hedef pozisyon güvenli değil: {target_pos}")
                    return False
                
                if smooth and self.smoothing > 0:
                    # Yumuşak hareket
                    points = self.smooth_movement(current_pos, target_pos)
                    
                    for point in points:
                        if not self.is_aiming:  # İptal edildi mi?
                            return False
                        
                        pyautogui.moveTo(point[0], point[1])
                        time.sleep(self.smoothing / len(points))
                else:
                    # Direkt hareket
                    pyautogui.moveTo(target_pos[0], target_pos[1])
                
                self.total_moves += 1
                self.last_target_position = target_pos
                return True
                
        except Exception as e:
            print(f"Fare hareket hatası: {e}")
            return False
    
    def aim_at_target(self, target: Dict[str, Any]) -> bool:
        """Hedefe nişan alır"""
        if not target or 'center' not in target:
            return False
        
        target_pos = target['center']
        confidence = target.get('confidence', 0.0)
        
        # Düşük güvenilirlik skorunu filtrele
        if confidence < 0.3:
            return False
        
        # Hareket hesapla ve uygula
        success = self.move_to_target(target_pos, smooth=True)
        
        if success:
            self.successful_aims += 1
        
        return success
    
    def start_continuous_aim(self, target_generator):
        """Sürekli nişan alma modunu başlatır"""
        self.is_aiming = True
        
        def aim_loop():
            while self.is_aiming:
                try:
                    target = next(target_generator, None)
                    if target:
                        self.aim_at_target(target)
                    time.sleep(0.01)  # CPU kullanımını azalt
                except Exception as e:
                    print(f"Sürekli nişan alma hatası: {e}")
                    break
        
        aim_thread = Thread(target=aim_loop, daemon=True)
        aim_thread.start()
        return aim_thread
    
    def stop_aiming(self):
        """Nişan almayı durdurur"""
        self.is_aiming = False
    
    def perform_click(self, button: str = 'left', clicks: int = 1) -> bool:
        """Fare tıklaması gerçekleştirir"""
        try:
            pyautogui.click(button=button, clicks=clicks)
            return True
        except Exception as e:
            print(f"Tıklama hatası: {e}")
            return False
    
    def perform_drag(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float = 0.1) -> bool:
        """Sürükleme işlemi gerçekleştirir"""
        try:
            pyautogui.dragTo(end_pos[0], end_pos[1], duration=duration, button='left')
            return True
        except Exception as e:
            print(f"Sürükleme hatası: {e}")
            return False
    
    def set_sensitivity(self, sensitivity: float):
        """Hassasiyeti ayarlar"""
        self.sensitivity = max(0.1, min(sensitivity, 5.0))
        self.save_config()
    
    def set_smoothing(self, smoothing: float):
        """Yumuşaklığı ayarlar"""
        self.smoothing = max(0.0, min(smoothing, 1.0))
        self.save_config()
    
    def set_aim_speed(self, speed: float):
        """Nişan alma hızını ayarlar"""
        self.aim_speed = max(0.1, min(speed, 20.0))
        self.save_config()
    
    def get_statistics(self) -> Dict[str, Any]:
        """İstatistikleri döndürür"""
        accuracy = (self.successful_aims / self.total_moves * 100) if self.total_moves > 0 else 0
        
        return {
            'total_moves': self.total_moves,
            'successful_aims': self.successful_aims,
            'accuracy': accuracy,
            'current_position': self.get_current_mouse_position(),
            'last_target': self.last_target_position,
            'is_aiming': self.is_aiming
        }
    
    def reset_statistics(self):
        """İstatistikleri sıfırlar"""
        self.total_moves = 0
        self.successful_aims = 0
    
    def calibrate_sensitivity(self, test_distance: int = 100) -> float:
        """Otomatik hassasiyet kalibrasyonu"""
        print("Hassasiyet kalibrasyonu başlatılıyor...")
        
        # Test noktaları oluştur
        center = self.screen_center
        test_points = [
            (center[0] + test_distance, center[1]),
            (center[0], center[1] + test_distance),
            (center[0] - test_distance, center[1]),
            (center[0], center[1] - test_distance)
        ]
        
        # Merkeze git
        pyautogui.moveTo(center[0], center[1])
        time.sleep(0.5)
        
        total_error = 0
        test_count = 0
        
        for target in test_points:
            if not self.is_position_safe(target):
                continue
            
            start_pos = self.get_current_mouse_position()
            self.move_to_target(target, smooth=False)
            time.sleep(0.1)
            
            actual_pos = self.get_current_mouse_position()
            error = math.sqrt((actual_pos[0] - target[0])**2 + (actual_pos[1] - target[1])**2)
            total_error += error
            test_count += 1
            
            # Merkeze geri dön
            pyautogui.moveTo(center[0], center[1])
            time.sleep(0.2)
        
        if test_count > 0:
            avg_error = total_error / test_count
            # Hassasiyeti hata oranına göre ayarla
            if avg_error > 10:
                self.sensitivity *= 1.2
            elif avg_error < 3:
                self.sensitivity *= 0.9
            
            self.save_config()
            print(f"Kalibrasyon tamamlandı. Ortalama hata: {avg_error:.1f}px, Yeni hassasiyet: {self.sensitivity:.2f}")
            return avg_error
        
        return -1


class AimAssist:
    """Nişan alma yardımcısı - üst seviye kontrol"""
    
    def __init__(self):
        self.mouse_controller = MouseController()
        self.aim_modes = {
            'closest': self._get_closest_target,
            'highest_confidence': self._get_highest_confidence_target,
            'center_priority': self._get_center_priority_target
        }
        self.current_mode = 'highest_confidence'
        self.aim_offset = (0, 0)  # Nişan ofset (headshot için)
        self.auto_fire = False
        self.fire_delay = 0.1  # Otomatik ateş gecikmesi
        
    def set_aim_mode(self, mode: str):
        """Nişan alma modunu ayarlar"""
        if mode in self.aim_modes:
            self.current_mode = mode
            print(f"Nişan modu: {mode}")
    
    def set_aim_offset(self, x_offset: int, y_offset: int):
        """Nişan ofset ayarlar (headshot için yukarı kaydırma)"""
        self.aim_offset = (x_offset, y_offset)
    
    def _get_closest_target(self, targets: List[Dict[str, Any]], current_pos: Tuple[int, int]) -> Optional[Dict[str, Any]]:
        """En yakın hedefi döndürür"""
        if not targets:
            return None
        
        closest_target = None
        min_distance = float('inf')
        
        for target in targets:
            target_pos = target['center']
            distance = math.sqrt((target_pos[0] - current_pos[0])**2 + (target_pos[1] - current_pos[1])**2)
            
            if distance < min_distance:
                min_distance = distance
                closest_target = target
        
        return closest_target
    
    def _get_highest_confidence_target(self, targets: List[Dict[str, Any]], current_pos: Tuple[int, int]) -> Optional[Dict[str, Any]]:
        """En yüksek güvenilirlik skoruna sahip hedefi döndürür"""
        if not targets:
            return None
        
        return max(targets, key=lambda x: x.get('confidence', 0))
    
    def _get_center_priority_target(self, targets: List[Dict[str, Any]], current_pos: Tuple[int, int]) -> Optional[Dict[str, Any]]:
        """Ekran merkezine en yakın + yüksek confidence hedefi döndürür"""
        if not targets:
            return None
        
        screen_center = self.mouse_controller.screen_center
        
        best_target = None
        best_score = -1
        
        for target in targets:
            target_pos = target['center']
            confidence = target.get('confidence', 0)
            
            # Merkeze uzaklık
            center_distance = math.sqrt((target_pos[0] - screen_center[0])**2 + (target_pos[1] - screen_center[1])**2)
            center_score = max(0, 1 - center_distance / 500)  # 500px'den sonra skor düşer
            
            # Kombine skor
            combined_score = confidence * 0.7 + center_score * 0.3
            
            if combined_score > best_score:
                best_score = combined_score
                best_target = target
        
        return best_target
    
    def select_target(self, targets: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Mevcut moda göre hedef seçer"""
        if not targets:
            return None
        
        current_pos = self.mouse_controller.get_current_mouse_position()
        target_selector = self.aim_modes.get(self.current_mode, self._get_highest_confidence_target)
        
        selected_target = target_selector(targets, current_pos)
        
        # Ofset uygula
        if selected_target and self.aim_offset != (0, 0):
            center = selected_target['center']
            new_center = (center[0] + self.aim_offset[0], center[1] + self.aim_offset[1])
            selected_target = selected_target.copy()
            selected_target['center'] = new_center
        
        return selected_target
    
    def aim_and_fire(self, targets: List[Dict[str, Any]]) -> bool:
        """Hedefe nişan alır ve isteğe bağlı ateş eder"""
        target = self.select_target(targets)
        if not target:
            return False
        
        # Nişan al
        aim_success = self.mouse_controller.aim_at_target(target)
        
        # Otomatik ateş
        if aim_success and self.auto_fire:
            time.sleep(self.fire_delay)
            self.mouse_controller.perform_click()
        
        return aim_success
    
    def set_auto_fire(self, enabled: bool, delay: float = 0.1):
        """Otomatik ateş ayarları"""
        self.auto_fire = enabled
        self.fire_delay = max(0.01, delay)


def test_mouse_control():
    """Fare kontrolü test fonksiyonu"""
    print("Fare kontrolü test ediliyor...")
    
    controller = MouseController()
    
    # Mevcut pozisyonu al
    current = controller.get_current_mouse_position()
    print(f"Mevcut pozisyon: {current}")
    
    # Test hedefleri
    screen_center = controller.screen_center
    test_targets = [
        (screen_center[0] + 100, screen_center[1]),
        (screen_center[0], screen_center[1] + 100),
        (screen_center[0] - 100, screen_center[1]),
        (screen_center[0], screen_center[1] - 100)
    ]
    
    print("Test hareketleri başlatılıyor...")
    
    for i, target in enumerate(test_targets):
        print(f"Hedef {i+1}: {target}")
        success = controller.move_to_target(target)
        print(f"Hareket {'başarılı' if success else 'başarısız'}")
        time.sleep(1)
    
    # Merkeze geri dön
    controller.move_to_target(screen_center)
    
    # İstatistikleri göster
    stats = controller.get_statistics()
    print(f"İstatistikler: {stats}")
    
    print("Test tamamlandı!")


if __name__ == "__main__":
    test_mouse_control()