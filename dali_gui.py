import tkinter as tk
from tkinter import scrolledtext
import sys
import os
from threading import Thread
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dali import Dali
from wake_word_detector import WakeWordDetector

class DaliGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 DALI - Always Listening")
        self.root.geometry("800x900")
        self.root.configure(bg="#0a0e27")
        
        self.dali = None
        self.wake_detector = None
        self.is_running = False
        self.is_active = False
        self.thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="🤖 DALI",
            font=("Arial", 36, "bold"),
            bg="#0a0e27",
            fg="#00d4ff"
        )
        title.pack(pady=15)
        
        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="Dynamic AI Listening Interface",
            font=("Arial", 12),
            bg="#0a0e27",
            fg="#888888"
        )
        subtitle.pack()
        
        # Status indicators frame
        status_frame = tk.Frame(self.root, bg="#0a0e27")
        status_frame.pack(pady=15)
        
        # Running status
        tk.Label(status_frame, text="Application:", font=("Arial", 11, "bold"), bg="#0a0e27", fg="#ffffff").pack(side=tk.LEFT, padx=10)
        self.app_status_label = tk.Label(
            status_frame,
            text="● Offline",
            font=("Arial", 11, "bold"),
            bg="#0a0e27",
            fg="#ff4444"
        )
        self.app_status_label.pack(side=tk.LEFT, padx=5)
        
        # Active status
        tk.Label(status_frame, text="  |  Listening:", font=("Arial", 11, "bold"), bg="#0a0e27", fg="#ffffff").pack(side=tk.LEFT, padx=10)
        self.listen_status_label = tk.Label(
            status_frame,
            text="● Waiting",
            font=("Arial", 11, "bold"),
            bg="#0a0e27",
            fg="#ffaa00"
        )
        self.listen_status_label.pack(side=tk.LEFT, padx=5)
        
        # Conversation display
        frame = tk.Frame(self.root, bg="#0a0e27")
        frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            frame,
            text="💬 Conversation:",
            font=("Arial", 12, "bold"),
            bg="#0a0e27",
            fg="#ffffff"
        ).pack(anchor="w")
        
        self.text_area = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=80,
            height=24,
            font=("Courier", 10),
            bg="#1a1f3a",
            fg="#00ff00",
            insertbackground="#00ff00",
            state='disabled'
        )
        self.text_area.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Configure text tags
        self.text_area.tag_config("dali", foreground="#00d4ff")
        self.text_area.tag_config("user", foreground="#ffaa00")
        self.text_area.tag_config("system", foreground="#88ff88")
        self.text_area.tag_config("error", foreground="#ff4444")
        self.text_area.tag_config("wake", foreground="#ff00ff")
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="#0a0e27")
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="▶ START LISTENING",
            font=("Arial", 12, "bold"),
            bg="#00cc44",
            fg="white",
            width=20,
            height=2,
            command=self.start_app,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹ STOP",
            font=("Arial", 12, "bold"),
            bg="#ff4444",
            fg="white",
            width=20,
            height=2,
            command=self.stop_app,
            state='disabled',
            cursor="hand2",
            relief=tk.FLAT
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # Info
        info_text = "🎤 Just say: 'Dali', 'Hey Dali', 'Dali Wake Up', or 'Hey Darling' to start!"
        info = tk.Label(
            self.root,
            text=info_text,
            font=("Arial", 10),
            bg="#0a0e27",
            fg="#666666",
            wraplength=700
        )
        info.pack(pady=10)
        
    def log_message(self, message, tag="system"):
        """Add message to conversation"""
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n", tag)
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')
        self.root.update()
        
    def start_app(self):
        """Start background listening"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.app_status_label.config(text="● Online", fg="#00cc44")
            self.listen_status_label.config(text="● Waiting for wake word", fg="#ffaa00")
            
            self.log_message("\n" + "="*70, "system")
            self.log_message("🤖 DALI LISTENING MODE ACTIVATED", "system")
            self.log_message("Say: 'Dali' or 'Hey Dali' to wake me up!", "system")
            self.log_message("="*70 + "\n", "system")
            
            self.thread = Thread(target=self.run_app, daemon=True)
            self.thread.start()
    
    def stop_app(self):
        """Stop listening"""
        if self.is_running:
            self.is_running = False
            if self.wake_detector:
                self.wake_detector.stop()
            if self.dali:
                self.dali.is_running = False
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.app_status_label.config(text="● Offline", fg="#ff4444")
            self.listen_status_label.config(text="● Stopped", fg="#999999")
            self.is_active = False
            self.log_message("\n🛑 DALI STOPPED\n", "system")
    
    def on_wake_word_detected(self, recognized_text):
        """Called when wake word is detected"""
        if self.is_running and not self.is_active:
            self.is_active = True
            self.listen_status_label.config(text="● ACTIVE - Processing command", fg="#00ff00")
            self.log_message(f"\n✨ WAKE WORD DETECTED: '{recognized_text}'", "wake")
            self.root.update()
            
            # Start active listening mode
            self.thread = Thread(target=self.run_active_mode, daemon=True)
            self.thread.start()
    
    def run_app(self):
        """Run background listener"""
        try:
            from wake_word_detector import WakeWordDetector
            
            # Create wake word detector
            self.wake_detector = WakeWordDetector(
                callback=self.on_wake_word_detected
            )
            
            self.wake_detector.start()
            
            # Keep running
            while self.is_running:
                time.sleep(1)
                
        except Exception as e:
            self.log_message(f"❌ Error: {e}", "error")
            self.root.after(1000, self.stop_app)
    
    def run_active_mode(self):
        """Run Dali in active mode after wake word detected"""
        try:
            from dali import Dali
            
            if self.dali is None:
                self.dali = Dali()
            
            # Override speak method
            original_speak = self.dali.voice.speak
            def gui_speak(text):
                self.root.after(0, self.log_message, f"🤖 Dali: {text}", "dali")
                try:
                    original_speak(text)
                except Exception as e:
                    self.log_message(f"❌ TTS Error: {e}", "error")
            
            self.dali.voice.speak = gui_speak
            
            # Override listen
            original_listen = self.dali.voice.listen
            def gui_listen(*args, **kwargs):
                text = original_listen(*args, **kwargs)
                if text:
                    self.root.after(0, self.log_message, f"👤 You: {text}", "user")
                return text
            
            self.dali.voice.listen = gui_listen
            
            # Now listen for the actual command
            self.log_message("\n🎤 Listening for your command...", "system")
            
            cmd_text = self.dali.voice.listen(timeout=20, phrase_time_limit=10)
            
            if cmd_text:
                # Process the command
                self.log_message(f"✅ Processing: '{cmd_text}'", "system")
                
                intent_type, data = self.dali.intent.classify_intent(cmd_text)
                response = self.dali.action.execute_action(intent_type, data)
                
                if response == "exit":
                    self.dali.voice.speak("Goodbye!")
                    self.root.after(500, self.stop_app)
                elif response:
                    self.dali.voice.speak(response)
                else:
                    self.dali.voice.speak("I didn't understand. Please try again.")
            
            # Back to waiting
            self.is_active = False
            self.listen_status_label.config(text="● Waiting for wake word", fg="#ffaa00")
            self.log_message("\n💡 Ready for next command...\n", "system")
            
        except Exception as e:
            self.log_message(f"❌ Error: {e}", "error")
            self.is_active = False
            self.listen_status_label.config(text="● Waiting for wake word", fg="#ffaa00")
if __name__ == "__main__":
    root = tk.Tk()
    app = DaliGUI(root)
    root.mainloop()
