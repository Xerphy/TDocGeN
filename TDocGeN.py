
from dataclasses import dataclass, field
from typing import List
from datetime import date

from docxtpl import DocxTemplate
from jinja2 import Environment, StrictUndefined

# helpers

def normalize_text(value):
    """
    limpia texto para docxtpl
    """
    if value is None:
        return ""

    return str(value).strip()


def list_to_multiline(value: list[str]) -> str:
    """
    convierte listas en texto multilinea
    """
    if not value:
        return ""

    return "\n".join(
        f"• {normalize_text(v)}"
        for v in value
    )


def safe_upper(value: str) -> str:
    """
    uppercase seguro SOLO para headers cortos
    """
    if not isinstance(value, str):
        return value

    return value.upper()

# modelos

@dataclass
class Practica:

    nombre: str
    numero: str

    competencia: str = ""

    material: List[str] = field(default_factory=list)

    marco_teorico: str = ""

    desarrollo: str = ""

    cuestionario: List[str] = field(default_factory=list)

    conclusiones: str = ""

    aplicaciones: List[str] = field(default_factory=list)

    referencias: List[str] = field(default_factory=list)

    criterios: str = ""

    @classmethod
    def quick(cls, numero, nombre):
        return cls(
            nombre=nombre,
            numero=numero
        )

    def update_from_dict(self, data: dict):

        valid_fields = self.__dataclass_fields__

        for key, value in data.items():

            if key not in valid_fields:
                continue

            setattr(self, key, value)

        return self

    def to_docx_dict(self):

        return {
            "nombre": normalize_text(self.nombre),

            "numero": normalize_text(self.numero),

            "competencia": normalize_text(
                self.competencia
            ),

            "material": list_to_multiline(
                self.material
            ),

            "marco_teorico": normalize_text(
                self.marco_teorico
            ),

            "desarrollo": normalize_text(
                self.desarrollo
            ),

            "cuestionario": list_to_multiline(
                self.cuestionario
            ),

            "conclusiones": normalize_text(
                self.conclusiones
            ),

            "aplicaciones": list_to_multiline(
                self.aplicaciones
            ),

            "referencias": list_to_multiline(
                self.referencias
            ),

            "criterios": normalize_text(
                self.criterios
            ),
        }


@dataclass
class Manual:

    division: str = ""

    tipo: str = ""

    asignatura: str = ""

    elaboro: List[str] = field(default_factory=list)

    emision: str = ""

    edicion: str = ""

    vigencia: str = ""

    practicas: List[Practica] = field(default_factory=list)

    presentacion: str = ""

    reglamento: str = ""

    @property
    def num_practicas(self):
        return len(self.practicas)

    @property
    def index(self):
        return {
            practica.nombre: practica.numero
            for practica in self.practicas
        }

    def agregar_practica(self, practica: Practica):
        self.practicas.append(practica)

    def validate(self):

        missing = []

        context = self.to_docx_context()

        for key, value in context.items():

            if value in ("", [], None):
                missing.append(key)

        return missing

    def to_docx_context(self):

        return {

            "division": safe_upper(
                self.division
            ),

            "tipo": safe_upper(
                self.tipo
            ),

            "asignatura": safe_upper(
                self.asignatura
            ),

            "num_practicas": self.num_practicas,

            "elaboro": "\n".join(
                safe_upper(x)
                for x in self.elaboro
            ),

            "emision": self.emision,

            "edicion": self.edicion,

            "vigencia": self.vigencia,

            "presentacion": normalize_text(
                self.presentacion
            ),

            "reglamento": normalize_text(
                self.reglamento
            ),

            "practicas": [
                p.to_docx_dict()
                for p in self.practicas
            ]
        }


# render 

class ManualRenderer:

    def __init__(self, template_path: str):

        self.template_path = template_path

    def render(
        self,
        manual: Manual,
        output_path: str = "informe.docx"
    ):

        context = manual.to_docx_context()

        missing = manual.validate()

        if missing:
            print(
                "[WARNING] Campos vacíos:",
                missing
            )

        doc = DocxTemplate(
            self.template_path
        )

        jinja_env = Environment(
            undefined=StrictUndefined,
            autoescape=True
        )

        doc.render(
            context,
            jinja_env=jinja_env
        )

        doc.save(output_path)

        print(
            f"[OK] Documento generado: {output_path}"
        )

        return output_path

# no hay ejemplo, solo se va a usar como libreria

if __name__ == "__main__":
    pass