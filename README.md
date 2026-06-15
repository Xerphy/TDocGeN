# TDocGeN

Automatic document generation framework for TESJo academic formats, laboratory manuals, technical reports, and structured institutional documentation.

TDocGeN simplifies the creation of `.docx` documents using reusable templates, structured data models, and automated rendering pipelines.

---

## What is this?

TDocGeN is a Python-based document generation script designed to automate repetitive academic formatting tasks.

Instead of manually editing Word documents every semester, TDocGeN allows users to define structured content once and generate complete documents automatically.

The script is built around:

* reusable templates,
* structured models,
* automatic section rendering,
* and flexible data-driven generation.

---

## Features

* Automatic `.docx` generation
* Structured academic document models
* Template-based rendering
* Laboratory practice generation
* JSON → document pipelines
* Reusable architecture
* Support for large theoretical content
* Dynamic questionnaires and references
* Python-centered workflow

---

## Example

```python id="l4i3r8"
manual = Manual(
    division="Ingeniería Mecatrónica",
    tipo="Rick Grimes",  # the document type normally goes here
    asignatura="Estadística y Control de Calidad"
)

practica = Practica.quick(
    "1.1",
    "Histogramas"
)

manual.agregar_practica(practica)

renderer = ManualRenderer("template.docx")

renderer.render(
    manual,
    "output.docx"
)
```

---

## JSON-based generation

TDocGeN supports dynamic document construction using dictionaries and JSON structures.

```python id="9x1wsa"
p.update_from_dict(json_data)
```

This allows:

* database integration,
* API-based generation,
* AI-generated content,
* and fully automated academic workflows.

---

## Project philosophy

Writing academic formats manually is repetitive.

Rearranging the same sections over and over again is repetitive.

Fixing broken Word spacing at 11:58 PM is also repetitive.

Let's not do repetitive things.

TDocGeN exists so people can focus on content instead of fighting document formatting like Rick Grimes surviving a corridor full of walkers.

---

## Use cases

* Laboratory manuals
* Academic reports
* Technical documentation
* Practice guides
* Institutional formats
* Automated reporting systems

In short: any workflow that requires automatically filling TESJo academic formats.

---

## Tech stack

* Python 3
* python-docx
* JSON structures
* Custom rendering engine

---

## License

This project is licensed under the MIT License.

The software is provided "AS IS", without warranty of any kind.

Users are responsible for verifying generated documents before official or institutional use.

---

## Status

Under active development.

If the walkers break the pipeline, open an issue.
