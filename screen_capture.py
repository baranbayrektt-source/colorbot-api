"""
Ekran görüntüsü alma modülü
Bu modül, gerçek zamanlı ekran görüntüsü alma işlemlerini yönetir.
"""

import cv2
import numpy as np
import pyautogui
import time
from threading import Thread, Lock
from typing import Optional, Tuple, Dict, Any


class ScreenCapture:
    """Ekran görüntüsü alma ve işleme sınıfı"""
    
    def __init__(self, region: Optional[Dict[str, int]] = None):
        """
        ScreenCapture sınıfını başlatır
        
        Args:
            region: Yakalanacak ekran bölgesi {'top': y, 'left': x, 'width': w, 'height': h}
                   None ise tam ekran yakalanır
        """
        # PyAutoGUI ayarları
        pyautogui.FAILSAFE = False  # Failsafe'i devre dışı bırak
        pyautogui.PAUSE = 0  # Delay'i sıfırla
        
        self.region = region or self._get_full_screen_region()
        self.latest_frame = None
        self.frame_lock = Lock()
        self.is_capturing = False
        self.capture_thread = None
        self.fps = 20  # Hedeflenen FPS (BALANCED for smoothness)
        self.frame_time = 1.0 / self.fps
        self.frame_skip_counter = 0
        
    def _get_full_screen_region(self) -> Dict[str, int]:
        """Tam ekran bölgesini döndürür"""
        screen_width, screen_height = pyautogui.size()
        return {
            'top': 0,
            'left': 0,
            'width': screen_width,
            'height': screen_height
        }
    
    def set_capture_region(self, x: int, y: int, width: int, height: int):
        """Yakalama bölgesini ayarlar"""
        self.region = {
            'top': y,
            'left': x,
            'width': width,
            'height': height
        }
    
    def get_screenshot(self) -> Optional[np.ndarray]:
        """Tek bir ekran görüntüsü alır"""
        try:
            # PyAutoGUI ile screenshot al
            if self.region['left'] == 0 and self.region['top'] == 0:
                # Tam ekran
                screenshot = pyautogui.screenshot()
            else:
                # Belirli bölge
                screenshot = pyautogui.screenshot(
                    region=(
                        self.region['left'], 
                        self.region['top'], 
                        self.region['width'], 
                        self.region['height']
                    )
                )
            
            # PIL Image'ı OpenCV formatına çevir
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return frame
        except Exception as e:
            print(f"Screenshot alma hatası: {e}")
            return None
    
    def _capture_loop(self):
        """Sürekli ekran yakalama döngüsü (thread'de çalışır)"""
        while self.is_capturing:
            start_time = time.time()
            
            frame = self.get_screenshot()
            if frame is not None:
                with self.frame_lock:
                    self.latest_frame = frame.copy()
            
            # FPS kontrolü
            elapsed_time = time.time() - start_time
            sleep_time = max(0, self.frame_time - elapsed_time)
            time.sleep(sleep_time)
    
    def start_continuous_capture(self):
        """Sürekli yakalama başlatır"""
        if not self.is_capturing:
            self.is_capturing = True
            self.capture_thread = Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            print("Sürekli ekran yakalama başlatıldı")
    
    def stop_continuous_capture(self):
        """Sürekli yakalamayı durdurur"""
        if self.is_capturing:
            self.is_capturing = False
            if self.capture_thread:
                self.capture_thread.join(timeout=1.0)
            # Silent stop - no message
    
    def get_latest_frame(self) -> Optional[np.ndarray]:
        """En son yakalanan frame'i döndürür"""
        with self.frame_lock:
            return self.latest_frame.copy() if self.latest_frame is not None else None
    
    def get_region_info(self) -> Dict[str, int]:
        """Mevcut yakalama bölgesi bilgilerini döndürür"""
        return self.region.copy()
    
    def set_fps(self, fps: int):
        """Hedef FPS'i ayarlar"""
        self.fps = max(1, min(fps, 120))  # 1-120 FPS arası sınırla
        self.frame_time = 1.0 / self.fps
        print(f"Hedef FPS: {self.fps} olarak ayarlandı")


class RegionSelector:
    """Ekran bölgesi seçimi için yardımcı sınıf"""
    
    @staticmethod
    def select_region_interactive() -> Optional[Dict[str, int]]:
        """
        Kullanıcıdan interaktif olarak bölge seçmesini ister
        Returns: Seçilen bölge koordinatları veya None
        """
        print("Bölge seçimi için talimatlar:")
        print("1. Açılacak pencerede fare ile başlangıç noktasını tıklayın")
        print("2. Sürükleyerek bitiş noktasını belirleyin")
        print("3. Fare tuşunu bırakın")
        print("4. ESC tuşuna basarak çıkın")
        
        # Tam ekran screenshot al
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Seçim değişkenleri
        selecting = False
        start_point = None
        end_point = None
        current_frame = frame.copy()
        
        def mouse_callback(event, x, y, flags, param):
            nonlocal selecting, start_point, end_point, current_frame
            
            if event == cv2.EVENT_LBUTTONDOWN:
                selecting = True
                start_point = (x, y)
                end_point = (x, y)
            
            elif event == cv2.EVENT_MOUSEMOVE and selecting:
                end_point = (x, y)
                current_frame = frame.copy()
                cv2.rectangle(current_frame, start_point, end_point, (0, 255, 0), 2)
            
            elif event == cv2.EVENT_LBUTTONUP:
                selecting = False
                end_point = (x, y)
        
        cv2.namedWindow('Bölge Seçimi', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('Bölge Seçimi', mouse_callback)
        
        while True:
            cv2.imshow('Bölge Seçimi', current_frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC tuşu
                break
        
        cv2.destroyAllWindows()
        
        if start_point and end_point:
            # Koordinatları düzenle
            x1, y1 = start_point
            x2, y2 = end_point
            
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            if width > 10 and height > 10:  # Minimum boyut kontrolü
                return {
                    'left': left,
                    'top': top,
                    'width': width,
                    'height': height
                }
        
        return None


def test_screen_capture():
    """Test fonksiyonu"""
    print("Ekran yakalama testi başlatılıyor...")
    
    # ScreenCapture oluştur
    capture = ScreenCapture()
    
    # Tek screenshot test
    frame = capture.get_screenshot()
    if frame is not None:
        print(f"Screenshot alındı: {frame.shape}")
        # Test için küçük bir pencerede göster
        small_frame = cv2.resize(frame, (800, 600))
        cv2.imshow('Test Screenshot', small_frame)
        cv2.waitKey(2000)  # 2 saniye göster
        cv2.destroyAllWindows()
    
    # Sürekli yakalama testi
    print("Sürekli yakalama testi (5 saniye)...")
    capture.start_continuous_capture()
    
    start_time = time.time()
    while time.time() - start_time < 5:
        frame = capture.get_latest_frame()
        if frame is not None:
            small_frame = cv2.resize(frame, (400, 300))
            cv2.imshow('Continuous Capture', small_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        time.sleep(0.01)
    
    capture.stop_continuous_capture()
    cv2.destroyAllWindows()
    print("Test tamamlandı!")


if __name__ == "__main__":
    test_screen_capture()