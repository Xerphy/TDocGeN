"""
TDocGeN — Generador de Manuales de Prácticas TESJo
Streamlit app · Step-based workflow
"""

import json
import os
import re
import tempfile
import traceback
import hashlib
from datetime import datetime
import streamlit as st

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="TDocGeN",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Reset & base */
html, body, .stApp {
    font-family: 'Inter', sans-serif;
}

/* App background */
.stApp {
    background-color: #0D1117;
    color: #E6EDF3;
}

/* Main block container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 960px;
}

/* ── Step nav rail ── */
.step-rail {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 2.5rem;
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 1rem 1.5rem;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
    cursor: pointer;
}
.step-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    flex-shrink: 0;
    transition: all .2s;
}
.step-dot.active {
    background: #4F8EF7;
    box-shadow: 0 0 16px #4F8EF755;
    color: #fff;
}
.step-dot.done {
    background: #238636;
    color: #fff;
}
.step-dot.idle {
    background: #21262D;
    border: 2px solid #30363D;
    color: #8B949E;
}
.step-label {
    font-size: 13px;
    font-weight: 500;
    color: #E6EDF3;
}
.step-label.idle { color: #8B949E; }
.step-connector {
    width: 32px;
    height: 2px;
    background: #30363D;
    flex-shrink: 0;
    margin: 0 4px;
}
.step-connector.done { background: #238636; }

/* ── Section title ── */
.section-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #4F8EF7;
    margin-bottom: .5rem;
}

/* ── Card ── */
.doc-card {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* ── Practice card ── */
.practice-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: .5rem;
}
.practice-badge {
    background: #4F8EF722;
    border: 1px solid #4F8EF755;
    color: #4F8EF7;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 12px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.practice-title {
    font-size: 15px;
    font-weight: 600;
    color: #E6EDF3;
}

/* ── Prompt area ── */
.prompt-box {
    background: #0D1117;
    border: 1px solid #4F8EF755;
    border-radius: 8px;
    padding: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #79C0FF;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 300px;
    overflow-y: auto;
    margin-top: .5rem;
}

/* ── Status badges ── */
.badge-ok {
    background: #23863622;
    border: 1px solid #23863655;
    color: #3FB950;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}
.badge-warn {
    background: #9E6A0322;
    border: 1px solid #9E6A0355;
    color: #D29922;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    background: #0D1117 !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
    color: #F8FAFC !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea textarea::placeholder {
    color: #A5B3C6 !important;
    opacity: 1 !important;
}
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stNumberInput label {
    color: #F8FAFC !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus,
.stSelectbox > div > div:focus {
    border-color: #4F8EF7 !important;
    box-shadow: 0 0 0 3px #4F8EF715 !important;
}

/* ── Buttons FIX (dark theme safe) ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    transition: all .15s !important;

    background-color: #21262D !important;
    color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
}

/* hover */
.stButton > button:hover {
    background-color: #30363D !important;
    transform: translateY(-1px);
}

/* primary buttons (Streamlit real selector) */
.stButton > button[data-baseweb="button"] {
    color: #E6EDF3 !important;
}

/* override primary via aria */
.stButton > button[aria-pressed="true"] {
    background: #4F8EF7 !important;
    color: #ffffff !important;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #21262D;
    margin: 1.5rem 0;
}

/* ── expander ── */
.streamlit-expanderHeader,
.stExpanderHeader,
.stExpander > div,
div[class*="stExpander"] > button,
div[class*="stExpander"] > button span,
div[class*="stExpander"] > button div,
.stExpanderHeader button,
.stExpanderHeader button span,
.stExpanderHeader span,
.streamlit-expanderHeader * {
    color: #E6EDF3 !important;
}

.streamlit-expanderHeader,
.stExpanderHeader,
.stExpander > div,
div[class*="stExpander"] > button,
div[class*="stExpander"] > button span,
div[class*="stExpander"] > button div,
.stExpanderHeader button,
.stExpanderHeader button span,
.stExpanderHeader span {
    background: #161B22 !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
}

div[class*="stExpander"] > button,
.stExpanderHeader button,
.streamlit-expanderHeader button {
    background: #161B22 !important;
    color: #E6EDF3 !important;
}

div[class*="stExpander"] > button:hover,
.stExpanderHeader button:hover,
.streamlit-expanderHeader button:hover {
    background: #131720 !important;
    color: #E6EDF3 !important;
}

div[class*="stExpander"] > button span,
.stExpanderHeader button span,
.streamlit-expanderHeader button span {
    color: #E6EDF3 !important;
}

div[class*="stExpander"] > button {
    background: #161B22 !important;
}

div[class*="stExpander"] > button:hover {
    background: #131720 !important;
}

/* Subtle label */
.field-hint {
    font-size: 13px;
    color: #C3D0E0;
    margin-top: -6px;
    margin-bottom: 10px;
    line-height: 1.45;
}

/* Progress bar */
.stProgress > div > div {
    background: #4F8EF7 !important;
    border-radius: 4px !important;
}

/* ── Download success banner ── */
.download-banner {
    background: #0D2818;
    border: 1px solid #238636;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 1rem;
}
.download-banner .db-icon { font-size: 22px; }
.download-banner .db-text { flex: 1; }
.download-banner .db-title {
    font-size: 14px;
    font-weight: 600;
    color: #3FB950;
}
.download-banner .db-sub {
    font-size: 12px;
    color: #8B949E;
    margin-top: 2px;
}

/* ── Download button override ── */
[data-testid="stDownloadButton"] > button {
    background: #238636 !important;
    border: 1px solid #2EA043 !important;
    color: #000 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    width: 100% !important;
    padding: .6rem 1rem !important;
    font-size: 14px !important;
    transition: all .15s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #2EA043 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px #23863644 !important;
}

/* ── Spinner text ── */
.stSpinner > div {
    border-color: #4F8EF7 !important;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  DEFAULT CONTENT
# ─────────────────────────────────────────────────────────────

DEFAULT_REGLAMENTO = """REGLAMENTO INTERNO DE LAS SALAS DE CÓMPUTO

CAPÍTULO I
GENERALIDADES

Artículo 1. El presente ordenamiento tiene por objeto reglamentar la organización y funcionamiento de las Salas de Cómputo del Instituto Tecnológico Superior de Jocotitlán (TESJo), con la finalidad de brindar un servicio eficiente y de calidad a la comunidad estudiantil y docente.

Artículo 2. Las disposiciones del presente reglamento son de observancia obligatoria para todos los usuarios de las Salas de Cómputo: estudiantes, docentes, personal administrativo e investigadores.

Artículo 3. Para efectos del presente reglamento se entenderá por:
I. Instituto: Instituto Tecnológico Superior de Jocotitlán.
II. Sala de Cómputo: Espacio físico equipado con equipo de cómputo destinado al aprendizaje y práctica de los estudiantes.
III. Usuario: Toda persona autorizada para hacer uso de las instalaciones.
IV. Administrador: Personal responsable del control, mantenimiento y supervisión de las Salas de Cómputo.

CAPÍTULO II
DE LOS DERECHOS Y OBLIGACIONES DE LOS USUARIOS

Artículo 4. Son derechos de los usuarios:
I. Hacer uso del equipo de cómputo disponible conforme a los horarios establecidos.
II. Recibir orientación y apoyo técnico básico del personal responsable.
III. Acceder a los recursos de software e internet disponibles para fines académicos.
IV. Solicitar la atención de fallas técnicas al personal responsable.

Artículo 5. Son obligaciones de los usuarios:
I. Presentar credencial institucional vigente para el acceso a las instalaciones.
II. Registrarse en la bitácora de uso al ingresar y al salir.
III. Hacer uso adecuado del equipo y las instalaciones.
IV. Respetar los horarios establecidos por la administración.
V. Mantener el orden y el silencio dentro de las instalaciones.
VI. Reportar inmediatamente al personal responsable cualquier desperfecto o anomalía detectada en el equipo.

CAPÍTULO III
DE LAS PROHIBICIONES

Artículo 6. Queda estrictamente prohibido a los usuarios:
I. Consumir alimentos, bebidas o cualquier tipo de sustancia dentro de las Salas de Cómputo.
II. Introducir o ejecutar programas no autorizados por la administración.
III. Modificar la configuración del sistema operativo o de los programas instalados.
IV. Utilizar el equipo con fines distintos a los académicos o institucionales.
V. Acceder a sitios de internet con contenido inapropiado, ilegal o contrario a la ética institucional.
VI. Reproducir música, videos o cualquier contenido multimedia a un volumen que perturbe a los demás usuarios.
VII. Dañar intencionalmente el equipo, mobiliario o instalaciones.
VIII. Sustraer equipo, componentes, materiales o accesorios pertenecientes al Instituto.
IX. Ceder el uso del equipo a personas no autorizadas.
X. Utilizar dispositivos de almacenamiento externo sin previa autorización del administrador.

CAPÍTULO IV
DE LAS SANCIONES

Artículo 7. El incumplimiento de las disposiciones del presente reglamento dará lugar a las siguientes sanciones, dependiendo de la gravedad de la falta:
I. Amonestación verbal.
II. Amonestación escrita con copia al expediente del alumno.
III. Suspensión temporal del derecho de acceso a las Salas de Cómputo.
IV. Suspensión definitiva del derecho de acceso a las Salas de Cómputo.
V. En casos de daño al patrimonio institucional, el usuario será responsable de la reparación o reposición del bien dañado, además de las sanciones disciplinarias correspondientes.

CAPÍTULO V
DISPOSICIONES FINALES

Artículo 8. Los casos no previstos en el presente reglamento serán resueltos por la Jefatura de División correspondiente, en coordinación con la Dirección Académica del Instituto.

Artículo 9. El presente reglamento entrará en vigor al momento de su publicación y difusión oficial por parte de las autoridades del Instituto.
"""

PROMPT_TEMPLATE = """You are an expert academic content generator specialized in higher technical education.

Your task is to produce a single valid JSON object describing one laboratory practice for a higher education engineering or technology course.

INPUT DATA:
  Name:    {nombre}
  Number:  {numero}
  Subject: {asignatura}

OUTPUT REQUIREMENTS:
- Return ONLY one valid JSON object.
- No markdown, no code fences, no comments, no extra text.
- Use strict JSON syntax: double quotes only, no trailing commas, no unquoted keys.
- Do not include any keys beyond the required fields.
- Perform a SELF-VALIDATION step before returning. Ensure the JSON is parseable and contains all required keys.
- Write in formal academic English with technical precision and detail.
- Respond always in Spanish.

IEEE CITATION REQUIREMENTS:
- All references must follow IEEE citation style.
- References must be real academic sources, ideally from 2018-2024.
- Provide at least 10 unique IEEE references.
- Cite references inside the theoretical_framework using bracket notation: [1], [2], [3], etc.

CONTENT DEPTH REQUIREMENTS:
- theoretical_framework must contain a minimum of 10 well-structured paragraphs.
- Include historical context, core theoretical principles, formal definitions, mathematical or algorithmic foundations, standards or protocols, recent research findings, and real-world applications.
- Provide at least 20 higher-order questions in the questionnaire.
- Each questionnaire entry must include both the question and its answer in a single string, clearly separated.
- Do not use the format "pregunta 1: respuesta" or "pregunta2, respuesta".
- Instead use the format:
  pregunta
  respuesta
- Use a formal academic tone throughout.

JSON STRUCTURE (STRICT — return ONLY this object):
{{
  "name": "{nombre}",
  "number": "{numero}",
  "competency": "<Detailed competency statement (2-4 sentences). Include measurable performance verbs, operating conditions, and evaluation criteria aligned with Bloom's taxonomy.>",
  "materials": [
    "<Hardware / software / resource 1>",
    "<Hardware / software / resource 2>",
    "<Hardware / software / resource 3>"
  ],
  "theoretical_framework": "<EXTENSIVE theoretical framework — minimum 6 to 10 well-structured paragraphs. Cover historical context, core theoretical principles, mathematical or algorithmic foundations where applicable, key standards or protocols, state-of-the-art research findings with IEEE-style citations such as [1] and [2], and real-world engineering applications. Use precise academic English throughout.>",
  "questionnaire": [
    "<Higher-order critical thinking question 1 — analysis or evaluation level>",
    "<Higher-order critical thinking question 2 — synthesis or design level>",
    "<Higher-order critical thinking question 3 — application level>",
    "<Higher-order critical thinking question 4 — comparison or contrast level>",
    "<Higher-order critical thinking question 5 — reflection or future-work level>"
  ],
  "applications": [
    "<Concrete real-world industry application 1 with brief technical justification>",
    "<Concrete real-world industry application 2 with brief technical justification>",
    "<Concrete real-world industry application 3 with brief technical justification>"
  ],
  "references": [
    "<Full IEEE-style reference 1 — journal article or conference paper, 2018-2024>",
    "<Full IEEE-style reference 2 — textbook or standard, authoritative source>",
    "<Full IEEE-style reference 3 — additional peer-reviewed source>"
  ]
}}"""

# ─────────────────────────────────────────────────────────────
#  KEY NORMALIZATION
#  The updated prompt outputs English keys.  TDocGeN's Practica
#  model expects the original Spanish keys.  This map handles
#  both formats transparently — legacy Spanish JSON still works.
# ─────────────────────────────────────────────────────────────

_EN_TO_ES: dict[str, str] = {
    "name":                  "nombre",
    "number":                "numero",
    "competency":            "competencia",
    "materials":             "material",
    "theoretical_framework": "marco_teorico",
    "questionnaire":         "cuestionario",
    "applications":          "aplicaciones",
    "references":            "referencias",
}

def normalize_practice_data(data: dict) -> dict:
    """
    Translate English prompt keys → Spanish TDocGeN canonical keys.
    Keys that are already in Spanish (or unknown) pass through unchanged,
    so both new (English) and legacy (Spanish) JSON are accepted.
    """
    return {_EN_TO_ES.get(k, k): v for k, v in data.items()}

REQUIRED_PRACTICE_FIELDS = [
    "name",
    "number",
    "competency",
    "materials",
    "theoretical_framework",
    "questionnaire",
    "applications",
    "references",
]

REQUIRED_PRACTICE_FIELDS_ES = [
    _EN_TO_ES[field]
    for field in REQUIRED_PRACTICE_FIELDS
]

ALLOWED_PRACTICE_KEYS = set(REQUIRED_PRACTICE_FIELDS_ES)


def strip_json_fences(text: str) -> str:
    """Remove common markdown code fences and backticks from AI output."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    if text.startswith("```") and text.endswith("```"):
        return text[3:-3].strip()
    return text


def extract_first_json_object(text: str) -> str:
    """Extract the first balanced JSON object from a larger text block."""
    start = text.find("{")
    if start == -1:
        return text
    stack = []
    for idx, char in enumerate(text[start:], start=start):
        if char == "{":
            stack.append(char)
        elif char == "}":
            stack.pop()
            if not stack:
                return text[start:idx + 1].strip()
    return text


def remove_trailing_commas(text: str) -> str:
    """Strip trailing commas from JSON-like content."""
    return re.sub(r",\s*(?=[}\]])", "", text)


def clean_json_text(raw: str) -> str:
    """Normalize AI JSON output so it can be parsed by json.loads."""
    text = raw.strip().replace("\r\n", "\n")
    text = strip_json_fences(text)
    text = extract_first_json_object(text)
    text = remove_trailing_commas(text)
    return text


def validate_practice_payload(data: dict) -> tuple[list[str], list[str]]:
    """Validate parsed practice JSON against required keys and allowed keys."""
    missing = []
    extra = []

    if not isinstance(data, dict):
        return ["root_object"], []

    for field in REQUIRED_PRACTICE_FIELDS_ES:
        value = data.get(field)
        if value in (None, ""):
            missing.append(field)
        elif isinstance(value, list) and not value:
            missing.append(field)

    for key in data.keys():
        if key not in ALLOWED_PRACTICE_KEYS:
            extra.append(key)

    return missing, extra

# ─────────────────────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "step": 1,
        # Step 1 — general doc fields
        "division": "",
        "tipo": "",
        "asignatura": "",
        "elaboro": [""],
        "emision": "",
        "edicion": "",
        "vigencia": "",
        "presentacion": "",
        "reglamento": DEFAULT_REGLAMENTO,
        # Step 2 — practices
        "practices": [],
        "next_practice_id": 1,
        # Generated document (persists across reruns so download stays visible)
        "generated_doc": None,  # {"bytes": bytes, "filename": str, "timestamp": str}
        # Autosave/load state
        "_autosave_loaded": False,
        "_autosave_prompted": False,
        "_autosave_enabled": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────

def go_to_step(n: int):
    st.session_state["step"] = n

def add_elaboro():
    st.session_state["elaboro"].append("")

def remove_elaboro(i: int):
    lst = st.session_state["elaboro"]
    if len(lst) > 1:
        lst.pop(i)

def add_practice():
    pid = st.session_state["next_practice_id"]
    st.session_state["practices"].append({
        "id": pid,
        "nombre": "",
        "numero": str(pid),
        "prompt": "",
        "json_input": "",
        "parsed": None,
        "expanded": True,
    })
    st.session_state["next_practice_id"] += 1

def remove_practice(pid: int):
    st.session_state["practices"] = [
        p for p in st.session_state["practices"] if p["id"] != pid
    ]

def build_prompt(p: dict) -> str:
    return PROMPT_TEMPLATE.format(
        nombre=p["nombre"] or "[sin nombre]",
        numero=p["numero"] or "[sin número]",
        asignatura=st.session_state.get("asignatura", "") or "[asignatura no especificada]",
    )

def parse_practice_json(p: dict):
    raw = p.get("json_input", "")
    if not raw or not raw.strip():
        return None, "El campo JSON está vacío."

    # Try direct parsing first, then attempt sanitized retry on common AI formatting issues.
    parse_attempts = []
    try:
        data = json.loads(raw)
        parse_attempts.append("direct")
    except json.JSONDecodeError:
        clean_text = clean_json_text(raw)
        if clean_text != raw:
            try:
                data = json.loads(clean_text)
                parse_attempts.append("cleaned")
            except json.JSONDecodeError as e:
                return None, f"JSON inválido — verifica la estructura: {e}"
        else:
            return None, f"JSON inválido — verifica la estructura y sintaxis."

    data = normalize_practice_data(data)
    missing, extra = validate_practice_payload(data)

    if missing or extra:
        messages = []
        if missing:
            messages.append(f"Faltan campos obligatorios: {', '.join(missing)}.")
        if extra:
            messages.append(f"Se encontraron claves adicionales no permitidas: {', '.join(extra)}.")
        if "cleaned" in parse_attempts:
            messages.append("El texto fue limpiado automáticamente para intentar parsear el JSON.")
        return None, " ".join(messages)

    return data, None


def build_context_data() -> dict:
    ps = st.session_state.get("practices", [])
    asig = st.session_state.get("asignatura", "")
    return {
        "division": st.session_state.get("division", ""),
        "tipo": st.session_state.get("tipo", ""),
        "asignatura": asig,
        "elaboro": st.session_state.get("elaboro", []),
        "emision": st.session_state.get("emision", ""),
        "edicion": st.session_state.get("edicion", ""),
        "vigencia": st.session_state.get("vigencia", ""),
        "presentacion": st.session_state.get("presentacion", ""),
        "reglamento": st.session_state.get("reglamento", DEFAULT_REGLAMENTO),
        "practicas": [
            {**{"nombre": p["nombre"], "numero": p["numero"]}, **(p.get("parsed") or {})}
            for p in ps
        ],
    }


def _compute_context_hash(data: dict) -> str:
    json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(json_str.encode("utf-8")).hexdigest()


def _resolve_autosave_path() -> str | None:
    try:
        from pathlib import Path
        base = Path.cwd()
    except Exception:
        from pathlib import Path
        base = Path(tempfile.gettempdir())

    autosave_file = base / "tdocgen_autosave.json"
    return str(autosave_file) if autosave_file.exists() else None


def _parse_context_json(raw: str | bytes) -> tuple[dict | None, str | None]:
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        cleaned = clean_json_text(raw)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            return None, f"JSON inválido: {e}"

    if not isinstance(data, dict):
        return None, "El JSON debe contener un objeto raíz."

    return data, None


def load_saved_context(data: dict, source: str | None = None) -> tuple[bool, str | None]:
    if not isinstance(data, dict):
        return False, "Contexto inválido."

    st.session_state["division"] = data.get("division", st.session_state.get("division", ""))
    st.session_state["tipo"] = data.get("tipo", st.session_state.get("tipo", ""))
    st.session_state["asignatura"] = data.get("asignatura", st.session_state.get("asignatura", ""))

    elaboro = data.get("elaboro", st.session_state.get("elaboro", [""]))
    if not isinstance(elaboro, list):
        elaboro = [str(elaboro)] if elaboro is not None else [""]
    st.session_state["elaboro"] = [str(x) for x in elaboro if str(x).strip()] or [""]

    st.session_state["emision"] = data.get("emision", st.session_state.get("emision", ""))
    st.session_state["edicion"] = data.get("edicion", st.session_state.get("edicion", ""))
    st.session_state["vigencia"] = data.get("vigencia", st.session_state.get("vigencia", ""))
    st.session_state["presentacion"] = data.get("presentacion", st.session_state.get("presentacion", ""))
    st.session_state["reglamento"] = data.get("reglamento", st.session_state.get("reglamento", DEFAULT_REGLAMENTO))

    raw_practices = data.get("practicas", data.get("practices", [])) or []
    practices = []
    next_id = 1
    for item in raw_practices:
        if not isinstance(item, dict):
            continue
        practice_data = normalize_practice_data(item)
        practice_json = json.dumps(practice_data, ensure_ascii=False, indent=2)
        practices.append({
            "id": next_id,
            "nombre": practice_data.get("nombre", ""),
            "numero": str(practice_data.get("numero", "")),
            "prompt": "",
            "json_input": practice_json,
            "parsed": practice_data,
            "expanded": False,
        })
        next_id += 1

    st.session_state["practices"] = practices
    st.session_state["next_practice_id"] = next_id
    st.session_state["_autosave_loaded"] = True
    st.session_state["_autosave_prompted"] = True
    if source:
        st.session_state["_autosave_file"] = source

    st.session_state["_autosave_hash"] = _compute_context_hash(build_context_data())
    return True, None


def render_autosave_loader():
    if st.session_state.get("_autosave_loaded") or st.session_state.get("_autosave_prompted"):
        return

    if any(
        st.session_state.get(k, "").strip()
        for k in ["division", "asignatura", "tipo", "emision", "edicion", "vigencia", "presentacion"]
    ) or st.session_state.get("practices"):
        return

    autosave_path = _resolve_autosave_path()
    if autosave_path is None:
        return

    st.markdown("""
    <div class="download-banner">
      <div class="db-icon">💾</div>
      <div class="db-text">
        <div class="db-title">Se encontró un progreso guardado automáticamente</div>
        <div class="db-sub">Puedes cargar el último autosave o subir un archivo JSON de contexto para continuar desde donde te quedaste.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        if st.button("Cargar progreso guardado", key="load_autosave_button"):
            try:
                from pathlib import Path
                with open(Path(autosave_path), "r", encoding="utf-8") as fh:
                    raw = fh.read()
                data, err = _parse_context_json(raw)
                if err:
                    st.error(err)
                else:
                    success, load_err = load_saved_context(data, source=autosave_path)
                    if success:
                        st.success("Progreso cargado desde autosave.")
                        st.rerun()
                    else:
                        st.error(load_err)
            except Exception as e:
                st.error(f"No se pudo cargar el autosave: {e}")
    with c2:
        if st.button("Ignorar", key="ignore_autosave_button"):
            st.session_state["_autosave_prompted"] = True
            st.rerun()

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px; color:#C3D0E0; margin-bottom:0.5rem;'>Selecciona un archivo JSON de progreso para cargar un proyecto guardado desde otra ruta.</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Seleccionar archivo JSON de progreso", type=["json"], key="upload_progress_file")
    if uploaded is not None:
        raw = uploaded.read()
        data, err = _parse_context_json(raw)
        if err:
            st.error(err)
        else:
            success, load_err = load_saved_context(data, source=getattr(uploaded, "name", "subido.json"))
            if success:
                st.success("Progreso cargado desde archivo JSON.")
                st.rerun()
            else:
                st.error(load_err)

def autosave_context(force: bool = False) -> None:
    """Save current context_data to JSON file on disk. Only writes if content changed (debounced) or force=True."""
    enabled = st.session_state.get("_autosave_enabled", True)
    if not enabled and not force:
        return

    try:
        from pathlib import Path
        import tempfile

        data = build_context_data()
        current_hash = _compute_context_hash(data)
        last_hash = st.session_state.get("_autosave_hash", None)

        # Skip write if content unchanged (unless forced)
        if current_hash == last_hash and not force:
            return

        # Prefer workspace cwd so the user can find the file easily
        try:
            base = Path.cwd()
        except Exception:
            base = Path(tempfile.gettempdir())

        autosave_file = base / "tdocgen_autosave.json"
        with open(autosave_file, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

        st.session_state["_autosave_file"] = str(autosave_file)
        st.session_state["_autosave_ts"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["_autosave_hash"] = current_hash
    except Exception:
        # Do not break the app for autosave errors; report in session_state
        st.session_state["_autosave_error"] = traceback.format_exc()

def step1_complete() -> bool:
    required = ["division", "asignatura", "emision", "edicion", "vigencia"]
    for f in required:
        if not st.session_state.get(f, "").strip():
            return False
    if not any(x.strip() for x in st.session_state.get("elaboro", [])):
        return False
    return True

def step2_complete() -> bool:
    ps = st.session_state.get("practices", [])
    if not ps:
        return False
    return all(p.get("parsed") is not None for p in ps)

# ─────────────────────────────────────────────────────────────
#  STEP RAIL
# ─────────────────────────────────────────────────────────────

def render_step_rail():
    s1_done = step1_complete()
    s2_done = step2_complete()
    current = st.session_state["step"]

    def dot_class(n):
        if current == n:
            return "active"
        if (n == 1 and s1_done) or (n == 2 and s2_done):
            return "done"
        return "idle"

    def label_class(n):
        return "" if current == n else "idle"

    conn1 = "done" if s1_done else ""

    st.markdown(f"""
    <div class="step-rail">
      <div class="step-item">
        <div class="step-dot {dot_class(1)}">{"✓" if dot_class(1) == "done" else "1"}</div>
        <div class="step-label {label_class(1)}">Datos del Documento</div>
      </div>
      <div class="step-connector {conn1}"></div>
      <div class="step-item">
        <div class="step-dot {dot_class(2)}">{"✓" if dot_class(2) == "done" else "2"}</div>
        <div class="step-label {label_class(2)}">Generación de Prácticas</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, _ = st.columns([1, 1, 4])
    with col1:
        if st.button(
            "① Datos",
            use_container_width=True,
            type="primary" if current == 1 else "secondary"
        ):
            go_to_step(1)
            st.rerun()
    with col2:
        if st.button(
            "② Prácticas",
            use_container_width=True,
            type="primary" if current == 2 else "secondary"
        ):
            go_to_step(2)
            st.rerun()

# ─────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────

def render_header():
    st.markdown("""
    <div style="display:flex; align-items:center; gap:14px; margin-bottom:1.5rem;">
      <div style="font-size:36px;"></div>
      <div>
        <div style="font-size:22px; font-weight:700; color:#E6EDF3; letter-spacing:-.02em;">TDocGeN</div>
        <div style="font-size:13px; color:#8B949E; margin-top:1px;">Generador de Manuales de Prácticas · TESJo</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  DYNAMIC LIST WIDGET
# ─────────────────────────────────────────────────────────────

def dynamic_list(key: str, label: str, placeholder: str = ""):
    """Renders a dynamic add/remove list stored in session_state[key]."""
    items: list = st.session_state.setdefault(key, [""])

    to_remove = None
    for i, item in enumerate(items):
        cols = st.columns([11, 1])
        with cols[0]:
            new_val = st.text_input(
                f"{label} #{i+1}",
                value=item,
                key=f"{key}_item_{i}",
                placeholder=placeholder,
                label_visibility="collapsed",
            )
            items[i] = new_val
        with cols[1]:
            st.markdown("<div style='padding-top:8px'>", unsafe_allow_html=True)
            if st.button("✕", key=f"{key}_del_{i}", help="Eliminar"):
                if len(items) > 1:
                    to_remove = i
            st.markdown("</div>", unsafe_allow_html=True)

    if to_remove is not None:
        items.pop(to_remove)
        st.rerun()

    if st.button(f"＋ Agregar {label.lower()}", key=f"{key}_add"):
        items.append("")
        st.rerun()

# ─────────────────────────────────────────────────────────────
#  STEP 1 — GENERAL DATA
# ─────────────────────────────────────────────────────────────

def render_step1():
    st.markdown('<div class="section-title">Información General del Manual</div>', unsafe_allow_html=True)
    st.markdown("Completa los datos institucionales del documento. Estos aparecerán en la portada y encabezados del manual.", unsafe_allow_html=False)
    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">División</div>', unsafe_allow_html=True)
        st.session_state["division"] = st.text_input(
            "División", value=st.session_state["division"],
            placeholder="ej. Ingeniería en Sistemas Computacionales",
            label_visibility="collapsed"
        )
    with c2:
        st.markdown('<div class="section-title">Asignatura</div>', unsafe_allow_html=True)
        st.session_state["asignatura"] = st.text_input(
            "Asignatura", value=st.session_state["asignatura"],
            placeholder="ej. Programación Orientada a Objetos",
            label_visibility="collapsed"
        )

    st.markdown("")

    # ── Tipo (used as student/owner name)
    st.markdown('<div class="section-title">Nombre del Alumno / Propietario del Documento</div>', unsafe_allow_html=True)
    st.markdown('<div class="field-hint">Este campo identifica al alumno o titular del manual. Aparecerá destacado en el documento.</div>', unsafe_allow_html=True)
    st.session_state["tipo"] = st.text_input(
        "Nombre alumno", value=st.session_state["tipo"],
        placeholder="ej. García López Juan Carlos  —  No. Control: 20231234",
        label_visibility="collapsed"
    )

    st.markdown("")

    # ── Elaboró (dynamic list)
    st.markdown('<div class="section-title">Elaboró</div>', unsafe_allow_html=True)
    st.markdown('<div class="field-hint">Docente(s) o autor(es) que elaboraron el manual.</div>', unsafe_allow_html=True)
    dynamic_list("elaboro", "Autor", placeholder="Nombre completo del docente")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Dates / edition
    st.markdown('<div class="section-title">Datos de Edición</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state["emision"] = st.text_input(
            "Emisión", value=st.session_state["emision"],
            placeholder="ej. Febrero 2024"
        )
    with c2:
        st.session_state["edicion"] = st.text_input(
            "Edición", value=st.session_state["edicion"],
            placeholder="ej. 1ª"
        )
    with c3:
        st.session_state["vigencia"] = st.text_input(
            "Vigencia", value=st.session_state["vigencia"],
            placeholder="ej. 2024-2025"
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Presentación
    st.markdown('<div class="section-title">Presentación</div>', unsafe_allow_html=True)
    st.session_state["presentacion"] = st.text_area(
        "Presentación", value=st.session_state["presentacion"],
        placeholder="Texto introductorio del manual…",
        height=140,
        label_visibility="collapsed"
    )

    st.markdown("")

    # ── Reglamento
    with st.expander("Reglamento Interno de Salas de Cómputo", expanded=False):
        st.markdown('<div class="field-hint">Texto oficial del reglamento. Puedes editarlo si es necesario.</div>', unsafe_allow_html=True)
        st.session_state["reglamento"] = st.text_area(
            "Reglamento", value=st.session_state["reglamento"],
            height=360,
            label_visibility="collapsed"
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Progress & CTA
    filled = sum([
        bool(st.session_state["division"].strip()),
        bool(st.session_state["asignatura"].strip()),
        bool(st.session_state["tipo"].strip()),
        bool(any(x.strip() for x in st.session_state["elaboro"])),
        bool(st.session_state["emision"].strip()),
        bool(st.session_state["edicion"].strip()),
        bool(st.session_state["vigencia"].strip()),
        bool(st.session_state["presentacion"].strip()),
    ])
    total = 8
    pct = filled / total

    col_prog, col_btn = st.columns([4, 1])
    with col_prog:
        st.markdown(f'<div style="font-size:12px; color:#8B949E; margin-bottom:4px;">{filled}/{total} campos completados</div>', unsafe_allow_html=True)
        st.progress(pct)
    with col_btn:
        if st.button("Continuar →", type="primary", use_container_width=True):
            if step1_complete():
                go_to_step(2)
                st.rerun()
            else:
                st.error("Completa los campos obligatorios antes de continuar: División, Asignatura, Elaboró, Emisión, Edición y Vigencia.")

# ─────────────────────────────────────────────────────────────
#  STEP 2 — PRACTICES
# ─────────────────────────────────────────────────────────────

def render_practice_card(p: dict, idx: int):
    pid = p["id"]
    nombre = p.get("nombre", "")
    numero = p.get("numero", "")

    display_title = nombre if nombre.strip() else f"Práctica {numero}"
    parsed_ok = p.get("parsed") is not None
    status_text = "Contenido cargado" if parsed_ok else "Esperando JSON"
    status_class = "badge-ok" if parsed_ok else "badge-warn"

    badge_html = f'<span class="{status_class}">{status_text}</span>'

    with st.expander(f"{'🟢' if parsed_ok else '🔵'} Práctica {numero} — {display_title}", expanded=p.get("expanded", True)):
        st.markdown(badge_html, unsafe_allow_html=True)
        st.markdown("")

        # ── Basic info
        c1, c2 = st.columns([3, 1])
        with c1:
            new_nombre = st.text_input(
                "Nombre de la práctica",
                value=nombre,
                key=f"prac_{pid}_nombre",
                placeholder="ej. Introducción a Python — Variables y Tipos de Datos"
            )
            p["nombre"] = new_nombre
        with c2:
            new_num = st.text_input(
                "Número",
                value=numero,
                key=f"prac_{pid}_numero",
                placeholder="ej. 1"
            )
            p["numero"] = new_num

        st.markdown("")

        # ── Prompt generation
        st.markdown('<div class="section-title">① Generar Prompt para IA</div>', unsafe_allow_html=True)
        st.markdown('<div class="field-hint">Genera el prompt, cópialo y pégalo en tu IA favorita (ChatGPT, Claude, Gemini…). El prompt está en inglés y solicita referencias IEEE 2018–2024.</div>', unsafe_allow_html=True)

        gen_col, _ = st.columns([1, 3])
        with gen_col:
            if st.button("Generar Prompt", key=f"gen_{pid}", type="primary"):
                p["prompt"] = build_prompt(p)
                st.rerun()

        if p.get("prompt"):
            prompt_text = p["prompt"]
            st.code(prompt_text, language='')
            st.markdown('<div class="field-hint">Pulsa el botón de copia junto al bloque de código para copiar el prompt, o utiliza el menú del navegador si lo prefieres.</div>', unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        # ── JSON input
        st.markdown('<div class="section-title">② Pegar respuesta JSON de la IA</div>', unsafe_allow_html=True)
        st.markdown('<div class="field-hint">La IA responderá un JSON. Pégalo aquí y presiona "Cargar JSON".</div>', unsafe_allow_html=True)

        new_json = st.text_area(
            "JSON de la IA",
            value=p.get("json_input", ""),
            height=160,
            key=f"json_{pid}",
            placeholder='{\n  "nombre": "...",\n  "competencia": "...",\n  ...\n}',
            label_visibility="collapsed",
        )
        p["json_input"] = new_json

        load_col, del_col = st.columns([2, 6])
        with load_col:
            if st.button("Cargar JSON", key=f"load_{pid}", type="primary"):
                data, err = parse_practice_json(p)
                if err:
                    st.error(err)
                else:
                    p["parsed"] = data
                    st.success("Contenido cargado exitosamente.")
                    st.rerun()
        with del_col:
            if st.button("🗑 Eliminar práctica", key=f"del_{pid}"):
                st.session_state[f"pending_delete_{pid}"] = True
                st.rerun()

            if st.session_state.get(f"pending_delete_{pid}"):
                st.warning("¿Eliminar práctica? Esta acción es irreversible y eliminará todo el contenido asociado.")
                c_yes, c_no = st.columns([1, 1])
                with c_yes:
                    if st.button("Sí, eliminar práctica", key=f"confirm_del_{pid}"):
                        remove_practice(pid)
                        st.session_state.pop(f"pending_delete_{pid}", None)
                        st.rerun()
                with c_no:
                    if st.button("Cancelar", key=f"cancel_del_{pid}"):
                        st.session_state.pop(f"pending_delete_{pid}", None)
                        st.rerun()

        # ── Preview and Edit parsed content
        if p.get("parsed"):
            with st.expander("✏️ Editar contenido cargado", expanded=True):
                d = p["parsed"]

                # ── Competencia
                st.markdown("**Competencia**")
                new_comp = st.text_area(
                    "Competencia",
                    value=d.get("competencia", ""),
                    height=100,
                    key=f"edit_comp_{pid}",
                    label_visibility="collapsed"
                )
                d["competencia"] = new_comp
                st.markdown("")

                # ── Marco Teórico
                st.markdown("**📖 Marco Teórico**")
                new_marco = st.text_area(
                    "Marco Teórico",
                    value=d.get("marco_teorico", ""),
                    height=150,
                    key=f"edit_marco_{pid}",
                    label_visibility="collapsed"
                )
                d["marco_teorico"] = new_marco
                st.markdown("")

                # ── Material (dynamic list)
                st.markdown("**Material**")
                mat = d.get("material", [])
                if not isinstance(mat, list):
                    mat = [mat]
                mat_to_remove = None
                for i, item in enumerate(mat):
                    cols = st.columns([11, 1])
                    with cols[0]:
                        new_item = st.text_input(
                            f"Material {i+1}",
                            value=item,
                            key=f"edit_mat_{pid}_{i}",
                            label_visibility="collapsed"
                        )
                        mat[i] = new_item
                    with cols[1]:
                        st.markdown("<div style='padding-top:8px'>", unsafe_allow_html=True)
                        if st.button("✕", key=f"edit_mat_del_{pid}_{i}", help="Eliminar"):
                            if len(mat) > 1:
                                mat_to_remove = i
                        st.markdown("</div>", unsafe_allow_html=True)
                if mat_to_remove is not None:
                    mat.pop(mat_to_remove)
                    st.rerun()
                if st.button("＋ Agregar material", key=f"edit_mat_add_{pid}"):
                    mat.append("")
                    st.rerun()
                d["material"] = mat
                st.markdown("")

                # ── Cuestionario (dynamic list)
                st.markdown("**❓ Cuestionario**")
                cuest = d.get("cuestionario", [])
                if not isinstance(cuest, list):
                    cuest = [cuest]
                cuest_to_remove = None
                for i, item in enumerate(cuest):
                    cols = st.columns([11, 1])
                    with cols[0]:
                        new_item = st.text_area(
                            f"Pregunta {i+1}",
                            value=item,
                            key=f"edit_cuest_{pid}_{i}",
                            height=80,
                            label_visibility="collapsed"
                        )
                        cuest[i] = new_item
                    with cols[1]:
                        st.markdown("<div style='padding-top:8px'>", unsafe_allow_html=True)
                        if st.button("✕", key=f"edit_cuest_del_{pid}_{i}", help="Eliminar"):
                            if len(cuest) > 1:
                                cuest_to_remove = i
                        st.markdown("</div>", unsafe_allow_html=True)
                if cuest_to_remove is not None:
                    cuest.pop(cuest_to_remove)
                    st.rerun()
                if st.button("＋ Agregar pregunta", key=f"edit_cuest_add_{pid}"):
                    cuest.append("")
                    st.rerun()
                d["cuestionario"] = cuest
                st.markdown("")

                # ── Aplicaciones (dynamic list)
                st.markdown("**🌐 Aplicaciones**")
                apps = d.get("aplicaciones", [])
                if not isinstance(apps, list):
                    apps = [apps]
                apps_to_remove = None
                for i, item in enumerate(apps):
                    cols = st.columns([11, 1])
                    with cols[0]:
                        new_item = st.text_input(
                            f"Aplicación {i+1}",
                            value=item,
                            key=f"edit_apps_{pid}_{i}",
                            label_visibility="collapsed"
                        )
                        apps[i] = new_item
                    with cols[1]:
                        st.markdown("<div style='padding-top:8px'>", unsafe_allow_html=True)
                        if st.button("✕", key=f"edit_apps_del_{pid}_{i}", help="Eliminar"):
                            if len(apps) > 1:
                                apps_to_remove = i
                        st.markdown("</div>", unsafe_allow_html=True)
                if apps_to_remove is not None:
                    apps.pop(apps_to_remove)
                    st.rerun()
                if st.button("＋ Agregar aplicación", key=f"edit_apps_add_{pid}"):
                    apps.append("")
                    st.rerun()
                d["aplicaciones"] = apps
                st.markdown("")

                # ── Referencias (dynamic list)
                st.markdown("**📚 Referencias IEEE**")
                refs = d.get("referencias", [])
                if not isinstance(refs, list):
                    refs = [refs]
                refs_to_remove = None
                for i, item in enumerate(refs):
                    cols = st.columns([11, 1])
                    with cols[0]:
                        new_item = st.text_input(
                            f"Referencia {i+1}",
                            value=item,
                            key=f"edit_refs_{pid}_{i}",
                            label_visibility="collapsed"
                        )
                        refs[i] = new_item
                    with cols[1]:
                        st.markdown("<div style='padding-top:8px'>", unsafe_allow_html=True)
                        if st.button("✕", key=f"edit_refs_del_{pid}_{i}", help="Eliminar"):
                            if len(refs) > 1:
                                refs_to_remove = i
                        st.markdown("</div>", unsafe_allow_html=True)
                if refs_to_remove is not None:
                    refs.pop(refs_to_remove)
                    st.rerun()
                if st.button("＋ Agregar referencia", key=f"edit_refs_add_{pid}"):
                    refs.append("")
                    st.rerun()
                d["referencias"] = refs


def render_step2():
    st.markdown('<div class="section-title">Gestión de Prácticas</div>', unsafe_allow_html=True)

    asig = st.session_state.get("asignatura", "")
    st.markdown(f"Agrega y configura las prácticas para **{asig}**. Para cada práctica: genera el prompt → pégalo en la IA → copia el JSON → cárgalo aquí.", unsafe_allow_html=True)

    # ── Summary bar
    ps = st.session_state["practices"]
    total_p = len(ps)
    done_p = sum(1 for p in ps if p.get("parsed") is not None)

    info_col, add_col = st.columns([5, 2])
    with info_col:
        if total_p == 0:
            st.info("No hay prácticas todavía. Agrega la primera práctica para empezar.")
        else:
            st.markdown(f'<div style="font-size:13px; color:#8B949E; padding-top:10px;">{done_p}/{total_p} prácticas con contenido cargado</div>', unsafe_allow_html=True)
            if total_p > 0:
                st.progress(done_p / total_p)
    with add_col:
        if st.button("＋ Nueva Práctica", type="primary", use_container_width=True):
            add_practice()
            st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Practice cards
    for idx, p in enumerate(ps):
        render_practice_card(p, idx)
        st.markdown("")

    # ── Generate document CTA
    if ps:
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Exportar Documento</div>', unsafe_allow_html=True)

        if done_p < total_p:
            st.warning(f"Faltan {total_p - done_p} práctica(s) por cargar JSON. Puedes exportar de todas formas, pero esas prácticas incompletas no serán incluidas correctamente.")

        c1, c2 = st.columns([3, 2])
        with c1:
            output_name = st.text_input(
                "Nombre del archivo de salida",
                value=f"manual_{asig.replace(' ','_').lower() or 'practicas'}.docx",
                placeholder="manual.docx"
            )
        with c2:
            template_path = st.text_input(
                "Ruta de la plantilla (.docx)",
                value="template.docx",
                placeholder="ruta/a/plantilla.docx"
            )

        gen_btn = st.button(
            "⚙ Generar Documento Word",
            type="primary",
            disabled=st.session_state.get("_generating", False),
        )

        if gen_btn:
            st.session_state["_generating"] = True
            st.session_state["generated_doc"] = None  # clear previous

            with st.spinner("Generando documento Word… esto puede tardar unos segundos."):
                try:
                    import sys
                    from pathlib import Path

                    BASE_DIR = Path.cwd()
                    if str(BASE_DIR) not in sys.path:
                        sys.path.insert(0, str(BASE_DIR))

                    from TDocGeN import Manual, Practica, ManualRenderer

                    manual = Manual(
                        division=st.session_state["division"],
                        tipo=st.session_state["tipo"],
                        asignatura=st.session_state["asignatura"],
                        elaboro=[x for x in st.session_state["elaboro"] if x.strip()],
                        emision=st.session_state["emision"],
                        edicion=st.session_state["edicion"],
                        vigencia=st.session_state["vigencia"],
                        presentacion=st.session_state["presentacion"],
                        reglamento=st.session_state["reglamento"],
                    )

                    for p in ps:
                        data = p.get("parsed") or {}
                        if data:
                            practica = (
                                Practica.quick(
                                    numero=p.get("numero", ""),
                                    nombre=p.get("nombre", ""),
                                ).update_from_dict(data)
                            )
                            manual.agregar_practica(practica)

                    template_file = Path(template_path)
                    if not template_file.exists():
                        st.error(f"Plantilla no encontrada: `{template_path}`. Verifica la ruta.")
                        st.stop()

                    renderer = ManualRenderer(str(template_file))

                    # ── Render to a temp file, read bytes, then clean up ──
                    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".docx")
                    os.close(tmp_fd)
                    try:
                        renderer.render(manual, output_path=tmp_path)
                        with open(tmp_path, "rb") as fh:
                            doc_bytes = fh.read()
                    finally:
                        if os.path.exists(tmp_path):
                            os.unlink(tmp_path)

                    # ── Build dynamic filename: use user-provided output name when available.
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    asig_slug = "".join(
                        c if c.isalnum() else "_"
                        for c in asig.lower()
                    )[:30].strip("_") or "practicas"

                    raw_name = output_name.strip() or f"manual_{asig_slug}_{timestamp}"
                    # Preservar .docx si está presente en el nombre
                    has_docx = raw_name.lower().endswith(".docx")
                    if has_docx:
                        base_name = raw_name[:-5]  # Remover .docx
                    else:
                        base_name = raw_name
                    # Sanear solo la parte base (sin extensión)
                    safe_name = "".join(
                        c if c.isalnum() or c in ("-", "_", ".") else "_"
                        for c in base_name
                    ).strip("_")
                    if not safe_name:
                        safe_name = f"manual_{asig_slug}_{timestamp}"
                    safe_name = f"{safe_name}.docx"

                    download_filename = safe_name

                    # ── Persist so download button survives reruns ──
                    st.session_state["generated_doc"] = {
                        "bytes":     doc_bytes,
                        "filename":  download_filename,
                        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "practices": done_p,
                    }

                except ImportError as e:
                    st.error(
                        f"No se pudo importar TDocGeN: {e}  \n"
                        "Asegúrate de que **TDocGeN.py** esté en el mismo directorio."
                    )
                except FileNotFoundError:
                    st.error(f"Plantilla no encontrada: `{template_path}`. Verifica la ruta.")
                except Exception as e:
                    st.error(f"Error al generar el documento:")
                    st.code(traceback.format_exc())
                finally:
                    st.session_state["_generating"] = False

        # ── Persistent download area (stays visible across reruns) ──
        gdoc = st.session_state.get("generated_doc")
        if gdoc:
            st.markdown(f"""
            <div class="download-banner">
              <div class="db-icon"></div>
              <div class="db-text">
                <div class="db-title">Documento generado correctamente</div>
                <div class="db-sub">{gdoc['filename']} · {gdoc['practices']} práctica(s) incluidas · {gdoc['timestamp']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            st.download_button(
                label="⬇ Descargar Documento Word (.docx)",
                data=gdoc["bytes"],
                file_name=gdoc["filename"],
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

        # ── Export context JSON (always available)
        with st.expander("Exportar contexto JSON (debug / backup)", expanded=False):
            context_data = build_context_data()

            # Autosave controls
            c_left, c_right = st.columns([3, 1])
            with c_left:
                st.checkbox("Habilitar autosave (guarda automáticamente en el disco del servidor)", value=st.session_state.get("_autosave_enabled", True), key="_autosave_enabled")
            with c_right:
                if st.button("Guardar ahora"):
                    autosave_context(force=True)
                    st.success("Contexto guardado en disco.")

            autosave_file = st.session_state.get("_autosave_file")
            autosave_ts = st.session_state.get("_autosave_ts")
            if autosave_file and autosave_ts:
                st.markdown(f"Último autosave: {autosave_ts} — {autosave_file}")
                try:
                    with open(autosave_file, "r", encoding="utf-8") as fh:
                        file_text = fh.read()
                except Exception:
                    file_text = json.dumps(context_data, ensure_ascii=False, indent=2)
            else:
                file_text = json.dumps(context_data, ensure_ascii=False, indent=2)

            st.download_button(
                "⬇ Descargar JSON completo",
                data=file_text,
                file_name="tdocgen_context.json",
                mime="application/json"
            )

            if st.session_state.get("_autosave_error"):
                st.error("Error autosave: revisa logs del servidor.")

        # Auto-write only when autosave is enabled and content changed (debounced via hash comparison)
        if st.session_state.get("_autosave_enabled", True):
            autosave_context()

    # ── Back
    st.markdown("<hr/>", unsafe_allow_html=True)
    if st.button("← Volver a Datos del Documento"):
        go_to_step(1)
        st.rerun()

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

render_header()
render_autosave_loader()
render_step_rail()
st.markdown("")

if st.session_state["step"] == 1:
    render_step1()
else:
    render_step2()

# ── Footer
st.markdown("""
<div style="margin-top:4rem; padding-top:1rem; border-top:1px solid #21262D; text-align:center; color:#484F58; font-size:12px;">
  TDocGeN · Instituto Tecnológico Superior de Jocotitlán · Generador de Manuales de Prácticas
</div>
""", unsafe_allow_html=True)