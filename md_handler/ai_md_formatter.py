# -*- coding: utf-8 -*-
# ai_md_formatter.py

from llama_cpp import Llama
from pathlib import Path
from quiz_document_model import QuizDocumentModel
from md_builder import MdBuilder
import json

class AIMdFormatter:

    def __init__(self, model_path):
        
        self.model_path = model_path / "google_gemma_4_26B_A4B_it_Q4_K_M.gguf"
        #self.model_path = model_path / "google_gemma_4_E4B_it_Q5_K_M.gguf"
        
        #gemma_4_E4B
        #self.max_tokens = 16384
        #gemma_4_26B
        self.max_tokens = 16384

        self.ia_model = Llama(
            model_path = str(self.model_path),
            top_p = 0.1,
            top_k = 10,
            temp = 0.0,
            repeat_penalty = 1.15,
            n_threads=4,
            n_ctx = self.max_tokens,
            use_mlock = True,
            verbose = False)
        self.md_text = ""
        
    def get_formatted_text(self, prompt):

        system_content = (
            "Eres un procesador de datos estricto. Tu tarea es convertir TODO el texto de entrada a un JSON estructurado, "
            "manteniendo el orden secuencial EXACTO del documento original. NO DEBES OMITIR NINGÚN PÁRRAFO, TÍTULO O INSTRUCCIÓN.\n\n"
            "Reglas de clasificación obligatorias y exhaustivas:\n"
            "1. TEXTO DE CONTEXTO ('texto_contexto'): Esta es la categoría por defecto. Cualquier título (ej. 'EVALUACIÓN...'), "
            "instrucción, o párrafo de lectura (ej. la historia) que NO sea una pregunta ni una opción, DEBE registrarse aquí. "
            "Mantén el texto exacto.\n"
            "2. ENUNCIADO DE PREGUNTA ('enunciado_pregunta'): Inician obligatoriamente con un número (ej. '1.', '2)'). "
            "Extrae el número en 'question_number' y elimina ese número del texto en 'content'.\n"
            "3. OPCIÓN DE RESPUESTA ('opcion_respuesta'): Inician obligatoriamente con una letra (ej. 'A)', 'B.'). "
            "Extrae la letra en 'option_letter' y elimina esa letra del texto en 'content'."
        )

        messages = [
            {"role": "system", "content": system_content},
            # --- INICIO DEL FEW-SHOT ---
            {"role": "user", "content": "Estructura el siguiente texto:\n**Examen de Ciencias**\nLee esto:\nEl sol es una estrella.\n1. ¿Qué es el sol?\nA) Un planeta\nB) Una estrella"},
            {"role": "assistant", "content": "{\"document_elements\": [{\"content\": \"**Examen de Ciencias**\", \"element_type\": \"texto_contexto\"}, {\"content\": \"Lee esto:\\nEl sol es una estrella.\", \"element_type\": \"texto_contexto\"}, {\"question_number\": 1, \"content\": \"¿Qué es el sol?\", \"element_type\": \"enunciado_pregunta\"}, {\"option_letter\": \"A\", \"content\": \"Un planeta\", \"element_type\": \"opcion_respuesta\"}, {\"option_letter\": \"B\", \"content\": \"Una estrella\", \"element_type\": \"opcion_respuesta\"}]}"},
            # --- FIN DEL FEW-SHOT ---
            {"role": "user", "content": prompt},
        ]

        quiz_document_model = QuizDocumentModel.model_json_schema()
        #print(json.dumps(quiz_document_model, indent=4, ensure_ascii=False))

        quiz_output_format = {
            "type": "json_object",
            "schema": quiz_document_model
        }
        
        ai_response = self.ia_model.create_chat_completion(
            messages = messages,
            response_format = quiz_output_format,
            max_tokens = 8192,
            #tokenize = False,
            #add_generation_prompt = True,
            #enable_thinking = False,
        )

        self.write_debug_file(json.dumps(ai_response))

        md_builder = MdBuilder(ai_response)
        
        return md_builder.generate_markdown()
    
    def write_debug_file(self, text):
        output_file = Path("/home/johan/RepositoriosGithub/moodocx/Temporales/EvaluacionCopiada.json")
        with open(output_file, 'w', encoding = 'utf-8') as f2:
            f2.write(text)

if __name__ == "__main__":
    model_path = Path("/home/johan/RepositoriosGithub/moodocx")
    ia_md_formatter = AIMdFormatter(model_path)
    file = Path("/home/johan/RepositoriosGithub/moodocx/Temporales/EvaluacionCopiada.md")
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    text_md = ia_md_formatter.get_formatted_text(content)
    
    output_file = Path("/home/johan/RepositoriosGithub/moodocx/Temporales/EvaluacionCopiada-formateada.md")
    with open(output_file, 'w', encoding = 'utf-8') as f2:
        f2.write(text_md)
    #ia_md_formatter.example()
