"""Proveedor de inferencia para modelos de pesos abiertos servidos por Groq."""

import os

from groq import Groq

from src.providers.base_provider import BaseProvider

# --- Constantes del proveedor (nada de "magic strings/numbers" inline) ---
GROQ_API_KEY_ENV_VAR = "GROQ_API_KEY"
# Elegir un ID disponible de la familia LLaMA, según la justificación del informe.
# Se configura en .env porque el catálogo de Groq puede cambiar.
GROQ_MODEL_NAME_ENV_VAR = "GROQ_MODEL_NAME"
GROQ_TEMPERATURE = 0.7


class GroqProvider(BaseProvider):
    """Genera respuestas usando un modelo de pesos abiertos vía la API de Groq."""

    def __init__(self):
        api_key = os.environ.get(GROQ_API_KEY_ENV_VAR)
        if not api_key:
            raise ValueError(
                f"Falta la variable de entorno {GROQ_API_KEY_ENV_VAR}. "
                "Obtené una key gratuita en console.groq.com y agregala a tu archivo .env."
            )
        self._model_name = os.environ.get(GROQ_MODEL_NAME_ENV_VAR)
        if not self._model_name:
            raise ValueError(
                f"Falta la variable de entorno {GROQ_MODEL_NAME_ENV_VAR}. "
                "Definila en .env con el ID de un modelo LLaMA disponible en Groq."
            )
        self._client = Groq(api_key=api_key)

    def generate(self, prompt: str) -> str:
        try:
            respuesta = self._client.chat.completions.create(
                model=self._model_name,
                temperature=GROQ_TEMPERATURE,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as error:
            raise RuntimeError(
                f"Error al consultar la API de Groq: {error}"
            ) from error

        return respuesta.choices[0].message.content
