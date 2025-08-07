"""
Renk tespiti ve hedef bulma modülü
Bu modül, ekran görüntüsünde belirli renkleri tespit eder ve hedefleri bulur.
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional, Any
import json
import os


class ColorRange:
    """Renk aralığını temsil eden sınıf"""
    
    def __init__(self, name: str, lower_hsv: Tuple[int, int, int], upper_hsv: Tuple[int, int, int]):
        self.name = name
        self.lower_hsv = np.array(lower_hsv)
        self.upper_hsv = np.array(upper_hsv)
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'lower_hsv': self.lower_hsv.tolist(),
            'upper_hsv': self.upper_hsv.tolist()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ColorRange':
        return cls(data['name'], tuple(data['lower_hsv']), tuple(data['upper_hsv']))


class TargetDetector:
    """Hedef tespit ve takip sınıfı"""
    
    def __init__(self):
        self.color_ranges = self._load_default_colors()
        self.active_colors = []  # Aktif olarak aranacak renkler
        self.min_contour_area = 100  # Minimum kontur alanı
        self.max_contour_area = 50000  # Maksimum kontur alanı
        self.target_history = []  # Hedef geçmişi (smoothing için)
        self.history_size = 5
        self.config_file = "color_config.json"
    
    def _load_default_colors(self) -> List[ColorRange]:
        """Varsayılan renk aralıklarını yükler"""
        default_colors = [
            # Red (enemy color)
            ColorRange("Red", (0, 100, 100), (10, 255, 255)),
            ColorRange("Red2", (170, 100, 100), (180, 255, 255)),
            
            # Yellow (enemy highlight)
            ColorRange("Yellow", (20, 100, 100), (30, 255, 255)),
            
            # Orange (enemy emphasis)
            ColorRange("Orange", (10, 100, 100), (20, 255, 255)),
            
            # Purple (enemy outline)
            ColorRange("Purple", (130, 100, 100), (160, 255, 255)),
            
            # Pink (health bar)
            ColorRange("Pink", (160, 100, 100), (170, 255, 255)),
            
            # White (name tags)
            ColorRange("White", (0, 0, 200), (180, 30, 255)),
        ]
        return default_colors
    
    def add_color_range(self, name: str, lower_hsv: Tuple[int, int, int], upper_hsv: Tuple[int, int, int]):
        """Yeni renk aralığı ekler"""
        color_range = ColorRange(name, lower_hsv, upper_hsv)
        self.color_ranges.append(color_range)
        self.save_color_config()
    
    def remove_color_range(self, name: str):
        """Renk aralığını kaldırır"""
        self.color_ranges = [cr for cr in self.color_ranges if cr.name != name]
        self.save_color_config()
    
    def set_active_colors(self, color_names: List[str]):
        """Aktif renkleri ayarlar"""
        self.active_colors = [cr for cr in self.color_ranges if cr.name in color_names]
        print(f"Aktif renkler: {[cr.name for cr in self.active_colors]}")
    
    def save_color_config(self):
        """Renk ayarlarını dosyaya kaydeder"""
        try:
            config_data = {
                'color_ranges': [cr.to_dict() for cr in self.color_ranges],
                'min_contour_area': self.min_contour_area,
                'max_contour_area': self.max_contour_area
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Config kaydetme hatası: {e}")
    
    def load_color_config(self):
        """Renk ayarlarını dosyadan yükler"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                self.color_ranges = [ColorRange.from_dict(cr) for cr in config_data.get('color_ranges', [])]
                self.min_contour_area = config_data.get('min_contour_area', 100)
                self.max_contour_area = config_data.get('max_contour_area', 50000)
                print("Renk ayarları yüklendi")
            else:
                print("Config dosyası bulunamadı, varsayılan ayarlar kullanılıyor")
        except Exception as e:
            print(f"Config yükleme hatası: {e}")
            self.color_ranges = self._load_default_colors()
    
    def detect_targets(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Frame'de hedefleri tespit eder
        
        Args:
            frame: Analiz edilecek görüntü
            
        Returns:
            Tespit edilen hedeflerin listesi [{'center': (x, y), 'area': int, 'color': str, 'confidence': float}]
        """
        if frame is None or len(self.active_colors) == 0:
            return []
        
        # HSV formatına çevir
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        all_targets = []
        
        for color_range in self.active_colors:
            targets = self._detect_color_targets(hsv, color_range)
            all_targets.extend(targets)
        
        # Overlapping hedefleri birleştir
        merged_targets = self._merge_overlapping_targets(all_targets)
        
        # Güvenilirlik skoruna göre sırala
        merged_targets.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Geçmişe ekle (smoothing için)
        self._update_target_history(merged_targets)
        
        return merged_targets
    
    def set_active_colors(self, color_names: List[str]):
        """Aktif renkleri ayarlar"""
        self.active_colors = [cr for cr in self.color_ranges if cr.name in color_names]
    
    def _detect_color_targets(self, hsv: np.ndarray, color_range: ColorRange) -> List[Dict[str, Any]]:
        """Belirli bir renk için hedefleri tespit eder"""
        # Renk maskesi oluştur
        mask = cv2.inRange(hsv, color_range.lower_hsv, color_range.upper_hsv)
        
        # Gürültüyü azalt
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Konturları bul
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        targets = []
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Alan filtresi
            if self.min_contour_area <= area <= self.max_contour_area:
                # Hedef merkezi hesapla
                M = cv2.moments(contour)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    
                    # Bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Aspect ratio kontrolü (çok uzun/dar objeleri filtrele)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    if 0.3 <= aspect_ratio <= 3.0:  # Makul aspect ratio
                        # Güvenilirlik skoru hesapla
                        confidence = self._calculate_confidence(area, aspect_ratio, contour)
                        
                        targets.append({
                            'center': (cx, cy),
                            'area': area,
                            'color': color_range.name,
                            'confidence': confidence,
                            'bounding_box': (x, y, w, h),
                            'contour': contour
                        })
        
        return targets
    
    def _calculate_confidence(self, area: float, aspect_ratio: float, contour) -> float:
        """Hedef güvenilirlik skorunu hesaplar"""
        # Temel confidence (alan bazlı)
        area_score = min(area / 1000.0, 1.0)  # 0-1 arası normalize et
        
        # Aspect ratio skoru (1'e yakın olan daha iyi)
        aspect_score = 1.0 - abs(1.0 - aspect_ratio) / 2.0
        aspect_score = max(0.1, aspect_score)
        
        # Şekil compactness (daire benzeri şekiller daha iyi)
        perimeter = cv2.arcLength(contour, True)
        if perimeter > 0:
            compactness = 4 * np.pi * area / (perimeter * perimeter)
            compactness_score = min(compactness, 1.0)
        else:
            compactness_score = 0.0
        
        # Toplam confidence skoru
        confidence = (area_score * 0.4 + aspect_score * 0.3 + compactness_score * 0.3)
        return min(confidence, 1.0)
    
    def _merge_overlapping_targets(self, targets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Üst üste binen hedefleri birleştirir"""
        if len(targets) <= 1:
            return targets
        
        merged = []
        used = set()
        
        for i, target1 in enumerate(targets):
            if i in used:
                continue
            
            # Bu hedefle overlapping olan diğer hedefleri bul
            group = [target1]
            used.add(i)
            
            for j, target2 in enumerate(targets[i+1:], i+1):
                if j in used:
                    continue
                
                if self._targets_overlap(target1, target2):
                    group.append(target2)
                    used.add(j)
            
            # Grup içindeki hedefleri birleştir
            if len(group) == 1:
                merged.append(group[0])
            else:
                merged_target = self._merge_target_group(group)
                merged.append(merged_target)
        
        return merged
    
    def _targets_overlap(self, target1: Dict[str, Any], target2: Dict[str, Any], threshold: float = 50.0) -> bool:
        """İki hedefin üst üste binip binmediğini kontrol eder"""
        x1, y1 = target1['center']
        x2, y2 = target2['center']
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance < threshold
    
    def _merge_target_group(self, group: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Hedef grubunu tek hedefe birleştirir"""
        # En yüksek confidence'a sahip olanın özelliklerini kullan
        best_target = max(group, key=lambda x: x['confidence'])
        
        # Merkezi ağırlıklı ortalama al
        total_weight = sum(t['confidence'] for t in group)
        if total_weight > 0:
            weighted_x = sum(t['center'][0] * t['confidence'] for t in group) / total_weight
            weighted_y = sum(t['center'][1] * t['confidence'] for t in group) / total_weight
            
            best_target['center'] = (int(weighted_x), int(weighted_y))
            best_target['confidence'] = min(total_weight / len(group), 1.0)
        
        return best_target
    
    def _update_target_history(self, targets: List[Dict[str, Any]]):
        """Hedef geçmişini günceller (smoothing için)"""
        self.target_history.append(targets)
        if len(self.target_history) > self.history_size:
            self.target_history.pop(0)
    
    def get_smoothed_target(self) -> Optional[Dict[str, Any]]:
        """Geçmiş verilere dayalı smooth edilmiş en iyi hedefi döndürür"""
        if not self.target_history:
            return None
        
        # Son birkaç frame'deki en tutarlı hedefi bul
        all_recent_targets = []
        for frame_targets in self.target_history[-3:]:  # Son 3 frame
            all_recent_targets.extend(frame_targets)
        
        if not all_recent_targets:
            return None
        
        # En yüksek confidence'a sahip hedefi döndür
        return max(all_recent_targets, key=lambda x: x['confidence'])
    
    def draw_targets(self, frame: np.ndarray, targets: List[Dict[str, Any]]) -> np.ndarray:
        """Hedefleri frame üzerine çizer"""
        result_frame = frame.copy()
        
        for i, target in enumerate(targets):
            center = target['center']
            color_name = target['color']
            confidence = target['confidence']
            bounding_box = target.get('bounding_box')
            
            # Renk seç (confidence'a göre)
            color = (0, 255, 0) if confidence > 0.7 else (0, 255, 255) if confidence > 0.4 else (0, 0, 255)
            
            # Merkez noktası
            cv2.circle(result_frame, center, 5, color, -1)
            cv2.circle(result_frame, center, 15, color, 2)
            
            # Bounding box
            if bounding_box:
                x, y, w, h = bounding_box
                cv2.rectangle(result_frame, (x, y), (x + w, y + h), color, 2)
            
            # Bilgi metni
            text = f"{color_name} ({confidence:.2f})"
            cv2.putText(result_frame, text, (center[0] + 20, center[1] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Hedef numarası
            cv2.putText(result_frame, str(i + 1), (center[0] - 5, center[1] + 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return result_frame


class ColorPicker:
    """Renk seçme yardımcısı"""
    
    @staticmethod
    def pick_color_from_image(image_path: str) -> Optional[ColorRange]:
        """Görüntüden renk seçer"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Mouse callback için değişkenler
            picked_colors = []
            
            def mouse_callback(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    hsv_color = hsv[y, x]
                    picked_colors.append(hsv_color)
                    print(f"Seçilen HSV: {hsv_color}")
            
            cv2.namedWindow('Renk Seçici')
            cv2.setMouseCallback('Renk Seçici', mouse_callback)
            
            print("Renk seçmek için görüntüye tıklayın, ESC ile çıkın")
            
            while True:
                cv2.imshow('Renk Seçici', img)
                if cv2.waitKey(1) & 0xFF == 27:  # ESC
                    break
            
            cv2.destroyAllWindows()
            
            if picked_colors:
                # Seçilen renklerin ortalamasını al
                avg_hsv = np.mean(picked_colors, axis=0).astype(int)
                
                # Tolerans aralığı oluştur
                tolerance = np.array([10, 50, 50])
                lower = np.maximum(avg_hsv - tolerance, [0, 0, 0])
                upper = np.minimum(avg_hsv + tolerance, [179, 255, 255])
                
                color_name = f"Özel_Renk_{len(picked_colors)}"
                return ColorRange(color_name, tuple(lower), tuple(upper))
            
            return None
            
        except Exception as e:
            print(f"Renk seçme hatası: {e}")
            return None


def test_color_detection():
    """Renk tespit sistemi test fonksiyonu"""
    print("Renk tespit sistemi test ediliyor...")
    
    detector = TargetDetector()
    detector.set_active_colors(["Kırmızı", "Sarı", "Kırmızı2"])
    
    # Test için örnek renk matrisi oluştur
    test_img = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Kırmızı daire
    cv2.circle(test_img, (150, 150), 30, (0, 0, 255), -1)
    
    # Sarı kare
    cv2.rectangle(test_img, (300, 100), (400, 200), (0, 255, 255), -1)
    
    # Yeşil daire (tespit edilmemeli)
    cv2.circle(test_img, (450, 300), 25, (0, 255, 0), -1)
    
    # Hedefleri tespit et
    targets = detector.detect_targets(test_img)
    
    print(f"{len(targets)} hedef tespit edildi:")
    for i, target in enumerate(targets):
        print(f"  {i+1}. {target['color']} - Merkez: {target['center']}, Güvenilirlik: {target['confidence']:.2f}")
    
    # Sonucu göster
    result_img = detector.draw_targets(test_img, targets)
    cv2.imshow('Renk Tespit Testi', result_img)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    
    print("Test tamamlandı!")


if __name__ == "__main__":
    test_color_detection()