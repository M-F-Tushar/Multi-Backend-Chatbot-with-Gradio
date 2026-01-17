import os
import sys
import json
import time
import argparse
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Optional
from dotenv import load_dotenv

load_dotenv(override=True)

try:
    from openai import OpenAI
except ImportError:
    print("❌ Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Error: google-generativeai package not installed. Run: pip install google-generativeai")
    sys.exit(1)


OLLAMA_MODELS = [
    "llama3.2:1b", "llama3.2:3b", "llama3.1:8b", "llama3.1:70b", "llama3.3:70b",
    "mistral:7b", "mixtral:8x7b", "codellama:7b", "codellama:34b",
    "phi3:mini", "phi3:medium", "gemma2:9b", "qwen2.5:7b", "deepseek-r1:7b"
]


OPENROUTER_MODELS = [
    # Flagship & High Performance
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    # Reasoning & Thinking
    "tngtech/deepseek-r1t2-chimera:free",
    "tngtech/deepseek-r1t-chimera:free",
    "tngtech/tng-r1t-chimera:free",
    "allenai/olmo-3-32b-think:free",
    "alibaba/tongyi-deepresearch-30b-a3b:free",
    "xiaomi/mimo-v2-flash:free",
    "nex-agi/deepseek-v3.1-nex-n1:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    # Coding
    "kwaipilot/kat-coder-pro:free",
    # Qwen Models

    "qwen/qwen3-4b:free",
    # Google Gemma
    "google/gemma-3-27b-it:free",
    "google/gemma-3-12b-it:free",
    "google/gemma-3-4b-it:free",
    "google/gemma-3n-e2b-it:free",
    # NVIDIA
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "nvidia/nemotron-nano-9b-v2:free",
    # Mistral
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    # Other Models
    "openai/gpt-oss-20b:free",
    "z-ai/glm-4.5-air:free",
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
    "arcee-ai/trinity-mini:free"
]



# GitHub Models 
GITHUB_MODELS = [
    # OpenAI GPT-5 Series (NEW)
    "gpt-5", "gpt-5-chat", "gpt-5-mini", "gpt-5-nano",
    # OpenAI Reasoning (NEW)
    "o3", "o3-mini", "o4-mini",
    # OpenAI GPT-4 (Working)
    "gpt-4o", "gpt-4o-mini",
    # Meta Llama (Working)
    "Llama-3.3-70B-Instruct",
    "Llama-3.2-90B-Vision-Instruct",
    "Llama-3.2-11B-Vision-Instruct",
    # Microsoft Phi-4 (NEW)
    "Phi-4", "Phi-4-reasoning", "Phi-4-multimodal-instruct",
    "Phi-4-mini-reasoning", "Phi-4-mini-instruct",
    # Mistral (Working)
    "Codestral-2501",
    # DeepSeek (Working + NEW)
    "DeepSeek-R1", "DeepSeek-V3-0324", "MAI-DS-R1"
]



# Groq Models 
GROQ_MODELS = [
    # Meta Llama 4 (NEW)
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    # Meta Llama 3.x (Working)
    "llama-3.3-70b-versatile", "llama-3.1-8b-instant",
    # OpenAI Open Source (Working + NEW)
    "openai/gpt-oss-120b", "openai/gpt-oss-20b",
    "openai/gpt-oss-safeguard-20b",
    # Moonshot AI (NEW)
    "moonshotai/kimi-k2-instruct-0905",
    # Qwen (NEW)
    "qwen/qwen3-32b",
    # Audio (Whisper)
    "whisper-large-v3", "whisper-large-v3-turbo"
]

# Gemini Models 
GEMINI_MODELS = [
    # Gemini 3 Preview (NEW - may require quota)
    "gemini-3-pro-preview", "gemini-3-pro-image-preview",
    # Gemini 2.5 (Working)
    "gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite",
    # Gemini 2.0 (Stable)
    "gemini-2.0-flash-exp",
    "gemini-robotics-er-1.5-preview",
    # Gemma 3 Open Models (Working)
    "gemma-3-27b-it", "gemma-3-12b-it", "gemma-3-4b-it", "gemma-3-1b-it",
    # Gemma 3n Nano (for devices)
    "gemma-3n-e4b-it", "gemma-3n-e2b-it"
]



class ErrorCategory(Enum):
    WORKING = "WORKING"
    AUTH_ERROR = "AUTH_ERROR"
    NOT_FOUND = "NOT_FOUND"
    RATE_LIMITED = "RATE_LIMITED"
    SERVER_ERROR = "SERVER_ERROR"
    NOT_INSTALLED = "NOT_INSTALLED"  
    TIMEOUT = "TIMEOUT"
    CONNECTION_ERROR = "CONNECTION_ERROR"
    AUDIO_MODEL = "AUDIO_MODEL" 
    ERROR = "ERROR"


@dataclass
class ValidationResult:
    provider: str
    model: str
    status: ErrorCategory
    response_time_ms: Optional[float] = None
    error_message: Optional[str] = None
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()



class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def colored(text: str, color: str) -> str:
    """Return colored text for terminal output."""
    return f"{color}{text}{Colors.RESET}"


def status_icon(status: ErrorCategory) -> str:
    """Get status icon and color for a result."""
    icons = {
        ErrorCategory.WORKING: colored("✅ WORKING", Colors.GREEN),
        ErrorCategory.AUTH_ERROR: colored("🔑 AUTH_ERROR", Colors.RED),
        ErrorCategory.NOT_FOUND: colored("❌ NOT_FOUND", Colors.RED),
        ErrorCategory.RATE_LIMITED: colored("⏳ RATE_LIMITED", Colors.YELLOW),
        ErrorCategory.SERVER_ERROR: colored("💥 SERVER_ERROR", Colors.RED),
        ErrorCategory.NOT_INSTALLED: colored("📦 NOT_INSTALLED", Colors.YELLOW),
        ErrorCategory.TIMEOUT: colored("⏱️ TIMEOUT", Colors.YELLOW),
        ErrorCategory.CONNECTION_ERROR: colored("🔌 CONNECTION_ERROR", Colors.RED),
        ErrorCategory.AUDIO_MODEL: colored("🎵 AUDIO_MODEL", Colors.CYAN),
        ErrorCategory.ERROR: colored("❌ ERROR", Colors.RED),
    }
    return icons.get(status, colored("❓ UNKNOWN", Colors.YELLOW))


class BaseValidator:
    """Base class for model validators."""
    
    def __init__(self, delay: float = 1.0, timeout: float = 30.0):
        self.delay = delay
        self.timeout = timeout
    
    def categorize_error(self, error: Exception) -> tuple[ErrorCategory, str]:
        """Categorize an exception into an error category."""
        error_str = str(error).lower()
        
        # Check for common error patterns
        if "401" in error_str or "unauthorized" in error_str or "invalid api key" in error_str:
            return ErrorCategory.AUTH_ERROR, str(error)
        elif "404" in error_str or "not found" in error_str or "does not exist" in error_str:
            return ErrorCategory.NOT_FOUND, str(error)
        elif "429" in error_str or "rate limit" in error_str or "too many requests" in error_str:
            return ErrorCategory.RATE_LIMITED, str(error)
        elif "500" in error_str or "502" in error_str or "503" in error_str or "server error" in error_str:
            return ErrorCategory.SERVER_ERROR, str(error)
        elif "timeout" in error_str or "timed out" in error_str:
            return ErrorCategory.TIMEOUT, str(error)
        elif "connection" in error_str or "connect" in error_str:
            return ErrorCategory.CONNECTION_ERROR, str(error)
        else:
            return ErrorCategory.ERROR, str(error)


class OllamaValidator(BaseValidator):
    """Validator for local Ollama models."""
    
    def __init__(self, delay: float = 0.5, timeout: float = 30.0):
        super().__init__(delay, timeout)
        self.base_url = "http://localhost:11434/v1"
        self.client = None
    
    def validate_model(self, model: str) -> ValidationResult:
        """Validate a single Ollama model."""
        start_time = time.time()
        
        try:
            if self.client is None:
                self.client = OpenAI(base_url=self.base_url, api_key="ollama")
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5,
                timeout=self.timeout
            )
            
            elapsed_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                provider="Ollama",
                model=model,
                status=ErrorCategory.WORKING,
                response_time_ms=round(elapsed_ms, 2)
            )
            
        except Exception as e:
            error_str = str(e).lower()
            elapsed_ms = (time.time() - start_time) * 1000
            
            # Check if model is not installed
            if "model" in error_str and ("not found" in error_str or "does not exist" in error_str):
                return ValidationResult(
                    provider="Ollama",
                    model=model,
                    status=ErrorCategory.NOT_INSTALLED,
                    response_time_ms=round(elapsed_ms, 2),
                    error_message=f"Model not pulled. Run: ollama pull {model}"
                )
            
            # Check if Ollama is not running
            if "connection" in error_str or "connect" in error_str:
                return ValidationResult(
                    provider="Ollama",
                    model=model,
                    status=ErrorCategory.CONNECTION_ERROR,
                    response_time_ms=round(elapsed_ms, 2),
                    error_message="Ollama not running. Start with: ollama serve"
                )
            
            category, msg = self.categorize_error(e)
            return ValidationResult(
                provider="Ollama",
                model=model,
                status=category,
                response_time_ms=round(elapsed_ms, 2),
                error_message=msg
            )


class OpenRouterValidator(BaseValidator):
    """Validator for OpenRouter models."""
    
    def __init__(self, delay: float = 1.0, timeout: float = 30.0):
        super().__init__(delay, timeout)
        self.base_url = "https://openrouter.ai/api/v1"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.client = None
    
    def validate_model(self, model: str) -> ValidationResult:
        """Validate a single OpenRouter model."""
        start_time = time.time()
        
        if not self.api_key:
            return ValidationResult(
                provider="OpenRouter",
                model=model,
                status=ErrorCategory.AUTH_ERROR,
                error_message="OPENROUTER_API_KEY not set in .env"
            )
        
        try:
            if self.client is None:
                self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5,
                timeout=self.timeout,
                extra_headers={
                    "HTTP-Referer": "http://localhost:7860",
                    "X-Title": "Model Validator"
                }
            )
            
            elapsed_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                provider="OpenRouter",
                model=model,
                status=ErrorCategory.WORKING,
                response_time_ms=round(elapsed_ms, 2)
            )
            
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            category, msg = self.categorize_error(e)
            return ValidationResult(
                provider="OpenRouter",
                model=model,
                status=category,
                response_time_ms=round(elapsed_ms, 2),
                error_message=msg
            )


class GitHubValidator(BaseValidator):
    """Validator for GitHub Models."""
    
    def __init__(self, delay: float = 1.0, timeout: float = 30.0):
        super().__init__(delay, timeout)
        self.base_url = "https://models.github.ai/inference"
        self.api_key = os.getenv("GITHUB_TOKEN")
        self.client = None
    
    def validate_model(self, model: str) -> ValidationResult:
        """Validate a single GitHub model."""
        start_time = time.time()
        
        if not self.api_key:
            return ValidationResult(
                provider="GitHub",
                model=model,
                status=ErrorCategory.AUTH_ERROR,
                error_message="GITHUB_TOKEN not set in .env"
            )
        
        try:
            if self.client is None:
                self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
            
            # Fix for newer OpenAI models (o1, o3, o4, gpt-5)
            # They require 'max_completion_tokens' instead of 'max_tokens'
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "Hi"}],
                "timeout": self.timeout
            }
            
            o_series = {"o1", "o1-mini", "o1-preview", "o3", "o3-mini", "o4", "o4-mini", "gpt-5"}
            is_o_series = any(s in model.lower() for s in o_series)
            
            if is_o_series:
                payload["max_completion_tokens"] = 5
            else:
                payload["max_tokens"] = 5
                
            response = self.client.chat.completions.create(**payload)
            
            elapsed_ms = (time.time() - start_time) * 1000

            return ValidationResult(
                provider="GitHub",
                model=model,
                status=ErrorCategory.WORKING,
                response_time_ms=round(elapsed_ms, 2)
            )
            
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            category, msg = self.categorize_error(e)
            return ValidationResult(
                provider="GitHub",
                model=model,
                status=category,
                response_time_ms=round(elapsed_ms, 2),
                error_message=msg
            )


class GroqValidator(BaseValidator):
    """Validator for Groq models."""
    
    def __init__(self, delay: float = 1.0, timeout: float = 30.0):
        super().__init__(delay, timeout)
        self.base_url = "https://api.groq.com/openai/v1"
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        # Whisper models need audio input, not text
        self.audio_models = {"whisper-large-v3", "whisper-large-v3-turbo", "distil-whisper-large-v3-en"}
    
    def validate_model(self, model: str) -> ValidationResult:
        """Validate a single Groq model."""
        start_time = time.time()
        
        if not self.api_key:
            return ValidationResult(
                provider="Groq",
                model=model,
                status=ErrorCategory.AUTH_ERROR,
                error_message="GROQ_API_KEY not set in .env"
            )
        
        # Skip Whisper models (they need audio input)
        if model in self.audio_models:
            return ValidationResult(
                provider="Groq",
                model=model,
                status=ErrorCategory.AUDIO_MODEL,
                error_message="Audio transcription model - requires audio file input"
            )
        
        try:
            if self.client is None:
                self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5,
                timeout=self.timeout
            )
            
            elapsed_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                provider="Groq",
                model=model,
                status=ErrorCategory.WORKING,
                response_time_ms=round(elapsed_ms, 2)
            )
            
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            category, msg = self.categorize_error(e)
            return ValidationResult(
                provider="Groq",
                model=model,
                status=category,
                response_time_ms=round(elapsed_ms, 2),
                error_message=msg
            )


class GeminiValidator(BaseValidator):
    """Validator for Google Gemini models."""
    
    def __init__(self, delay: float = 1.0, timeout: float = 30.0):
        super().__init__(delay, timeout)
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.configured = False
        # TTS models need different API
        self.tts_models = {"gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"}
    
    def validate_model(self, model: str) -> ValidationResult:
        """Validate a single Gemini model."""
        start_time = time.time()
        
        if not self.api_key:
            return ValidationResult(
                provider="Gemini",
                model=model,
                status=ErrorCategory.AUTH_ERROR,
                error_message="GOOGLE_API_KEY not set in .env"
            )
        
        # Skip TTS models (they need different API)
        if model in self.tts_models:
            return ValidationResult(
                provider="Gemini",
                model=model,
                status=ErrorCategory.AUDIO_MODEL,
                error_message="TTS model - requires text-to-speech API"
            )
        
        try:
            if not self.configured:
                genai.configure(api_key=self.api_key)
                self.configured = True
            
            gemini = genai.GenerativeModel(model_name=model)
            response = gemini.generate_content(
                "Hi",
                generation_config={"max_output_tokens": 5}
            )
            
            elapsed_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                provider="Gemini",
                model=model,
                status=ErrorCategory.WORKING,
                response_time_ms=round(elapsed_ms, 2)
            )
            
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            category, msg = self.categorize_error(e)
            return ValidationResult(
                provider="Gemini",
                model=model,
                status=category,
                response_time_ms=round(elapsed_ms, 2),
                error_message=msg
            )


# ============================================================================
# Main Validator Class
# ============================================================================

class ModelValidator:
    """Main orchestrator for validating models across all providers."""
    
    PROVIDERS = {
        "ollama": (OllamaValidator, OLLAMA_MODELS, 0.5),
        "openrouter": (OpenRouterValidator, OPENROUTER_MODELS, 1.0),
        "github": (GitHubValidator, GITHUB_MODELS, 1.0),
        "groq": (GroqValidator, GROQ_MODELS, 1.0),
        "gemini": (GeminiValidator, GEMINI_MODELS, 1.0),
    }
    
    def __init__(self, providers: list[str] = None, delay: float = None, 
                 timeout: float = 30.0, quick_test: bool = False):
        self.timeout = timeout
        self.quick_test = quick_test
        self.delay_override = delay
        self.results: list[ValidationResult] = []
        
        # Select providers
        if providers:
            self.selected_providers = [p.lower() for p in providers if p.lower() in self.PROVIDERS]
        else:
            self.selected_providers = list(self.PROVIDERS.keys())
    
    def run(self) -> list[ValidationResult]:
        """Run validation for all selected providers and models."""
        print("\n" + "=" * 70)
        print(colored("🔍 MODEL VALIDATION REPORT", Colors.BOLD + Colors.CYAN))
        print(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70 + "\n")
        
        # Check API keys status
        self._print_api_status()
        
        total_models = 0
        for provider_name in self.selected_providers:
            _, models, _ = self.PROVIDERS[provider_name]
            total_models += len(models) if not self.quick_test else 1
        
        print(f"\n📊 Testing {total_models} models across {len(self.selected_providers)} provider(s)...\n")
        
        for provider_name in self.selected_providers:
            self._validate_provider(provider_name)
        
        return self.results
    
    def _print_api_status(self):
        """Print API key configuration status."""
        print(colored("📋 API Configuration Status:", Colors.BOLD))
        
        status_items = [
            ("Ollama", "Always available (local)", True),
            ("OpenRouter", "OPENROUTER_API_KEY", bool(os.getenv("OPENROUTER_API_KEY"))),
            ("GitHub", "GITHUB_TOKEN", bool(os.getenv("GITHUB_TOKEN"))),
            ("Groq", "GROQ_API_KEY", bool(os.getenv("GROQ_API_KEY"))),
            ("Gemini", "GOOGLE_API_KEY", bool(os.getenv("GOOGLE_API_KEY"))),
        ]
        
        for name, key_name, available in status_items:
            icon = colored("✅", Colors.GREEN) if available else colored("❌", Colors.RED)
            key_status = "configured" if available else "missing"
            print(f"   {icon} {name}: {key_name} ({key_status})")
    
    def _validate_provider(self, provider_name: str):
        """Validate all models for a single provider."""
        validator_class, models, default_delay = self.PROVIDERS[provider_name]
        delay = self.delay_override if self.delay_override is not None else default_delay
        
        validator = validator_class(delay=delay, timeout=self.timeout)
        
        # Quick test mode: only test first model
        if self.quick_test:
            models = models[:1]
        
        print(colored(f"\n{'─' * 50}", Colors.BLUE))
        print(colored(f"🔌 {provider_name.upper()} ({len(models)} models)", Colors.BOLD + Colors.BLUE))
        print(colored(f"{'─' * 50}", Colors.BLUE))
        
        for i, model in enumerate(models, 1):
            result = validator.validate_model(model)
            self.results.append(result)
            
            # Print result
            time_str = f"({result.response_time_ms:.0f}ms)" if result.response_time_ms else ""
            print(f"   [{i:2}/{len(models)}] {model[:45]:<45} {status_icon(result.status)} {time_str}")
            
            if result.error_message and result.status not in [ErrorCategory.WORKING, ErrorCategory.AUDIO_MODEL]:
                # Truncate long error messages
                error_preview = result.error_message[:80] + "..." if len(result.error_message) > 80 else result.error_message
                print(colored(f"         └─ {error_preview}", Colors.YELLOW))
            
            # Rate limiting delay
            if i < len(models):
                time.sleep(delay)
    
    def generate_report(self, output_file: str = "model_validation_report.json") -> dict:
        """Generate and save a JSON report."""
        # Calculate summary statistics
        summary = {}
        for provider_name in self.selected_providers:
            provider_results = [r for r in self.results if r.provider.lower() == provider_name]
            status_counts = {}
            for result in provider_results:
                status = result.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
            summary[provider_name] = {
                "total": len(provider_results),
                "by_status": status_counts
            }
        
        # Build report
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": summary,
            "total_models": len(self.results),
            "results": [
                {
                    "provider": r.provider,
                    "model": r.model,
                    "status": r.status.value,
                    "response_time_ms": r.response_time_ms,
                    "error_message": r.error_message,
                    "timestamp": r.timestamp
                }
                for r in self.results
            ]
        }
        
        # Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def print_summary(self):
        """Print a summary of validation results."""
        print("\n" + "=" * 70)
        print(colored("📊 VALIDATION SUMMARY", Colors.BOLD + Colors.CYAN))
        print("=" * 70)
        
        for provider_name in self.selected_providers:
            provider_results = [r for r in self.results if r.provider.lower() == provider_name]
            
            working = sum(1 for r in provider_results if r.status == ErrorCategory.WORKING)
            audio = sum(1 for r in provider_results if r.status == ErrorCategory.AUDIO_MODEL)
            errors = len(provider_results) - working - audio
            
            print(f"\n{colored(provider_name.upper(), Colors.BOLD)}: {len(provider_results)} models")
            print(f"   ✅ Working: {working}")
            if audio > 0:
                print(f"   🎵 Audio/TTS: {audio}")
            if errors > 0:
                print(f"   ❌ Errors: {errors}")
                
                # Show breakdown of error types
                error_breakdown = {}
                for r in provider_results:
                    if r.status not in [ErrorCategory.WORKING, ErrorCategory.AUDIO_MODEL]:
                        error_breakdown[r.status.value] = error_breakdown.get(r.status.value, 0) + 1
                
                for error_type, count in error_breakdown.items():
                    print(f"      └─ {error_type}: {count}")
        
        # Overall totals
        total_working = sum(1 for r in self.results if r.status == ErrorCategory.WORKING)
        total_audio = sum(1 for r in self.results if r.status == ErrorCategory.AUDIO_MODEL)
        total_errors = len(self.results) - total_working - total_audio
        
        print("\n" + "─" * 70)
        print(colored("TOTAL:", Colors.BOLD))
        print(f"   ✅ Working: {total_working}/{len(self.results)} models")
        if total_audio > 0:
            print(f"   🎵 Audio/TTS (skipped): {total_audio}")
        if total_errors > 0:
            print(f"   ❌ Errors: {total_errors}")
        print()


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Validate AI models across multiple providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_models.py                      # Run all providers
  python validate_models.py --providers ollama groq
  python validate_models.py --quick-test         # Test one model per provider
  python validate_models.py --delay 2.0          # 2 second delay between requests
        """
    )
    
    parser.add_argument(
        "--providers", "-p",
        nargs="+",
        choices=["ollama", "openrouter", "github", "groq", "gemini"],
        help="Specific providers to test (default: all)"
    )
    
    parser.add_argument(
        "--delay", "-d",
        type=float,
        help="Delay in seconds between API requests (default: varies by provider)"
    )
    
    parser.add_argument(
        "--timeout", "-t",
        type=float,
        default=30.0,
        help="Timeout in seconds per request (default: 30)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="model_validation_report.json",
        help="Output file for JSON report (default: model_validation_report.json)"
    )
    
    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="Quick test mode: only test first model from each provider"
    )
    
    args = parser.parse_args()
    
    # Run validation
    validator = ModelValidator(
        providers=args.providers,
        delay=args.delay,
        timeout=args.timeout,
        quick_test=args.quick_test
    )
    
    try:
        validator.run()
        validator.print_summary()
        
        # Generate report
        report = validator.generate_report(args.output)
        print(f"📄 Report saved to: {colored(args.output, Colors.GREEN)}\n")
        
    except KeyboardInterrupt:
        print(colored("\n\n⚠️ Validation interrupted by user.", Colors.YELLOW))
        if validator.results:
            print(f"   Partial results for {len(validator.results)} models tested.")
            validator.generate_report(args.output)
            print(f"   Partial report saved to: {args.output}")
        sys.exit(1)


if __name__ == "__main__":
    main()
