# Q0063 · Estimate image token cost

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Multimodal | Medium |

## Question

Implement an image-token estimator for a tile-based vision model: scale to fit within 2048×2048, then scale so the shortest side is at most 768, then charge a base cost plus a cost per 512-pixel tile.

## Answer

This follows the formula one major provider historically published for high-detail images (85 base tokens plus 170 per 512 px tile). Treat the constants as illustrative and check current documentation per model.

```python
import math


def image_tokens(width: int, height: int, base: int = 85, per_tile: int = 170, tile: int = 512) -> int:
    w, h = float(width), float(height)
    s = min(1.0, 2048 / max(w, h))
    w, h = w * s, h * s
    s = min(1.0, 768 / min(w, h))
    w, h = w * s, h * s
    return base + per_tile * math.ceil(w / tile) * math.ceil(h / tile)


assert image_tokens(1024, 1024) == 765
assert image_tokens(2048, 4096) == 1105
assert image_tokens(512, 512) == 255
```

A 1024×1024 image becomes 768×768, which is 4 tiles, so 765 tokens. Use estimators like this for budgeting and quota checks before sending, and downscale images when full detail isn't needed.

## Likely follow-ups

- When would you choose the low-detail mode?

---

[← Q0062](../../batch_01_llm_fundamentals/0062_how_vision_language_models_see_images/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0064 →](../../batch_01_llm_fundamentals/0064_model_cascade_by_confidence/README.md)
