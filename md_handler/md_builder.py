# -*- coding: utf-8 -*-
# md_builder.py

import json
from typing import Dict, Any, List

class MdBuilder:
    def __init__(self, ai_response_dict: Dict[str, Any]):
        self.ai_response_dict = ai_response_dict

    def _extract_document_elements(self) -> List[Dict[str, Any]]:
        raw_content = self.ai_response_dict.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if not raw_content:
            return []
            
        try:
            parsed_content = json.loads(raw_content)
            return parsed_content.get("document_elements", [])
        except json.JSONDecodeError:
            raise ValueError("El contenido extraído de la IA no es un JSON válido.")

    def generate_markdown(self) -> str:
        elements = self._extract_document_elements()
        formatted_lines = []
        previous_element_type = None

        for element in elements:
            current_type = element.get("element_type")
            
            if current_type == "texto_contexto":
                if previous_element_type in ["opcion_respuesta", "enunciado_pregunta"]:
                    formatted_lines.append("")
                
                formatted_lines.append(element.get("content", ""))
                formatted_lines.append("")
                
            elif current_type == "enunciado_pregunta":
                if previous_element_type is not None:
                    formatted_lines.append("")
                
                question_number = element.get("question_number", "")
                content = element.get("content", "")
                formatted_lines.append(f"{question_number}. {content}")
                
            elif current_type == "opcion_respuesta":
                option_letter = element.get("option_letter", "")
                content = element.get("content", "")
                formatted_lines.append(f"{option_letter}. {content}")
            
            previous_element_type = current_type

        raw_markdown = "\n".join(formatted_lines)
        clean_markdown = raw_markdown.replace("\n\n\n", "\n\n").strip()
        
        return clean_markdown