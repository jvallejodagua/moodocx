# -*- coding: utf-8 -*-
# template_compiler_model.py

from typing import Any, Dict, Tuple, List
from pydantic import BaseModel, Field

class TemplateCompilerFunction(BaseModel):
    function_name: str = Field(
        ..., 
        description="Nombre de la función a ejecutar"
    )
    args: Tuple[Any, ...] = Field(
        default_factory=tuple, 
        description="Argumentos posicionales"
    )
    kwargs: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Argumentos nombrados"
    )

class TemplateCompilerTask(BaseModel):
    task_id: str = Field(
        ..., 
        description="Identificador único de la tarea"
    )
    functions: List[TemplateCompilerFunction]