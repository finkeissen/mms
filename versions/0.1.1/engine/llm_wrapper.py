#!/usr/bin/env python3
"""
LLM-Wrapper für das MMS-Projekt (Version 0.1)

Zentrale Stelle für alle Aufrufe an ein Sprachmodell.

Design (v0.1):
- Konfiguration liegt in llm_config.json im Projekt-Root (0.1)
- Struktur llm_config.json (v0.1):

{
  "version": "0.1",
  "default_backend": "dummy",
  "default_model": "mms-dummy-0.1",
  "tasks": {
    "generate_domains": { "backend": "dummy", "model": "mms-dummy-0.1" },
    "generate_problems": { "backend": "dummy", "model": "mms-dummy-0.1" }
  },
  "extra": {}
}

- Jede Engine-Funktion ruft call_llm(prompt, task="...") auf.
- Wenn keine Task-Spezifikation da ist, werden default_backend und default_model genutzt.

Backends (v0.1):
- "dummy"         -> gibt eine JSON-Info über den Prompt zurück (zum Testen)
- "not_configured" (Fallback, wenn keine Konfiguration existiert)

Dieses Modul verändert nichts außerhalb des Projektcontainers (0.1).
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

# Projekt-Root (0.1)
BASE = Path(__file__).resolve().parents[1]
CONFIG_FILE = BASE / "llm_config.json"


class LLMConfig:
    """
    Repräsentiert die LLM-Konfiguration aus llm_config.json.

    Unterstützt zwei Modi:
    - neue Struktur (version, default_backend, tasks, ...)
    - alte einfache Struktur (backend, model, extra) für Abwärtskompatibilität
    """

    def __init__(
        self,
        default_backend: str = "not_configured",
        default_model: str = "",
        tasks: Optional[Dict[str, Dict[str, Any]]] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.default_backend = default_backend
        self.default_model = default_model
        self.tasks: Dict[str, Dict[str, Any]] = tasks or {}
        self.extra: Dict[str, Any] = extra or {}

    @classmethod
    def load(cls) -> "LLMConfig":
        """
        Lädt die LLM-Konfiguration aus llm_config.json, falls vorhanden.
        Fällt andernfalls auf einen sicheren Default zurück ("not_configured").
        """
        if not CONFIG_FILE.exists():
            # Kein Konfigurationsfile: sicherer Fallback
            return cls(default_backend="not_configured")

        try:
            raw = CONFIG_FILE.read_text(encoding="utf-8")
            data = json.loads(raw)
        except Exception as e:
            raise RuntimeError(f"Fehler beim Lesen von {CONFIG_FILE}: {e}") from e

        # Neue Struktur mit version/default_backend/default_model
        if "default_backend" in data or "default_model" in data or "tasks" in data:
            default_backend = data.get("default_backend", "not_configured")
            default_model = data.get("default_model", "")
            tasks = data.get("tasks", {}) or {}
            extra = data.get("extra", {}) or {}
            return cls(
                default_backend=default_backend,
                default_model=default_model,
                tasks=tasks,
                extra=extra,
            )

        # Alte einfache Struktur (optional für Kompatibilität)
        if "backend" in data or "model" in data:
            backend = data.get("backend", "not_configured")
            model = data.get("model", "")
            extra = data.get("extra", {}) or {}
            return cls(
                default_backend=backend,
                default_model=model,
                tasks={},
                extra=extra,
            )

        # Fallback, falls etwas ganz anderes drinsteht
        return cls(default_backend="not_configured")


def _resolve_task_config(cfg: LLMConfig, task: Optional[str]) -> Dict[str, Any]:
    """
    Ermittelt Backend/Model/Extra für eine gegebene Task.
    Falls keine Task vorhanden oder keine Task-spezifische Konfiguration existiert,
    werden default_backend, default_model und cfg.extra verwendet.
    """
    backend = cfg.default_backend
    model = cfg.default_model
    extra: Dict[str, Any] = dict(cfg.extra)  # Basis-extra

    if task and task in cfg.tasks:
        t_conf = cfg.tasks[task] or {}
        backend = t_conf.get("backend", backend)
        model = t_conf.get("model", model)
        t_extra = t_conf.get("extra")
        if isinstance(t_extra, dict):
            extra.update(t_extra)

    return {
        "backend": backend,
        "model": model,
        "extra": extra,
    }


def _backend_dummy(prompt: str, backend: str, model: str, extra: Dict[str, Any], **_: Any) -> str:
    """
    Dummy-Backend: gibt eine JSON-Struktur mit Prompt-Vorschau zurück.

    Dies ist zum Testen der gesamten Pipeline gedacht.
    Die Antwort entspricht NICHT den Protokoll-JSON-Strukturen und wird
    von den Parsern (z.B. generate_domains) absichtlich als ungültig erkannt,
    bis ein echtes LLM konfiguriert ist.
    """
    fake = {
        "backend": backend,
        "model": model or "none",
        "extra": extra,
        "received_prompt_preview": prompt[:200],
        "message": (
            "LLM ist noch im Dummy-Modus. "
            "Dies ist eine simulierte Antwort aus llm_wrapper._backend_dummy."
        ),
    }
    return json.dumps(fake, ensure_ascii=False)


def _backend_not_configured(prompt: str, backend: str, model: str, extra: Dict[str, Any], **_: Any) -> str:
    """
    Backend für den Fall, dass keine sinnvolle Konfiguration vorliegt.
    """
    raise RuntimeError(
        "LLM ist nicht konfiguriert (backend='not_configured').\n"
        f"Bitte erstelle eine Datei {CONFIG_FILE.name} im Projekt-Root (0.1), z.B.:\n"
        "{\n"
        '  "version": "0.1",\n'
        '  "default_backend": "dummy",\n'
        '  "default_model": "mms-dummy-0.1",\n'
        '  "tasks": {},\n'
        '  "extra": {}\n'
        "}\n"
    )


# Beispiel-Placeholder für ein mögliches OpenAI-Backend (auskommentiert):
#
# def _backend_openai_chat(prompt: str, backend: str, model: str, extra: Dict[str, Any], **kwargs: Any) -> str:
#     import openai
#     api_key_env = extra.get("api_key_env", "OPENAI_API_KEY")
#     api_key = os.environ.get(api_key_env)
#     if not api_key:
#         raise RuntimeError(f"OPENAI API Key fehlt in Umgebungsvariable {api_key_env}.")
#     openai.api_key = api_key
#
#     temperature = float(kwargs.get("temperature", extra.get("temperature", 0.2)))
#     response = openai.ChatCompletion.create(
#         model=model or "gpt-4.1-mini",
#         temperature=temperature,
#         messages=[
#             {"role": "system", "content": "Du bist ein hilfreiches Modell im MMS-Forschungsprojekt."},
#             {"role": "user", "content": prompt},
#         ],
#     )
#     return response["choices"][0]["message"]["content"]


def call_llm(prompt: str, task: Optional[str] = None, **kwargs: Any) -> str:
    """
    Zentrale LLM-Aufruffunktion.

    - Liest Konfiguration aus llm_config.json
    - Wählt Backend/Modell, ggf. Task-spezifisch
    - Gibt den reinen Text-Output des Modells zurück

    Parameter:
    - prompt: vollständiger Prompt (inkl. Protokolltext)
    - task: logischer Aufgabenname (z.B. "generate_domains", "generate_problems")
    - kwargs: optionale Zusatzparameter (z.B. temperature, max_tokens)

    Rückgabewert:
    - reiner Text-String der Modellantwort
    """
    cfg = LLMConfig.load()
    resolved = _resolve_task_config(cfg, task)
    backend = resolved["backend"]
    model = resolved["model"]
    extra = resolved["extra"]

    if backend == "dummy":
        return _backend_dummy(prompt, backend, model, extra, **kwargs)

    if backend == "not_configured":
        return _backend_not_configured(prompt, backend, model, extra, **kwargs)

    # Hier können weitere Backends ergänzt werden:
    #
    # if backend == "openai_chat":
    #     return _backend_openai_chat(prompt, backend, model, extra, **kwargs)
    #
    # if backend == "local_http":
    #     return _backend_local_http(prompt, backend, model, extra, **kwargs)

    raise RuntimeError(f"Unbekanntes LLM-Backend in llm_config.json: {backend!r}")
