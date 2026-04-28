# -*- coding: utf-8 -*-
# ai_md_formatter.py

from llama_cpp import Llama
from pathlib import Path
from md_handler.quiz_document_model import QuizDocumentModel
from md_handler.md_builder import MdBuilder
import json

class AIMdFormatter:

    def __init__(self, model_path):

        #self.model_path = model_path / "Qwen2.5_Coder_14B_Instruct_Q5_K_M.gguf"
        #self.model_path = model_path / "google_gemma_4_26B_A4B_it_Q4_K_M.gguf" #26B 15.9Gb
        #self.model_path = model_path / "google_gemma_4_E4B_it_Q5_K_M.gguf" #8B 5.4Gb
        #self.model_path = model_path / "google_gemma_4_E2B_it_Q4_K_M.gguf" #5B 3.2Gb
        #self.model_path = model_path / "google_gemma_3n_E2B_it_Q4_K_M.gguf" #4B 2.6Gb
        #self.model_path = model_path / "google_gemma_4_E4B_it_Q8_0.gguf" #8B 7.5Gb
        self.model_path = model_path / "Agente_GPT_Qwen_2.5_7B_Spanish_16bit.Q4_K_M.gguf"


        self.md_handler_path = self.model_path.parent / "md_handler"

        #Una evaluación suele contenerse bien en 8192/2 tokens
        self.max_tokens = 16384

        #n_gpu_layers para nvidia gtx 1060 3Gb
        self.ia_model = Llama(
            model_path = str(self.model_path),
            seed = 13,
            top_p = 0.8,
            top_k = 40, #10 - 40
            temp = 0.1,
            chat_format = "chatml", #Qwen
            repeat_penalty = 1.0,
            n_threads=4,
            n_gpu_layers=0, #=6 4B 2.6Gb =0 5B 3.2Gb =0 26B 15.9Gb
            presence_penalty= 0.0,
            #n_batch = 128,
            n_ctx = self.max_tokens,
            #use_mlock = True,
            verbose = False)
        self.system_prompt = ""
        self.content_example1 = ""
        self.expected_output1 = ""
        self.messages = []

    def get_formatted_text_qwen(self, prompt):

        self.set_model_prompt_setup(prompt)

        quiz_document_model = QuizDocumentModel.model_json_schema()

        quiz_output_format = {
            "type": "json_object",
            "schema": quiz_document_model
        }
        
        ai_response = self.ia_model.create_chat_completion(
            messages = self.messages,
            response_format = quiz_output_format,
            max_tokens = int(self.max_tokens/2), 
        )

        #self.write_debug_file(json.dumps(ai_response))

        md_builder = MdBuilder(ai_response)
        
        return md_builder.generate_markdown()

    def get_formatted_text_gemma(self, prompt):
        
        self.set_model_prompt_setup(prompt)

        '''
        Se comprobó bajo nivel de precisión.
        Se prueba un formato abierto.
        quiz_document_model = QuizDocumentModel.model_json_schema()

        quiz_output_format = {
            "type": "json_object",
            "schema": quiz_document_model
        }
        '''
        ai_response = self.ia_model.create_chat_completion(
            messages = self.messages,
            #response_format = quiz_output_format,
            max_tokens = int(self.max_tokens/2),
        )

        #self.write_debug_file(json.dumps(ai_response))

        #md_builder = MdBuilder(ai_response)
        
        return ai_response['choices'][0]['message']['content']

    def set_model_prompt_setup(self, prompt):
        system_prompt_path = self.md_handler_path / "system_prompt.md"
        self.system_prompt = "Eres un asistente muy ayudador"
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()

        content_example1_path = self.md_handler_path / "example1.md"
        with open(content_example1_path, 'r', encoding='utf-8') as f:
            self.content_example1 = f.read()

        expected_output1_path = self.md_handler_path / "expected_output1.md"
        with open(expected_output1_path, 'r', encoding='utf-8') as f:
            self.expected_output1 = f.read()        

        content_example2_path = self.md_handler_path / "example2.md"
        with open(content_example2_path, 'r', encoding='utf-8') as f:
            self.content_example2 = f.read()

        expected_output2_path = self.md_handler_path / "expected_output2.md"
        with open(expected_output2_path, 'r', encoding='utf-8') as f:
            self.expected_output2 = f.read()        

        self.messages = [
            {"role": "system", "content": self.system_prompt},
            # --- Ejemplo few-shot ---
            {"role": "user", "content": self.content_example1},
            {"role": "assistant", "content": self.expected_output1},
            {"role": "user", "content": self.content_example2},
            {"role": "assistant", "content": self.expected_output2},
            # --- Fin del ejemplo ---
            {"role": "user", "content": prompt},
        ]