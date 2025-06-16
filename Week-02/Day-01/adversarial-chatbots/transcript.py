
from pathlib import Path

class Transcript:
    def __init__(self, file_path):
        self.path = Path(file_path)
        self.encoding ="utf-8"
        
        #####################################################
        # Start with a new transcript upon each instantiation
        #####################################################
        self.path.write_text("")  
    
    def log(self, role, turn, message):
        with self.path.open("a", encoding=self.encoding) as f:
            f.write(f"[{turn}] {role}:\n{message}\n")