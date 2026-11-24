"""Validate the public JSONL submission format."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

CLASS_IDS = {0, 1, 2, 3}


def validate(path: Path) -> int:
    seen: set[str] = set()
    errors: list[str] = []

    for line_number, raw_line in enumerate(path.read_text().splitlines(), start=1):
        if not raw_line.strip():
            errors.append(f"line {line_number}: empty lines are not allowed")
            continue
        try:
            record = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON ({exc.msg})")
            continue

        image_id = record.get("image_id")
        predictions = record.get("predictions")
        if not isinstance(image_id, str) or not image_id:
            errors.append(f"line {line_number}: image_id must be a non-empty string")
        elif image_id in seen:
            errors.append(f"line {line_number}: duplicate image_id {image_id!r}")
        else:
            seen.add(image_id)

        if not isinstance(predictions, list):
            errors.append(f"line {line_number}: predictions must be a list")
            continue

        for prediction_number, prediction in enumerate(predictions, start=1):
            prefix = f"line {line_number}, prediction {prediction_number}"
            if not isinstance(prediction, dict):
                errors.append(f"{prefix}: prediction must be an object")
                continue

            class_id = prediction.get("class_id")
            if class_id not in CLASS_IDS:
                errors.append(f"{prefix}: class_id must be one of {sorted(CLASS_IDS)}")

            confidence = prediction.get("confidence")
            if (
                not isinstance(confidence, (int, float))
                or isinstance(confidence, bool)
                or not math.isfinite(confidence)
                or not 0 <= confidence <= 1
            ):
                errors.append(f"{prefix}: confidence must be a finite number in [0, 1]")

            bbox = prediction.get("bbox")
            if (
                not isinstance(bbox, list)
                or len(bbox) != 4
                or any(
                    not isinstance(value, (int, float))
                    or isinstance(value, bool)
                    or not math.isfinite(value)
                    for value in bbox
                )
                or bbox[0] >= bbox[2]
                or bbox[1] >= bbox[3]
            ):
                errors.append(
                    f"{prefix}: bbox must be [x_min, y_min, x_max, y_max] with "
                    "finite values and positive area"
                )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"Valid submission: {len(seen)} image(s)")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m src.validate_submission <submission.jsonl>", file=sys.stderr)
        return 2
    return validate(Path(sys.argv[1]))


if __name__ == "__main__":
    raise SystemExit(main())
