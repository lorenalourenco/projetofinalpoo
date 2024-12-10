import os
import subprocess

class DiagramGenerator:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.output_dir = os.path.join(source_dir, 'diagrams')
        self.dot_path = os.path.join(self.output_dir, 'classes.dot')

    def generate_diagram(self):
        os.makedirs(self.output_dir, exist_ok=True)
        command = f"pyreverse -o dot -p Diagrams {self.source_dir}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Erro ao gerar diagrama: {result.stderr}")
        return self.dot_path
