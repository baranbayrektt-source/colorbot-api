#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ColorBot License System
Güvenli lisans kontrolü ve yönetimi
"""

import sqlite3
import hashlib
import requests
import json
import os
import time
import random
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import threading

class LicenseSystem:
    """ColorBot lisans sistemi"""
    
    def __init__(self):
        self.db_path = "license_database.db"
        self.api_url = "https://colorbot-api.vercel.app/api"  # Vercel API
        self.api_key = "QUARX_API_SECRET_2024"  # API güvenlik anahtarı
        self.license_key = None
        self.license_data = None
        self.is_valid = False
        self.expiry_date = None
        self.license_type = None
        
        # Local cache
        self.cache_file = "license_cache.json"
        self.cache_duration = 300  # 5 dakika
        
        # API connection settings
        self.api_timeout = 10  # 10 saniye timeout
        self.retry_attempts = 3  # 3 deneme
        
        # Initialize database
        self.init_database()
    
    def init_database(self):
        """Veritabanını başlat"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Licenses tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS licenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT UNIQUE NOT NULL,
                    license_type TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    expiry_date TEXT NOT NULL,
                    is_used INTEGER DEFAULT 0,
                    used_by TEXT,
                    generated_by TEXT DEFAULT 'admin',
                    price REAL DEFAULT 0.0,
                    hardware_id TEXT,
                    last_check TEXT
                )
            ''')
            
            # Users tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    email TEXT,
                    license_key TEXT,
                    created_date TEXT,
                    expiry_date TEXT,
                    is_active INTEGER DEFAULT 1,
                    last_login TEXT,
                    login_count INTEGER DEFAULT 0,
                    hardware_id TEXT,
                    ip_address TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Veritabanı başlatma hatası: {e}")
    
    def generate_license_key(self) -> str:
        """25 haneli güvenli lisans anahtarı üret"""
        while True:
            # QUA-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX formatında
            chars = string.ascii_uppercase + string.digits
            key_parts = [
                ''.join(random.choice(chars) for _ in range(4))
                for _ in range(6)
            ]
            key = f"QUA-{key_parts[0]}-{key_parts[1]}-{key_parts[2]}-{key_parts[3]}-{key_parts[4]}-{key_parts[5]}"
            
            # Veritabanında kontrol et
            if not self.key_exists(key):
                return key
    
    def key_exists(self, key: str) -> bool:
        """Key'in veritabanında var olup olmadığını kontrol et"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM licenses WHERE license_key = ?", (key,))
            exists = cursor.fetchone()[0] > 0
            conn.close()
            return exists
        except:
            return False
    
    def validate_license(self, license_key: str) -> Tuple[bool, str, Dict]:
        """Lisans anahtarını doğrula"""
        try:
            # Format kontrolü
            if not self.is_valid_format(license_key):
                return False, "Geçersiz lisans formatı", {}
            
            # Veritabanında kontrol et
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT license_key, license_type, expiry_date, is_used, used_by, price
                FROM licenses 
                WHERE license_key = ?
            ''', (license_key,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False, "Lisans anahtarı bulunamadı", {}
            
            key, license_type, expiry_date, is_used, used_by, price = result
            
            # Süre kontrolü
            expiry = datetime.fromisoformat(expiry_date)
            now = datetime.now()
            
            if expiry < now:
                return False, "Lisans süresi dolmuş", {}
            
            # Kullanım kontrolü
            if is_used == 1 and used_by:
                # Hardware ID kontrolü eklenebilir
                pass
            
            # Lisans verilerini hazırla
            license_data = {
                'key': key,
                'type': license_type,
                'expiry_date': expiry_date,
                'is_used': is_used,
                'used_by': used_by,
                'price': price,
                'days_remaining': (expiry - now).days
            }
            
            return True, "Lisans geçerli", license_data
            
        except Exception as e:
            return False, f"Doğrulama hatası: {e}", {}
    
    def is_valid_format(self, key: str) -> bool:
        """Lisans anahtarı formatını kontrol et"""
        # QUA-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX formatı
        if not key.startswith("QUA-"):
            return False
        
        parts = key.split("-")
        if len(parts) != 7:  # QUA + 6 grup
            return False
        
        if parts[0] != "QUA":
            return False
        
        # Her grup 4 karakter olmalı
        for part in parts[1:]:
            if len(part) != 4:
                return False
            # Sadece büyük harf ve rakam
            if not all(c.isalnum() and c.isupper() or c.isdigit() for c in part):
                return False
        
        return True
    
    def activate_license(self, license_key: str, username: str = None, email: str = None) -> Tuple[bool, str]:
        """Lisansı aktifleştir"""
        try:
            # Lisansı doğrula
            is_valid, message, license_data = self.validate_license(license_key)
            
            if not is_valid:
                return False, message
            
            # Hardware ID al
            hardware_id = self.get_hardware_id()
            
            # Veritabanını güncelle
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Lisansı kullanıldı olarak işaretle
            cursor.execute('''
                UPDATE licenses 
                SET is_used = 1, used_by = ?, hardware_id = ?, last_check = ?
                WHERE license_key = ?
            ''', (username or "Unknown", hardware_id, datetime.now().isoformat(), license_key))
            
            # Kullanıcı kaydı oluştur
            cursor.execute('''
                INSERT INTO users (username, email, license_key, created_date, expiry_date, hardware_id, last_login, login_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            ''', (username or "Unknown", email or "", license_key, datetime.now().isoformat(), 
                  license_data['expiry_date'], hardware_id, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            # Cache'e kaydet
            self.save_to_cache(license_data)
            
            return True, "Lisans başarıyla aktifleştirildi"
            
        except Exception as e:
            return False, f"Aktivasyon hatası: {e}"
    
    def get_hardware_id(self) -> str:
        """Benzersiz hardware ID oluştur"""
        try:
            import platform
            import uuid
            
            # Sistem bilgilerini birleştir
            system_info = [
                platform.machine(),
                platform.processor(),
                platform.node(),
                str(uuid.getnode())  # MAC adresi
            ]
            
            # Hash oluştur
            hardware_string = "-".join(system_info)
            return hashlib.md5(hardware_string.encode()).hexdigest()[:16]
            
        except:
            return "unknown"
    
    def check_license_status(self) -> Tuple[bool, str, Dict]:
        """Mevcut lisans durumunu kontrol et"""
        try:
            # Cache'i devre dışı bırak - her seferinde key iste
            return False, "Lisans anahtarı bulunamadı", {}
            
        except Exception as e:
            return False, f"Durum kontrolü hatası: {e}", {}
    
    def save_to_cache(self, license_data: Dict):
        """Lisans verilerini cache'e kaydet"""
        try:
            cache_data = {
                'license_data': license_data,
                'timestamp': time.time(),
                'license_key': self.license_key
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
                
        except Exception as e:
            print(f"Cache kaydetme hatası: {e}")
    
    def load_from_cache(self) -> Optional[Dict]:
        """Cache'den lisans verilerini yükle"""
        try:
            if not os.path.exists(self.cache_file):
                return None
            
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
            
            return cache_data.get('license_data')
            
        except Exception as e:
            print(f"Cache yükleme hatası: {e}")
            return None
    
    def is_cache_valid(self, cache_data: Dict) -> bool:
        """Cache'in geçerli olup olmadığını kontrol et"""
        try:
            if not cache_data:
                return False
            
            # Süre kontrolü
            expiry_date = datetime.fromisoformat(cache_data['expiry_date'])
            if expiry_date < datetime.now():
                return False
            
            return True
            
        except:
            return False
    
    def get_license_info(self) -> Dict:
        """Lisans bilgilerini döndür"""

        if not self.license_data:
            return {}
        
        return {
            'key': self.license_data.get('key', ''),
            'type': self.license_data.get('type', ''),
            'expiry_date': self.license_data.get('expiry_date', ''),
            'days_remaining': self.license_data.get('days_remaining', 0),
            'is_valid': self.is_valid
        }
    
    def set_license_key(self, key: str):
        """Lisans anahtarını ayarla"""
        self.license_key = key
    
    def clear_license(self):
        """Lisans verilerini temizle"""
        self.license_key = None
        self.license_data = None
        self.is_valid = False
        self.expiry_date = None
        self.license_type = None
        
        # Cache'i sil
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
    
    def check_api_connection(self) -> bool:
        """API bağlantısını kontrol et"""
        try:
            response = requests.get(
                f"{self.api_url}/health",
                timeout=self.api_timeout,
                headers={'X-API-Key': self.api_key}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"⚠️ API bağlantı hatası: {e}")
            return False
    
    def validate_license_online(self, license_key: str) -> Tuple[bool, str, Dict]:
        """Online lisans doğrulama"""
        try:
            data = {
                'license_key': license_key,
                'hardware_id': self.get_hardware_id()
            }
            
            response = requests.post(
                f"{self.api_url}/license/validate",
                json=data,
                timeout=self.api_timeout,
                headers={
                    'X-API-Key': self.api_key,
                    'Content-Type': 'application/json'
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('valid'):
                    return True, "Lisans geçerli", result.get('license_data', {})
                else:
                    return False, result.get('message', 'Lisans geçersiz'), {}
            else:
                return False, f"API Hatası: {response.status_code}", {}
                
        except requests.exceptions.Timeout:
            return False, "API zaman aşımı", {}
        except requests.exceptions.ConnectionError:
            return False, "API bağlantı hatası", {}
        except Exception as e:
            return False, f"Online doğrulama hatası: {e}", {}
    
    def activate_license_online(self, license_key: str, username: str = None, email: str = None) -> Tuple[bool, str]:
        """Online lisans aktivasyonu"""
        try:
            data = {
                'license_key': license_key,
                'username': username,
                'email': email,
                'hardware_id': self.get_hardware_id()
            }
            
            response = requests.post(
                f"{self.api_url}/license/activate",
                json=data,
                timeout=self.api_timeout,
                headers={
                    'X-API-Key': self.api_key,
                    'Content-Type': 'application/json'
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    return True, result.get('message', 'Lisans aktifleştirildi')
                else:
                    return False, result.get('message', 'Aktivasyon başarısız')
            else:
                return False, f"API Hatası: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "API zaman aşımı"
        except requests.exceptions.ConnectionError:
            return False, "API bağlantı hatası"
        except Exception as e:
            return False, f"Online aktivasyon hatası: {e}"
    
    def get_license_status_online(self, license_key: str) -> Tuple[bool, str, Dict]:
        """Online lisans durumu kontrolü"""
        try:
            response = requests.get(
                f"{self.api_url}/license/status",
                params={'license_key': license_key},
                timeout=self.api_timeout,
                headers={'X-API-Key': self.api_key}
            )
            
            if response.status_code == 200:
                result = response.json()
                license_data = result.get('license_data', {})
                return True, "Başarılı", license_data
            else:
                return False, f"API Hatası: {response.status_code}", {}
                
        except requests.exceptions.Timeout:
            return False, "API zaman aşımı", {}
        except requests.exceptions.ConnectionError:
            return False, "API bağlantı hatası", {}
        except Exception as e:
            return False, f"Online durum kontrolü hatası: {e}", {}
    
    def validate_license(self, license_key: str) -> Tuple[bool, str, Dict]:
        """Lisans anahtarını doğrula (Online + Offline)"""
        # Önce online kontrol et
        if self.check_api_connection():
            is_valid, message, license_data = self.validate_license_online(license_key)
            if is_valid:
                return True, message, license_data
        
        # Online başarısızsa offline kontrol et
        return self._validate_license_offline(license_key)
    
    def _validate_license_offline(self, license_key: str) -> Tuple[bool, str, Dict]:
        """Offline lisans doğrulama"""
        try:
            # Format kontrolü
            if not self.is_valid_format(license_key):
                return False, "Geçersiz lisans formatı", {}
            
            # Veritabanında kontrol et
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT license_key, license_type, expiry_date, is_used, used_by, price, hardware_id
                FROM licenses 
                WHERE license_key = ?
            ''', (license_key,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False, "Lisans anahtarı bulunamadı", {}
            
            key, license_type, expiry_date, is_used, used_by, price, hardware_id = result
            
            # Süre kontrolü - Çok sıkı kontrol
            expiry = datetime.fromisoformat(expiry_date)
            now = datetime.now()
            

            
            # Süresi dolmuşsa kesinlikle kabul etme
            if expiry <= now:
                return False, "Lisans süresi dolmuş", {}
            
            # HWID kontrolü - Eğer key daha önce kullanılmışsa aynı PC'de olmalı
            current_hwid = self.get_hardware_id()
            if hardware_id and hardware_id != current_hwid:
                return False, "Bu lisans başka bir bilgisayarda kullanılıyor", {}
            
            # Lisans verilerini hazırla
            days_remaining = (expiry - now).days
            # Eğer aynı gün içindeyse ve henüz bitmemişse 1 gün kaldı say
            if days_remaining == 0 and expiry > now:
                days_remaining = 1
            
            license_data = {
                'key': key,
                'type': license_type,
                'expiry_date': expiry_date,
                'is_used': is_used,
                'used_by': used_by,
                'price': price,
                'days_remaining': max(0, days_remaining)  # Negatif olmasın
            }
            
            return True, "Lisans geçerli", license_data
            
        except Exception as e:
            return False, f"Doğrulama hatası: {e}", {}
    
    def activate_license(self, license_key: str, username: str = None, email: str = None) -> Tuple[bool, str]:
        """Lisans aktivasyonu (Online + Offline)"""
        # Önce online aktivasyon dene
        if self.check_api_connection():
            success, message = self.activate_license_online(license_key, username, email)
            if success:
                return True, message
        
        # Online başarısızsa offline aktivasyon
        return self._activate_license_offline(license_key, username, email)
    
    def _activate_license_offline(self, license_key: str, username: str = None, email: str = None) -> Tuple[bool, str]:
        """Offline lisans aktivasyonu"""
        try:
            # Lisansı doğrula
            is_valid, message, license_data = self._validate_license_offline(license_key)
            if not is_valid:
                return False, message
            
            # Kullanım kontrolü - Devre dışı bırak (aynı key tekrar kullanılabilir)
            # if license_data.get('is_used') == 1:
            #     return False, "Lisans zaten kullanılıyor"
            
            # Veritabanında güncelle
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE licenses 
                SET is_used = 1, used_by = ?, hardware_id = ?
                WHERE license_key = ?
            ''', (username or 'Unknown', self.get_hardware_id(), license_key))
            
            # Kullanıcı kaydı oluştur
            now = datetime.now()
            cursor.execute('''
                INSERT INTO users (username, email, license_key, created_date, expiry_date, hardware_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, license_key, now.isoformat(), license_data['expiry_date'], self.get_hardware_id()))
            
            conn.commit()
            conn.close()
            
            # Instance değişkenlerini set et
            self.license_key = license_key
            self.license_data = license_data
            self.is_valid = True
            self.expiry_date = license_data['expiry_date']
            self.license_type = license_data['type']
            self.save_to_cache(license_data)
            
            return True, "Lisans başarıyla aktifleştirildi"
            
        except Exception as e:
            return False, f"Aktivasyon hatası: {e}"

# Global lisans sistemi instance'ı
license_system = LicenseSystem()
