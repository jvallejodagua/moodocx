# -*- coding: utf-8 -*-
# ia_md_formatter.py

from llama_cpp import Llama
from pathlib import Path

class IAMdFormatter:

    def __init__(self, model_path):
        
        self.model_path = model_path / "gemma_2b_it_Q4_K_M.gguf"

        self.ia_model = Llama(
            model_path=str(self.model_path), 
            n_ctx=8192, # Memoria de contexto
            verbose=False)

    def parse_prompt(self, prompt_input):
        pass

    def parse_md_text(self, md_text):
        pass
    
    def example(self):
        prompt = "Escribe un bucle for en bash."
        print(f"Usuario: {prompt}")

        salida = self.ia_model(
            f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n", 
            max_tokens=256, 
            stop=["<end_of_turn>"]
        )

        print(f"Gemma:\n{salida['choices'][0]['text']}")

if __name__ == "__main__":
    model_path = Path("/home/johan/RepositoriosGithub/moodocx")
    ia_md_formatter = IAMdFormatter(model_path)
    ia_md_formatter.example()
