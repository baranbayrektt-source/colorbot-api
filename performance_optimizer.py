"""
⚡ QUARXV1 Performance Optimizer
Advanced CPU & Memory Optimization System
"""

import os
import sys
import time
import threading
import psutil
import gc
from typing import Optional, Dict, Any
import ctypes
from ctypes import wintypes

class PerformanceOptimizer:
    """Advanced performance optimization system"""
    
    def __init__(self):
        self.is_optimizing = False
        self.optimization_thread = None
        self.cpu_threshold = 15.0  # Maximum CPU usage % - BALANCED FOR SMOOTHNESS
        self.memory_threshold = 200  # Maximum memory usage MB - HIGHER FOR SMOOTHNESS
        self.frame_skip_enabled = True
        self.adaptive_quality = True
        
        # Performance metrics
        self.metrics = {
            'cpu_usage': 0.0,
            'memory_usage': 0.0,
            'frame_rate': 20.0,  # HIGHER FOR SMOOTHNESS
            'frame_skip_count': 0,
            'optimization_level': 2  # BALANCED OPTIMIZATION
        }
        
        # Optimization levels - BALANCED FOR SMOOTHNESS
        self.optimization_levels = {
            1: {'fps': 30, 'quality': 'high', 'skip_frames': 0},
            2: {'fps': 20, 'quality': 'medium', 'skip_frames': 1},  # DEFAULT
            3: {'fps': 15, 'quality': 'low', 'skip_frames': 2},
            4: {'fps': 10, 'quality': 'minimal', 'skip_frames': 3}
        }
        
    def enable_optimization(self):
        """Enable performance optimization"""
        try:
            print("⚡ Enabling Performance Optimization...")
            
            # Set process priority to below normal
            self._set_process_priority()
            
            # Enable CPU affinity optimization
            self._optimize_cpu_affinity()
            
            # Configure memory optimization
            self._optimize_memory()
            
            # Start adaptive optimization
            self._start_adaptive_optimization()
            
            # Enable power management
            self._configure_power_management()
            
            self.is_optimizing = True
            print("✅ Performance optimization enabled")
            return True
            
        except Exception as e:
            print(f"⚠️ Optimization failed: {e}")
            return False
    
    def _set_process_priority(self):
        """Set optimal process priority"""
        try:
            # Set to below normal priority to reduce CPU impact
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)  # BELOW_NORMAL_PRIORITY_CLASS
            
            # Set thread priority
            thread_handle = ctypes.windll.kernel32.GetCurrentThread()
            ctypes.windll.kernel32.SetThreadPriority(thread_handle, -1)  # THREAD_PRIORITY_BELOW_NORMAL
            
        except Exception:
            pass
    
    def _optimize_cpu_affinity(self):
        """Optimize CPU core usage"""
        try:
            # Get CPU count
            cpu_count = psutil.cpu_count()
            
            if cpu_count >= 4:
                # Use only performance cores (avoid efficiency cores on newer CPUs)
                process = psutil.Process()
                
                # Use cores 0,2,4,6 (typically performance cores)
                performance_cores = list(range(0, min(cpu_count, 8), 2))
                process.cpu_affinity(performance_cores)
                
        except Exception:
            pass
    
    def _optimize_memory(self):
        """Optimize memory usage"""
        try:
            # Force garbage collection
            gc.collect()
            
            # Set working set size limits
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetCurrentProcess()
            
            # Limit working set to 200MB
            min_ws = 50 * 1024 * 1024  # 50MB minimum
            max_ws = 200 * 1024 * 1024  # 200MB maximum
            
            kernel32.SetProcessWorkingSetSize(handle, min_ws, max_ws)
            
        except Exception:
            pass
    
    def _start_adaptive_optimization(self):
        """Start adaptive performance optimization"""
        if self.optimization_thread is None:
            self.optimization_thread = threading.Thread(
                target=self._adaptive_optimization_loop,
                daemon=True
            )
            self.optimization_thread.start()
    
    def _adaptive_optimization_loop(self):
        """Adaptive optimization main loop"""
        while self.is_optimizing:
            try:
                # Monitor system resources
                self._update_metrics()
                
                # Adjust optimization level based on CPU usage
                self._adjust_optimization_level()
                
                # Perform memory cleanup if needed
                if self.metrics['memory_usage'] > self.memory_threshold:
                    self._perform_memory_cleanup()
                
                # Sleep with adaptive interval
                sleep_time = 2.0 if self.metrics['cpu_usage'] < 10 else 1.0
                time.sleep(sleep_time)
                
            except Exception:
                time.sleep(2.0)
    
    def _update_metrics(self):
        """Update performance metrics"""
        try:
            # Get current process
            process = psutil.Process()
            
            # Update CPU usage
            self.metrics['cpu_usage'] = process.cpu_percent()
            
            # Update memory usage (in MB)
            memory_info = process.memory_info()
            self.metrics['memory_usage'] = memory_info.rss / 1024 / 1024
            
        except Exception:
            pass
    
    def _adjust_optimization_level(self):
        """Adjust optimization level based on CPU usage"""
        cpu_usage = self.metrics['cpu_usage']
        current_level = self.metrics['optimization_level']
        
        # Increase optimization if CPU usage is high
        if cpu_usage > 20 and current_level < 4:
            self.metrics['optimization_level'] = min(4, current_level + 1)
            print(f"⚡ Optimization level increased to {self.metrics['optimization_level']}")
        
        # Decrease optimization if CPU usage is low
        elif cpu_usage < 8 and current_level > 1:
            self.metrics['optimization_level'] = max(1, current_level - 1)
            print(f"⚡ Optimization level decreased to {self.metrics['optimization_level']}")
    
    def _perform_memory_cleanup(self):
        """Perform memory cleanup"""
        try:
            # Force garbage collection
            gc.collect()
            
            # Trim working set
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetCurrentProcess()
            kernel32.SetProcessWorkingSetSize(handle, -1, -1)
            
            print("🧹 Memory cleanup performed")
            
        except Exception:
            pass
    
    def _configure_power_management(self):
        """Configure power management for performance"""
        try:
            # Set high performance power plan
            os.system("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
            
            # Disable CPU parking
            os.system("powercfg /setacvalueindex scheme_current sub_processor PROCTHROTTLEMIN 100")
            os.system("powercfg /setactive scheme_current")
            
        except Exception:
            pass
    
    def get_optimal_settings(self) -> Dict[str, Any]:
        """Get optimal settings based on current performance"""
        level = self.metrics['optimization_level']
        settings = self.optimization_levels[level].copy()
        
        # Add dynamic adjustments
        if self.metrics['cpu_usage'] > 15:
            settings['fps'] = max(10, settings['fps'] - 5)
            settings['skip_frames'] += 1
        
        return settings
    
    def should_skip_frame(self) -> bool:
        """Determine if current frame should be skipped"""
        if not self.frame_skip_enabled:
            return False
        
        level = self.metrics['optimization_level']
        skip_frames = self.optimization_levels[level]['skip_frames']
        
        if skip_frames > 0:
            self.metrics['frame_skip_count'] += 1
            return (self.metrics['frame_skip_count'] % (skip_frames + 1)) != 0
        
        return False
    
    def get_optimal_sleep_time(self) -> float:
        """Get optimal sleep time for main loop"""
        level = self.metrics['optimization_level']
        target_fps = self.optimization_levels[level]['fps']
        
        base_sleep = 1.0 / target_fps
        
        # Adjust based on CPU usage
        if self.metrics['cpu_usage'] > 15:
            return base_sleep * 1.5
        elif self.metrics['cpu_usage'] < 5:
            return base_sleep * 0.8
        
        return base_sleep
    
    def optimize_screen_capture(self, width: int, height: int) -> tuple:
        """Get optimized screen capture dimensions"""
        level = self.metrics['optimization_level']
        
        scale_factors = {
            1: 1.0,    # Full quality
            2: 0.8,    # 80% quality
            3: 0.6,    # 60% quality
            4: 0.5     # 50% quality
        }
        
        scale = scale_factors[level]
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Ensure dimensions are even (for better performance)
        new_width = new_width - (new_width % 2)
        new_height = new_height - (new_height % 2)
        
        return new_width, new_height
    
    def optimize_color_detection(self) -> Dict[str, Any]:
        """Get optimized color detection settings"""
        level = self.metrics['optimization_level']
        
        settings = {
            1: {'blur_kernel': 3, 'iterations': 2, 'precision': 'high'},
            2: {'blur_kernel': 5, 'iterations': 1, 'precision': 'medium'},
            3: {'blur_kernel': 7, 'iterations': 1, 'precision': 'low'},
            4: {'blur_kernel': 9, 'iterations': 1, 'precision': 'minimal'}
        }
        
        return settings[level]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get current performance report"""
        return {
            'cpu_usage': f"{self.metrics['cpu_usage']:.1f}%",
            'memory_usage': f"{self.metrics['memory_usage']:.1f}MB",
            'optimization_level': self.metrics['optimization_level'],
            'target_fps': self.optimization_levels[self.metrics['optimization_level']]['fps'],
            'frame_skips': self.metrics['frame_skip_count'],
            'status': 'Optimized' if self.is_optimizing else 'Disabled'
        }
    
    def emergency_optimization(self):
        """Emergency optimization for very high CPU usage"""
        print("🚨 Emergency optimization activated!")
        
        # Force maximum optimization
        self.metrics['optimization_level'] = 4
        
        # Aggressive memory cleanup
        for _ in range(3):
            gc.collect()
            time.sleep(0.1)
        
        # Reduce process priority further
        try:
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.kernel32.SetPriorityClass(handle, 0x00000040)  # IDLE_PRIORITY_CLASS
        except:
            pass
        
        print("⚡ Emergency optimization complete")
    
    def disable_optimization(self):
        """Disable performance optimization"""
        self.is_optimizing = False
        
        if self.optimization_thread:
            self.optimization_thread.join(timeout=1.0)
            self.optimization_thread = None
        
        # Reset process priority
        try:
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.kernel32.SetPriorityClass(handle, 0x00000020)  # NORMAL_PRIORITY_CLASS
        except:
            pass
        
        # Silent disable - no message

# Global optimizer instance
performance_optimizer = PerformanceOptimizer()

def enable_performance_optimization():
    """Enable performance optimization"""
    return performance_optimizer.enable_optimization()

def get_optimal_settings():
    """Get optimal settings for current performance"""
    return performance_optimizer.get_optimal_settings()

def should_skip_frame():
    """Check if frame should be skipped"""
    return performance_optimizer.should_skip_frame()

def get_optimal_sleep_time():
    """Get optimal sleep time"""
    return performance_optimizer.get_optimal_sleep_time()

def optimize_screen_capture(width, height):
    """Optimize screen capture dimensions"""
    return performance_optimizer.optimize_screen_capture(width, height)

def get_performance_report():
    """Get performance report"""
    return performance_optimizer.get_performance_report()

def emergency_cpu_optimization():
    """Emergency CPU optimization"""
    performance_optimizer.emergency_optimization()

def disable_performance_optimization():
    """Disable optimization"""
    performance_optimizer.disable_optimization()