"""
EduBridge AI - LLM Engine
Handles communication with local LLMs running on AMD ROCm via Ollama.
"""

import os
from typing import Optional
from langchain_community.llms import Ollama
from langchain_core.language_models import BaseLLM


class ROCmLLMEngine:
    """
    Wraps Ollama LLM backend optimized for AMD ROCm.
    Supports model selection and basic health checks.
    """

    def __init__(
        self,
        model: str = "mistral",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
    ):
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self._llm: Optional[BaseLLM] = None

    def load(self) -> BaseLLM:
        """Initialize and return the LLM instance."""
        print(f"[ROCmLLMEngine] Loading model '{self.model}' via Ollama at {self.base_url}")
        self._llm = Ollama(
            model=self.model,
            base_url=self.base_url,
            temperature=self.temperature,
        )
        return self._llm

    @property
    def llm(self) -> BaseLLM:
        if self._llm is None:
            return self.load()
        return self._llm

    def health_check(self) -> bool:
        """Ping the Ollama server to verify it's running."""
        try:
            import httpx
            resp = httpx.get(f"{self.base_url}/api/tags", timeout=5)
            return resp.status_code == 200
        except Exception as e:
            print(f"[ROCmLLMEngine] Health check failed: {e}")
            return False

    def list_available_models(self) -> list[str]:
        """List all models available in the local Ollama instance."""
        try:
            import httpx
            resp = httpx.get(f"{self.base_url}/api/tags", timeout=5)
            data = resp.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []


# Singleton instance
_engine: Optional[ROCmLLMEngine] = None


def get_llm_engine() -> ROCmLLMEngine:
    global _engine
    if _engine is None:
        _engine = ROCmLLMEngine(
            model=os.getenv("LLM_MODEL", "mistral"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
        )
    return _engine
