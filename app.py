"""
TDocGeN — Generador de Manuales de Prácticas TESJo
Streamlit app · Step-based workflow
"""

import json
import traceback
import streamlit as st

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="TDocGeN",
    page_icon="📄",
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
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #4F8EF7;
    margin-bottom: .4rem;
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
    color: #E6EDF3 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #4F8EF7 !important;
    box-shadow: 0 0 0 3px #4F8EF715 !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    transition: all .15s !important;
}
.stButton > button[kind="primary"] {
    background: #4F8EF7 !important;
    border: none !important;
    color: #fff !important;
}
.stButton > button[kind="primary"]:hover {
    background: #3D7DE0 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px #4F8EF744 !important;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #21262D;
    margin: 1.5rem 0;
}

/* ── expander ── */
.streamlit-expanderHeader {
    background: #161B22 !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
    color: #E6EDF3 !important;
}

/* Subtle label */
.field-hint {
    font-size: 11px;
    color: #8B949E;
    margin-top: -8px;
    margin-bottom: 8px;
}

/* Progress bar */
.stProgress > div > div {
    background: #4F8EF7 !important;
    border-radius: 4px !important;
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

PROMPT_TEMPLATE = """Eres un experto en diseño curricular para educación tecnológica superior.

Genera el contenido académico completo para la siguiente práctica de laboratorio del TESJo.

DATOS DE LA PRÁCTICA:
- Nombre: {nombre}
- Número: {numero}
- Asignatura: {asignatura}

Devuelve EXCLUSIVAMENTE un objeto JSON válido con esta estructura exacta (sin texto adicional, sin bloques de código markdown):

{{
  "nombre": "{nombre}",
  "numero": "{numero}",
  "competencia": "<Redacta la competencia específica de esta práctica. 2-3 oraciones. Incluye verbos de desempeño, condición y criterio de calidad.>",
  "material": [
    "<Elemento de material/software/recurso 1>",
    "<Elemento de material/software/recurso 2>",
    "<Elemento de material/software/recurso 3>"
  ],
  "marco_teorico": "<Marco teórico completo de la práctica. Mínimo 4 párrafos bien desarrollados. Incluye conceptos fundamentales, historia, fundamentos técnicos y aplicación en el contexto de la asignatura.>",
  "cuestionario": [
    "<Pregunta de reflexión o evaluación 1>",
    "<Pregunta de reflexión o evaluación 2>",
    "<Pregunta de reflexión o evaluación 3>",
    "<Pregunta de reflexión o evaluación 4>",
    "<Pregunta de reflexión o evaluación 5>"
  ],
  "aplicaciones": [
    "<Aplicación práctica o caso de uso real 1>",
    "<Aplicación práctica o caso de uso real 2>",
    "<Aplicación práctica o caso de uso real 3>"
  ],
  "referencias": [
    "<Referencia bibliográfica en formato APA 1>",
    "<Referencia bibliográfica en formato APA 2>",
    "<Referencia bibliográfica en formato APA 3>"
  ]
}}

IMPORTANTE:
- Responde ÚNICAMENTE con el JSON. Nada más.
- Usa terminología técnica apropiada para nivel superior tecnológico.
- El marco_teorico debe ser extenso y bien fundamentado.
- Las referencias deben ser reales y actuales (2018-2024).
- Todo el contenido debe estar en español formal académico.
"""

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
    raw = p.get("json_input", "").strip()

    if not raw:
        return None, "El campo JSON está vacío."

    # limpiar markdown
    if raw.startswith("```"):
        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")
        raw = raw.strip()

    try:
        data = json.loads(raw)
        return data, None

    except json.JSONDecodeError as e:
        return None, f"JSON inválido: {e}"

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

    col1, col2, _, nav_col = st.columns([1, 1, 4, 2])
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
      <div style="font-size:36px;">📄</div>
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

    badge_html = f'<span class="badge-ok">✓ JSON cargado</span>' if parsed_ok else f'<span class="badge-warn">⟳ Pendiente</span>'

    with st.expander(f"{'🟢' if parsed_ok else '🔵'} Práctica {numero} — {display_title}", expanded=p.get("expanded", True)):

        st.markdown(f"{badge_html}", unsafe_allow_html=True)
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
        st.markdown('<div class="field-hint">Genera el prompt, cópialo y pégalo en tu IA favorita (ChatGPT, Claude, Gemini…).</div>', unsafe_allow_html=True)

        gen_col, _ = st.columns([1, 3])
        with gen_col:
            if st.button("⚡ Generar Prompt", key=f"gen_{pid}", type="primary"):
                p["prompt"] = build_prompt(p)
                st.rerun()

        if p.get("prompt"):
            prompt_text = p["prompt"]
            st.text_area(
                "Prompt generado",
                value=prompt_text,
                height=200,
                key=f"prompt_area_{pid}",
                label_visibility="collapsed",
            )
            st.markdown('<div class="field-hint">Selecciona todo el texto (Ctrl+A) y cópialo, o usa el botón de copia de tu navegador.</div>', unsafe_allow_html=True)

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
            if st.button("✅ Cargar JSON", key=f"load_{pid}", type="primary"):
                data, err = parse_practice_json(p)
                if err:
                    st.error(err)
                else:
                    p["parsed"] = data
                    st.success("¡Práctica cargada correctamente!")
                    st.rerun()
        with del_col:
            if st.button("🗑 Eliminar práctica", key=f"del_{pid}"):
                remove_practice(pid)
                st.rerun()

        # ── Preview parsed content
        if p.get("parsed"):
            with st.expander("👁 Vista previa de contenido cargado", expanded=False):
                d = p["parsed"]
                st.markdown(f"**Competencia:** {d.get('competencia','')}")
                st.markdown(f"**Marco Teórico:** {d.get('marco_teorico','')[:300]}…")
                mat = d.get("material", [])
                if mat:
                    st.markdown("**Material:** " + " · ".join(mat))
                cuest = d.get("cuestionario", [])
                if cuest:
                    st.markdown("**Cuestionario:** " + str(len(cuest)) + " preguntas generadas")
                refs = d.get("referencias", [])
                if refs:
                    st.markdown("**Referencias:** " + str(len(refs)) + " referencias")


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
            st.warning(f"Faltan {total_p - done_p} práctica(s) por cargar JSON. Puedes exportar de todas formas, pero esas prácticas quedarán vacías.")

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

        if st.button("Generar Documento Word", type="primary"):
            # Build Manual and render
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
                        practica = Practica.quick(
                            numero=p.get("numero", ""),
                            nombre=p.get("nombre", ""),
                        ).update_from_dict(data)

                        manual.agregar_practica(practica)

                from pathlib import Path

                template_file = Path(template_path)

                if not template_file.exists():
                    st.error(f"No existe la plantilla: {template_path}")
                    st.stop()

                renderer = ManualRenderer(str(template_file))
                renderer.render(manual, output_path=output_name)

                st.success(f"Documento generado: **{output_name}**")

            except ImportError as e:
                st.error(f"No se pudo importar TDocGeN: {e}. Asegúrate de que TDocGeN.py esté en el mismo directorio.")
            except FileNotFoundError:
                st.error(f"Plantilla no encontrada: `{template_path}`. Verifica la ruta.")
            except Exception as e:
                st.error(f"Error al generar el documento:\n\n{e}")
                st.code(traceback.format_exc())

        # ── Export context JSON (always available)
        with st.expander("📋 Exportar contexto JSON (debug / backup)", expanded=False):
            context_data = {
                "division": st.session_state["division"],
                "tipo": st.session_state["tipo"],
                "asignatura": st.session_state["asignatura"],
                "elaboro": st.session_state["elaboro"],
                "emision": st.session_state["emision"],
                "edicion": st.session_state["edicion"],
                "vigencia": st.session_state["vigencia"],
                "presentacion": st.session_state["presentacion"],
                "practicas": [
                    {**{"nombre": p["nombre"], "numero": p["numero"]}, **(p.get("parsed") or {})}
                    for p in ps
                ]
            }
            st.download_button(
                "⬇ Descargar JSON completo",
                data=json.dumps(context_data, ensure_ascii=False, indent=2),
                file_name="tdocgen_context.json",
                mime="application/json"
            )

    # ── Back
    st.markdown("<hr/>", unsafe_allow_html=True)
    if st.button("← Volver a Datos del Documento"):
        go_to_step(1)
        st.rerun()

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

render_header()
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
