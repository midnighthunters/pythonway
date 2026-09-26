# Q0922 · Audio prompt injection and ultrasonic command evasion

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Prompt injection defense | Easy |

## Question

Explain audio prompt injection in speech-to-text GenAI models, and write Python code demonstrating audio spectrum frequency filtering for ultrasonic commands.

## Answer

Voice-enabled LLM assistants (e.g. Whisper + LLM) can be triggered by audio containing imperceptible high-frequency acoustic signals (18 kHz - 22 kHz, above human hearing) or commands hidden inside background music.

Preprocessing audio with a bandpass filter (300 Hz - 8,000 Hz, the human vocal range) strips out ultrasonic and sub-audible attack signals before transcription.

```python
from typing import List


def filter_audio_frequencies(frequencies: List[float], min_hz: float = 300.0, max_hz: float = 8000.0) -> List[float]:
    """Bandpass filter keeping only human vocal frequencies."""
    return [f for f in frequencies if min_hz <= f <= max_hz]


# Sample audio frequency components (in Hz)
audio_spectrum = [120.0, 450.0, 1200.0, 3500.0, 19500.0, 22000.0]

filtered = filter_audio_frequencies(audio_spectrum)
assert 19500.0 not in filtered  # Ultrasonic attack frequency stripped
assert 22000.0 not in filtered
assert 450.0 in filtered
assert 1200.0 in filtered
```

## Likely follow-ups

- How does audio steganography hide instructions inside harmless spoken podcasts?
- What role does speaker verification (biometrics) play in voice-command authorization?

---

[← Q0921](../../batch_10_ai_security_responsible_ai/0921_multimodal_prompt_injection_in_images_and_visual_typography/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0923 →](../../batch_10_ai_security_responsible_ai/0923_model_hallucination_vs_adversarial_manipulation/README.md)
