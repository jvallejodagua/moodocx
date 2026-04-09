from typing import List, Literal, Union
from pydantic import BaseModel, Field
from typing_extensions import Annotated

class EvaluationElement(BaseModel):
    pass


class ContextText(EvaluationElement):
    element_type: Literal["texto_contexto"] = "texto_contexto"
    content: str = Field(
        ...,
        description = "Bloque de texto general que sirve de contexto o lectura. No tiene numeración de pregunta ni letra de opción."
    )


class QuestionPrompt(EvaluationElement):
    element_type: Literal["enunciado_pregunta"] = "enunciado_pregunta"
    question_number: int = Field(
        ...,
        description = "El número entero de la pregunta extraído del texto (ej. 1, 2, 3)."
    )
    content: str = Field(
        ...,
        description="El texto del enunciado de la pregunta. Se debe omitir el número inicial."
    )


class AnswerOption(EvaluationElement):
    element_type: Literal["opcion_respuesta"] = "opcion_respuesta"
    option_letter: str = Field(
        ...,
        description="La letra que identifica la opción de respuesta (ej. A, B, C, D)."
    )
    content: str = Field(
        ...,
        description="El texto de la opción de respuesta. Se debe omitir la letra inicial."
    )

EvaluationComponent = Annotated[
    Union[ContextText, QuestionPrompt, AnswerOption], 
    Field(discriminator="element_type")
]


class QuizDocumentModel(BaseModel):
    document_elements: List[EvaluationComponent] = Field(
        default_factory = list,
        description="Lista secuencial de todos los elementos del documento. Debes mantener el orden cronológico exacto en el que aparecen en el texto original."
    )

    def add_context_text(self, text_content: str) -> None:
        self.document_elements.append(
            ContextText(content=text_content)
        )

    def add_question_prompt(self, number: int, text_content: str) -> None:
        self.document_elements.append(
            QuestionPrompt(
                question_number=number,
                content=text_content
            )
        )

    def add_answer_option(self, letter: str, text_content: str) -> None:
        self.document_elements.append(
            AnswerOption(
                option_letter=letter,
                content=text_content
            )
        )

    def retrieve_all_elements(self) -> List[EvaluationComponent]:
        return self.document_elements