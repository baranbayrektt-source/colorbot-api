"""
ColorBot - Profesyonel Renk Tabanlı Nişan Yardımcısı
Basit ve etkili konsol arayüzü
"""

import sys
import os
import time
import threading
import logging
import requests
from typing import Optional, Dict, Any, List
import traceback

# Local modules
from screen_capture import ScreenCapture
from color_detection import TargetDetector
from mouse_control import MouseController, AimAssist
from key_binding import KeyBinding
from key_capture import KeyCapture, KeyValidator
from real_security import initialize_real_security, check_real_environment, disable_real_security
from performance_optimizer import enable_performance_optimization, get_optimal_sleep_time, should_skip_frame, get_performance_report, emergency_cpu_optimization, disable_performance_optimization
from final_stealth import start_final_stealth, stop_final_stealth, update_final_activity, show_console_final
from license_system import license_system


class ColorBot:
    """Ana ColorBot sınıfı - Temiz ve basit"""
    
    def __init__(self):
        # Logging
        logging.basicConfig(level=logging.WARNING, format='%(message)s')
        
        # Bileşenler
        self.screen_capture = None
        self.target_detector = None
        self.mouse_controller = None
        self.aim_assist = None
        self.key_binding = None
        
        # Ana ayarlar
        self.is_running = False
        self.is_active = False
        self.hold_mode = True  # True: basılı tut, False: toggle
        
        # Aimbot ayarları
        self.fov_x = 100  # X FOV (yatay - genişlik)
        self.fov_y = 80   # Y FOV (dikey - yükseklik)
        self.display_fov_x = 20  # X FOV (kullanıcıya gösterilen değer)
        self.display_fov_y = 16  # Y FOV (kullanıcıya gösterilen değer)
        self.smooth = 5.0  # Smooth değeri (1.0-20.0)
        
        # Tuş atamaları
        self.aim_key = "none"  # Nişan tuşu (atanmamış)
        
        # İstatistikler
        self.stats = {
            'targets_found': 0,
            'shots_fired': 0,
            'session_time': 0
        }
        
        print("🎯 ColorBot Pro yükleniyor...")
        self.initialize()
    
    def initialize(self):
        """Sistemi başlat"""
        try:
            # Ekran yakalama
            self.screen_capture = ScreenCapture()
            print("✅ Ekran yakalama")
            
            # Hedef tespit
            self.target_detector = TargetDetector()
            # Renk seçimi kullanıcı tarafından yapılacak
            print("✅ Hedef tespit")
            
            # Fare kontrolü
            self.mouse_controller = MouseController()
            self.aim_assist = AimAssist()
            print("✅ Fare kontrolü")
            
            # Tuş kontrolü
            self.key_binding = KeyBinding()
            self.setup_keybinds()
            print("✅ Tuş kontrolü")
            
            print("🎉 ColorBot Pro hazır!")
            
        except Exception as e:
            print(f"❌ Başlatma hatası: {e}")
            sys.exit(1)
    
    def setup_keybinds(self):
        """Tuş bağlamalarını ayarla"""
        def on_aim_activate():
            self.is_active = True
        
        def on_aim_deactivate():
            self.is_active = False
        
        def on_toggle():
            self.is_active = not self.is_active
        
        def on_exit():
            self.stop()
            sys.exit(0)
        
        # Dinamik tuş atama - aim_key'i kullan
        self.key_binding.set_callbacks(
            on_activate=on_aim_activate,
            on_deactivate=on_aim_deactivate,
            on_toggle=on_toggle,
            on_exit=on_exit
        )
        
        # Aim tuşunu kaydet (sadece atanmışsa)
        if self.aim_key and self.aim_key != "none":
            self.key_binding.set_activation_key(self.aim_key)
        self.key_binding.set_exit_key("f12")
        self.key_binding.set_hold_mode(self.hold_mode)
    
    def start(self):
        """Sistemi başlat"""
        if self.is_running:
            return
        
        # 🛡️ Initialize REAL PROFESSIONAL security
        print("🛡️ Initializing REAL Professional Security...")
        try:
            if not initialize_real_security():
                print("❌ Security initialization failed!")
        except Exception as e:
            print(f"⚠️ Security system error: {e}")
            print("🔄 Continuing without protection...")
        
        # 🔍 REAL Environment safety check
        try:
            safety_report = check_real_environment()
            
            if not safety_report['safe']:
                print(f"\n🚨 REAL THREAT ANALYSIS")
                print(f"🔴 Risk Level: {safety_report['risk_level']}")
                print(f"⚠️ Threat Score: {safety_report['threat_score']}")
                print(f"🎯 Detected Threats: {len(safety_report['threats'])}")
                
                for category, threat in safety_report['threats']:
                    print(f"   └── [{category.upper()}] {threat}")
                
                print(f"\n📋 Professional Recommendations:")
                for rec in safety_report['recommendations']:
                    print(f"   • {rec}")
                
                if safety_report['risk_level'] == 'CRITICAL':
                    print("\n🛑 CRITICAL THREAT - OPERATION ABORTED")
                    return
                elif safety_report['risk_level'] == 'HIGH':
                    print("\n⚠️ HIGH THREAT DETECTED!")
                    print("🎯 Continue with maximum stealth? (y/n)")
                    if input().lower() != 'y':
                        return
                    else:
                        print("👻 Activating stealth protocols...")
                else:
                    print("\n✅ Environment secured - Professional protection active")
        except Exception as e:
            print(f"⚠️ Environment check error: {e}")
            print("🔄 Skipping security analysis...")
        
        # ⚡ Enable performance optimization
        print("⚡ Enabling Performance Optimization...")
        try:
            if enable_performance_optimization():
                print("✅ CPU optimization enabled")
            else:
                print("⚠️ Performance optimization failed")
        except Exception as e:
            print(f"⚠️ Performance optimizer error: {e}")
            print("🔄 Continuing with standard performance...")
        
        print("Starting...")
        
        # Ekran yakalama başlat
        self.screen_capture.start_continuous_capture()
        
        # Tuş dinleme başlat
        self.key_binding.start_listening()
        
        # Ana döngü başlat
        self.is_running = True
        self.main_thread = threading.Thread(target=self.main_loop, daemon=True)
        self.main_thread.start()
        
        # 👻 Start final stealth system  
        print("👻 Activating final stealth...")
        try:
            start_final_stealth()
        except Exception as e:
            print(f"⚠️ Final stealth error: {e}")

        print("✅ QUARXV1 started with security protection")
    
    def stop(self):
        """Sistemi durdur"""
        self.is_running = False
        self.is_active = False
        
        # ⚡ Silently disable performance optimization
        try:
            disable_performance_optimization()
        except:
            pass
        
        # 👻 Silently stop final stealth
        try:
            stop_final_stealth()
        except:
            pass
        
        # 🛡️ Silently disable security protocols
        try:
            disable_real_security()
        except:
            pass
        
        if self.screen_capture:
            self.screen_capture.stop_continuous_capture()
        if self.key_binding:
            self.key_binding.stop_listening()
        
        # Silent stop - program ending
    
    def main_loop(self):
        """Ana işlem döngüsü - Performance Optimized"""
        frame_count = 0
        cpu_check_interval = 100  # Check CPU every 100 frames
        
        while self.is_running:
            try:
                # ⚡ Performance monitoring
                if frame_count % cpu_check_interval == 0:
                    report = get_performance_report()
                    if float(report['cpu_usage'].replace('%', '')) > 25:
                        print("🚨 High CPU usage detected - applying emergency optimization")
                        emergency_cpu_optimization()
                
                # ⚡ Frame skipping for performance
                if should_skip_frame():
                    time.sleep(get_optimal_sleep_time())
                    frame_count += 1
                    continue
                
                # Process frame only if active
                if self.is_active:
                    self.process_frame()
                
                # ⚡ Adaptive sleep time based on performance
                sleep_time = get_optimal_sleep_time()
                time.sleep(sleep_time)
                
                frame_count += 1
                
            except Exception as e:
                # Error handling with performance consideration
                time.sleep(0.1)
                continue
    
    def process_frame(self):
        """Frame işle ve nişan al"""
        try:
            # Ekran görüntüsü al
            frame = self.screen_capture.get_latest_frame()
            if frame is None:
                return
            
            # FOV alanında hedef ara
            targets = self.find_targets_in_fov(frame)
            if not targets:
                return
            
            # En iyi hedefi seç
            best_target = self.select_best_target(targets, frame)
            if best_target:
                self.aim_at_target(best_target)
                self.stats['targets_found'] += 1
                
        except Exception as e:
            pass  # Sessiz hata handling
    
    def find_targets_in_fov(self, frame):
        """FOV alanında hedefleri bul (X ve Y ayrı)"""
        all_targets = self.target_detector.detect_targets(frame)
        screen_center = (frame.shape[1] // 2, frame.shape[0] // 2)
        fov_targets = []
        
        for target in all_targets:
            target_pos = target['center']
            dx = abs(target_pos[0] - screen_center[0])
            dy = abs(target_pos[1] - screen_center[1])
            if dx <= self.fov_x and dy <= self.fov_y:
                fov_targets.append(target)
        
        return fov_targets
    
    def select_best_target(self, targets, frame):
        """En iyi hedefi seç (X ve Y ayrı skorlama)"""
        if not targets:
            return None
        
        screen_center = frame.shape[1] // 2, frame.shape[0] // 2
        
        def score_target(target):
            pos = target['center']
            dx = abs(pos[0] - screen_center[0])
            dy = abs(pos[1] - screen_center[1])
            confidence = target.get('confidence', 0.5)
            
            # X ve Y ayrı skorlama
            x_score = max(0, 1 - dx / self.fov_x)
            y_score = max(0, 1 - dy / self.fov_y)
            distance_score = (x_score * 0.3 + y_score * 0.7)  # Y ekseni daha önemli
            return confidence * 0.6 + distance_score * 0.4
        
        return max(targets, key=score_target)
    
    def aim_at_target(self, target):
        """Gelişmiş smooth nişan alma (X ve Y ayrı)"""
        target_pos = target['center']
        current_pos = self.mouse_controller.get_current_mouse_position()
        
        # Mesafe hesapla
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        distance = (dx**2 + dy**2)**0.5
        
        # Çok yakınsa hareket etme
        if distance < 5:
            return
        
        # Adaptive smooth (X ve Y ayrı)
        base_smooth = self.smooth
        
        if dx > 50:
            smooth_x = base_smooth * 0.3
        elif dx > 25:
            smooth_x = base_smooth * 0.5
        else:
            smooth_x = base_smooth * 0.8
            
        if dy > 40:
            smooth_y = base_smooth * 0.2
        elif dy > 20:
            smooth_y = base_smooth * 0.4
        else:
            smooth_y = base_smooth * 0.9
        
        # Hareket miktarını hesapla
        move_x = dx * (smooth_x / 20.0)
        move_y = dy * (smooth_y / 20.0)
        
        # Maksimum hareket sınırı (X ve Y ayrı)
        max_move_x = 60
        max_move_y = 40
        
        if abs(move_x) > max_move_x:
            move_x = max_move_x if move_x > 0 else -max_move_x
        if abs(move_y) > max_move_y:
            move_y = max_move_y if move_y > 0 else -max_move_y
        
        # Yeni pozisyon
        new_x = current_pos[0] + move_x
        new_y = current_pos[1] + move_y
        
        # Hareket et
        self.mouse_controller.move_to_target((int(new_x), int(new_y)), smooth=False)
    


def clear_screen():
    """Ekranı temizle"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu(bot):
    """Show main menu with performance info"""
    clear_screen()
    print("\033[96m")
    print(" _____                                             _____ ")
    print("( ___ )                                           ( ___ )")
    print(" |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | ")
    print(" |   |   ___  _   _   _    ____  __  ____     ___  |   | ")
    print(" |   |  / _ \\| | | | / \\  |  _ \\ \\ \\/ /\\ \\   / / | |   | ")
    print(" |   | | | | | | | |/ _ \\ | |_) | \\  /  \\ \\ / /| | |   | ")
    print(" |   | | |_| | |_| / ___ \\|  _ <  /  \\   \\ V / | | |   | ")
    print(" |   |  \\__\\_\\\\___/_/   \\_\\_| \\_\\/_/\\_\\   \\_/  |_| |   | ")
    print(" |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| ")
    print("(_____)                                           (_____)")
    print("\033[0m")
    print()
    
    # Show license information
    license_info = license_system.get_license_info()

    if license_info:
        # Check if license expired
        if license_info.get('days_remaining', 0) <= 0:
            print("\033[91mLicense expired!\033[0m")
            print("Please purchase a new license key.")
            input("Press Enter to exit...")
            sys.exit(0)
        
        # Format expiry date nicely
        try:
            from datetime import datetime
            expiry_date = datetime.fromisoformat(license_info['expiry_date'])
            formatted_date = expiry_date.strftime('%d/%m/%Y %H:%M')
        except:
            formatted_date = license_info['expiry_date']
        
        print(f"\033[92mLicense: {license_info['type']}\033[0m")
        print(f"Expires: {formatted_date}")
        print(f"Remaining: {license_info['days_remaining']} days")
        print()
    
    print(f"FOV X: {bot.display_fov_x}    FOV Y: {bot.display_fov_y}")
    print(f"Smooth (Aim Speed): {bot.smooth}")
    print(f"Mode: Hold")
    print(f"Key: {bot.aim_key.upper() if bot.aim_key != 'none' else 'Not assigned'}")
    colors_text = ', '.join([cr.name for cr in bot.target_detector.active_colors]) if bot.target_detector.active_colors else "Not selected"
    print(f"Colors: {colors_text}")
    print("\033[95m" + "═" * 60 + "\033[0m")
    print("1. FOV Settings    2. Smooth")
    print("3. Key             4. Colors ") 
    print("5. Exit")
    print("\033[95m" + "═" * 60 + "\033[0m")


def set_fov(bot):
    """FOV Settings Menu"""
    while True:
        clear_screen()
        print("\033[96m")
        print(" _____                                             _____ ")
        print("( ___ )                                           ( ___ )")
        print(" |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | ")
        print(" |   |   ___  _   _   _    ____  __  ____     ___  |   | ")
        print(" |   |  / _ \\| | | | / \\  |  _ \\ \\ \\/ /\\ \\   / / | |   | ")
        print(" |   | | | | | | | |/ _ \\ | |_) | \\  /  \\ \\ / /| | |   | ")
        print(" |   | | |_| | |_| / ___ \\|  _ <  /  \\   \\ V / | | |   | ")
        print(" |   |  \\__\\_\\\\___/_/   \\_\\_| \\_\\/_/\\_\\   \\_/  |_| |   | ")
        print(" |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| ")
        print("(_____)                                           (_____)")
        print("\033[0m")
        print()
        print(f"Current FOV X: {bot.display_fov_x}")
        print(f"Current FOV Y: {bot.display_fov_y}")
        print()
        print("\033[95m" + "═" * 60 + "\033[0m")
        print("1. FOV X")
        print("2. FOV Y")
        print("3. Back")
        print("\033[95m" + "═" * 60 + "\033[0m")
        
        choice = input("> ").strip()
        
        if choice == "1":
            set_fov_x(bot)
        elif choice == "2":
            set_fov_y(bot)
        elif choice == "3":
            break
        else:
            print("Invalid choice")

def set_fov_x(bot):
    """FOV X Menu"""
    while True:
        clear_screen()
        print("\033[96m")
        print(" _____                                             _____ ")
        print("( ___ )                                           ( ___ )")
        print(" |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | ")
        print(" |   |   ___  _   _   _    ____  __  ____     ___  |   | ")
        print(" |   |  / _ \\| | | | / \\  |  _ \\ \\ \\/ /\\ \\   / / | |   | ")
        print(" |   | | | | | | | |/ _ \\ | |_) | \\  /  \\ \\ / /| | |   | ")
        print(" |   | | |_| | |_| / ___ \\|  _ <  /  \\   \\ V / | | |   | ")
        print(" |   |  \\__\\_\\\\___/_/   \\_\\_| \\_\\/_/\\_\\   \\_/  |_| |   | ")
        print(" |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| ")
        print("(_____)                                           (_____)")
        print("\033[0m")
        print()
        print(f"Current FOV X: {bot.display_fov_x}")
        print("Range: 15-50")
        print()
        print("\033[95m" + "═" * 60 + "\033[0m")
        print("1. Set Value")
        print("2. Back")
        print("\033[95m" + "═" * 60 + "\033[0m")
        
        choice = input("> ").strip()
        
        if choice == "1":
            set_fov_x_value(bot)
        elif choice == "2":
            break
        else:
            print("Invalid choice")

def set_fov_x_value(bot):
    """Set FOV X value"""
    try:
        print("\nFOV X")
        print("Range: 15-50")
        print()
        fov_x_input = float(input("FOV X: "))
        if 15 <= fov_x_input <= 50:
            real_fov_x = (fov_x_input - 15) * 320 / 35 + 80
            bot.fov_x = real_fov_x
            bot.display_fov_x = fov_x_input
            print(f"✅ FOV X set to: {fov_x_input}")
        else:
            print("❌ Invalid range (15-50)")
        input("Press Enter to continue...")
    except ValueError:
        print("❌ Invalid input")
        input("Press Enter to continue...")

def set_fov_y(bot):
    """FOV Y Menu"""
    while True:
        clear_screen()
        print("\033[96m")
        print(" _____                                             _____ ")
        print("( ___ )                                           ( ___ )")
        print(" |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | ")
        print(" |   |   ___  _   _   _    ____  __  ____     ___  |   | ")
        print(" |   |  / _ \\| | | | / \\  |  _ \\ \\ \\/ /\\ \\   / / | |   | ")
        print(" |   | | | | | | | |/ _ \\ | |_) | \\  /  \\ \\ / /| | |   | ")
        print(" |   | | |_| | |_| / ___ \\|  _ <  /  \\   \\ V / | | |   | ")
        print(" |   |  \\__\\_\\\\___/_/   \\_\\_| \\_\\/_/\\_\\   \\_/  |_| |   | ")
        print(" |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| ")
        print("(_____)                                           (_____)")
        print("\033[0m")
        print()
        print(f"Current FOV Y: {bot.display_fov_y}")
        print("Range: 10-40")
        print()
        print("\033[95m" + "═" * 60 + "\033[0m")
        print("1. Set Value")
        print("2. Back")
        print("\033[95m" + "═" * 60 + "\033[0m")
        
        choice = input("> ").strip()
        
        if choice == "1":
            set_fov_y_value(bot)
        elif choice == "2":
            break
        else:
            print("Invalid choice")

def set_fov_y_value(bot):
    """Set FOV Y value"""
    try:
        print("\nFOV Y")
        print("Range: 10-40")
        print()
        fov_y_input = float(input("FOV Y: "))
        if 10 <= fov_y_input <= 40:
            real_fov_y = (fov_y_input - 10) * 240 / 30 + 60
            bot.fov_y = real_fov_y
            bot.display_fov_y = fov_y_input
            print(f"✅ FOV Y set to: {fov_y_input}")
        else:
            print("❌ Invalid range (10-40)")
        input("Press Enter to continue...")
    except ValueError:
        print("❌ Invalid input")
        input("Press Enter to continue...")

def set_smooth(bot):
    """Set smooth"""
    try:
        smooth = float(input(f"Smooth (1-20): "))
        if 1.0 <= smooth <= 20.0:
            bot.smooth = smooth
            print(f"Smooth: {smooth}")
    except ValueError:
        pass


def set_colors(bot):
    """Set colors"""
    print("1. Yellow  2. Red  3. Purple")
    choice = input("Color: ").strip()
    
    if choice == "1":
        bot.target_detector.set_active_colors(['Yellow'])
        print("Yellow")
    elif choice == "2":
        bot.target_detector.set_active_colors(['Red'])
        print("Red")
    elif choice == "3":
        bot.target_detector.set_active_colors(['Purple'])
        print("Purple")

def set_aim_key(bot):
    """Set aim key"""
    key_capture = KeyCapture()
    print("Select key...")
    
    new_key = key_capture.capture_key(timeout=10.0)
    
    if new_key and KeyValidator.is_valid_key(new_key):
        bot.aim_key = new_key
        desc = KeyCapture.get_key_description(new_key)
        print(f"Key set: {desc}")
        bot.setup_keybinds()


def check_license():
    """License validation"""
    # Check license from cache
    is_valid, message, license_data = license_system.check_license_status()
    
    if is_valid and license_data:
        return True
    
    # Request license key if not found
    license_key = input("License Key: ").strip()
    
    if not license_key:
        return False
    
    # Validate license
    is_valid, message, license_data = license_system.validate_license(license_key)
    
    if is_valid:
        # Activate license
        success, activation_message = license_system.activate_license(license_key)
        return success
    
    return False

def main():
    """Main function"""
    # License validation
    if not check_license():
        return
    
    print("\n\033[92m🎉 ColorBot starting...\033[0m\n")
    
    # Create and start ColorBot
    bot = ColorBot()
    bot.start()
    
    # Main command loop
    try:
        while bot.is_running:
            show_menu(bot)
            
            choice = input("\n> ").strip()
            
            # Update final stealth activity on any input
            try:
                update_final_activity()
            except:
                pass
            
            if choice == "1":
                set_fov(bot)
            elif choice == "2":
                set_smooth(bot)
            elif choice == "3":
                set_aim_key(bot)
            elif choice == "4":
                set_colors(bot)
            elif choice == "5":
                break
            else:
                print("Invalid choice")
    
    except KeyboardInterrupt:
        pass
    
    finally:
        bot.stop()


if __name__ == "__main__":
    # Çalışma dizinini ayarla
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()