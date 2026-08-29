import tkinter as tk
from tkinter import ttk, messagebox
import pymem
import pymem.pattern
import ctypes
from pymem.memory import read_bytes, write_bytes
from pymem.pattern import pattern_scan_all
from pymem import Pymem
import threading
import time
import sys
import os

#exe
class AimbotController:
    def __init__(self, root):
        self.root = root
        self.root.title("Aimbot")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")
        
        # Variables
        self.is_injecting = False
        self.is_injected = False
        self.pm = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#16213e", height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title = tk.Label(header_frame, text="🎯 Aimbot", 
                        font=("Segoe UI", 20, "bold"), 
                        bg="#16213e", fg="#e94560")
        title.pack(pady=20)
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        # Status Frame
        status_frame = tk.Frame(main_frame, bg="#16213e", relief="ridge", bd=2)
        status_frame.pack(fill="x", pady=(0, 20))
        
        # Status Label
        self.status_label = tk.Label(status_frame, text="⚪ Status: Ready", 
                                    font=("Segoe UI", 12), 
                                    bg="#16213e", fg="#ffffff")
        self.status_label.pack(pady=10)
        
        # Progress Bar
        self.progress = ttk.Progressbar(status_frame, length=300, mode='indeterminate')
        self.progress.pack(pady=5)
        self.progress.pack_forget()
        
        # Button Frame
        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(pady=20)
        
        # Inject Button
        self.inject_btn = tk.Button(btn_frame, text="🔫 Inject Aimbot", 
                                   font=("Segoe UI", 13, "bold"),
                                   bg="#e94560", fg="white", 
                                   activebackground="#c73e54", 
                                   activeforeground="white",
                                   relief="flat", bd=0, 
                                   padx=30, pady=12,
                                   cursor="hand2",
                                   command=self.start_injection)
        self.inject_btn.pack(pady=5)
        
        # Status Text Frame
        status_text_frame = tk.Frame(main_frame, bg="#16213e", relief="sunken", bd=1)
        status_text_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Status Text (Log)
        self.status_text = tk.Text(status_text_frame, height=6, 
                                  font=("Consolas", 9), 
                                  bg="#0f0f1a", fg="#00ff88",
                                  relief="flat", bd=0,
                                  wrap="word")
        self.status_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar for text
        scrollbar = tk.Scrollbar(status_text_frame, command=self.status_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # Footer
        footer = tk.Label(self.root, text="Developed for Test Only | Use at your own risk", 
                         font=("Segoe UI", 8), 
                         bg="#1a1a2e", fg="#6c6c8a")
        footer.pack(side="bottom", pady=10)
        
        # Initial log
        self.add_log("🟢 Application started successfully")
        self.add_log("📌 Waiting for injection...")
        
        # Check for admin
        if not self.is_admin():
            self.add_log("⚠️ Not running as Administrator!")
            self.add_log("⚠️ Some features may not work properly")
        # Nazmul Exe
    def add_log(self, message):
        """Add message to status log"""
        timestamp = time.strftime("%H:%M:%S")
        self.status_text.insert("end", f"[{timestamp}] {message}\n")
        self.status_text.see("end")
        self.root.update()
        
    def update_status(self, text, color="#ffffff"):
        """Update status label"""
        self.status_label.config(text=text, fg=color)
        self.root.update()
    
    def is_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
        
    def adjust_privileges(self):
        """Adjust system privileges"""
        try:
            SE_DEBUG_NAME = "SeDebugPrivilege"
            SE_PRIVILEGE_ENABLED = 0x00000002
            token_handle = ctypes.c_void_p()
            luid = ctypes.c_longlong()
            
            ctypes.windll.advapi32.OpenProcessToken(
                ctypes.windll.kernel32.GetCurrentProcess(),
                0x20 | 0x8,
                ctypes.byref(token_handle)
            )
            
            ctypes.windll.advapi32.LookupPrivilegeValueA(
                0, SE_DEBUG_NAME.encode('ascii'), ctypes.byref(luid)
            )
            
            class LUID_AND_ATTRIBUTES(ctypes.Structure):
                _fields_ = [("Luid", ctypes.c_longlong), ("Attributes", ctypes.c_ulong)]
            
            class TOKEN_PRIVILEGES(ctypes.Structure):
                _fields_ = [("PrivilegeCount", ctypes.c_ulong), ("Privileges", LUID_AND_ATTRIBUTES)]
            
            new_privileges = TOKEN_PRIVILEGES(1, LUID_AND_ATTRIBUTES(luid.value, SE_PRIVILEGE_ENABLED))
            
            ctypes.windll.advapi32.AdjustTokenPrivileges(
                token_handle, False, ctypes.byref(new_privileges), 0, None, None
            )
            
            ctypes.windll.kernel32.CloseHandle(token_handle)
            self.add_log("✅ Privileges adjusted successfully")
            return True
        except Exception as e:
            self.add_log(f"❌ Failed to adjust privileges: {e}")
            return False
    
    def perform_aimbot_injection(self):
        """Main injection logic"""
        try:
            self.add_log("🔍 Starting injection process...")
            self.update_status("🔄 Injecting...", "#ffd700")
            
            # Adjust privileges
            if not self.adjust_privileges():
                self.update_status("❌ Privilege adjustment failed", "#ff4444")
                return False
            
            # Connect to process
            self.add_log("🔗 Connecting to HD-Player.exe...")
            self.pm = Pymem("HD-Player.exe")
            self.add_log("✅ Connected to HD-Player.exe")
            
            # Pattern for scanning
            pattern = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00................................\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xA5\x43..............................................................................................................................................................................................................................................\x80\xBF'
            
            self.add_log("🔎 Scanning for patterns...")
            addresses = pattern_scan_all(self.pm.process_handle, pattern, return_multiple=True)
            
            if not addresses:
                self.add_log("❌ No matching addresses found")
                self.update_status("❌ No addresses found", "#ff4444")
                return False
            
            self.add_log(f"✅ Found {len(addresses)} address(es)")
            
            # Process each address
            success_count = 0
            for i, addr in enumerate(addresses):
                try:
                    address_rep = addr + 0xAB
                    address_scan = addr + 0xAF
                    
                    original_rep = read_bytes(self.pm.process_handle, address_rep, 4)
                    original_scan = read_bytes(self.pm.process_handle, address_scan, 4)
                    
                    write_bytes(self.pm.process_handle, address_rep, original_scan, 4)
                    write_bytes(self.pm.process_handle, address_scan, original_rep, 4)
                    
                    success_count += 1
                    self.add_log(f"✅ Address {i+1} patched successfully")
                    
                except Exception as e:
                    self.add_log(f"⚠️ Address {i+1} failed: {e}")
            
            if success_count > 0:
                self.add_log(f"🎯 Injection complete! {success_count}/{len(addresses)} addresses patched")
                self.update_status("✅ Aimbot Activated!", "#00ff88")
                return True
            else:
                self.add_log("❌ No addresses were patched")
                self.update_status("❌ Injection failed", "#ff4444")
                return False
                
        except pymem.exception.ProcessNotFound:
            self.add_log("❌ HD-Player.exe not found! Make sure the game is running.")
            self.update_status("❌ Process not found", "#ff4444")
            return False
        except Exception as e:
            self.add_log(f"❌ Unexpected error: {e}")
            self.update_status("❌ Error occurred", "#ff4444")
            return False
        finally:
            if self.pm:
                self.pm.close_process()
                self.add_log("🔒 Process connection closed")
    
    def injection_worker(self):
        """Worker thread for injection"""
        self.inject_btn.config(state="disabled")
        self.progress.pack(pady=5)
        self.progress.start(10)
        
        result = self.perform_aimbot_injection()
        
        self.progress.stop()
        self.progress.pack_forget()
        self.inject_btn.config(state="normal")
        
        if result:
            self.is_injected = True
            self.inject_btn.config(text="✅ Aimbot Active", bg="#00cc88")
            messagebox.showinfo("Success", "Aimbot injected successfully! 🎯")
        else:
            self.inject_btn.config(text="🔄 Retry Injection", bg="#ff6b6b")
    
    def start_injection(self):
        """Start injection in a separate thread"""
        if self.is_injected:
            messagebox.showinfo("Info", "Aimbot is already active! ✅")
            return
            
        if self.is_injecting:
            return
            
        self.is_injecting = True
        thread = threading.Thread(target=self.injection_worker, daemon=True)
        thread.start()
        
    def on_closing(self):
        """Cleanup on close"""
        if self.pm:
            try:
                self.pm.close_process()
            except:
                pass
        self.root.destroy()


def main():
    # Check if running as admin on Windows
    if sys.platform == "win32":
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                # Re-run as admin
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit()
        except:
            pass
    
    root = tk.Tk()
    app = AimbotController(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()