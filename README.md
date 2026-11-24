# RoadDefect Reliability Hackathon

Develop reliable computer-vision models for detecting road-surface defects.

The challenge uses the [RDD2022 dataset](https://www.kaggle.com/datasets/aliabdelmenam/rdd-2022) for development. Final evaluation is performed on a private, unannotated test set. Participants must submit predictions only; the organizers retain the annotations and run the evaluation.

## Challenge goals

1. Detect road defects accurately.
2. Build models that remain reliable when deployed on unseen road images.
3. Explicitly control false alarms around a target false-alarm rate of **5%**.

## Defect classes

The default label set follows RDD2022:

| Class ID | Class |
| ---: | --- |
| 0 | Longitudinal crack |
| 1 | Transverse crack |
| 2 | Alligator crack |
| 3 | Pothole |

## Evaluation

The leaderboard reports two complementary metrics:

- **mIoU@50**: mean IoU of class-aware, one-to-one matched detections at IoU >= 0.50.
- **Reliability@5**: a score that rewards a false-alarm rate close to the target of 5%.

The default reliability definition is:

```text
Reliability@5 = max(0, 1 - abs(FAR - 0.05) / 0.05)
```

`FAR` is the image-level false-alarm rate: the proportion of images with at least one predicted defect when the ground-truth image contains no defect. The target can be changed by the organizers through the challenge configuration, without changing the submission format.

The default final score is:

```text
Final score = 0.80 * mIoU@50 + 0.20 * Reliability@5
```

The two component scores are always shown separately. See [EVALUATION.md](EVALUATION.md) for the exact matching and edge-case rules.

## Modeling ideas

Participants are free to choose their approach. The following directions are
intended as starting points rather than requirements:

- **Real-time detectors:** YOLO-family models are a strong baseline when
  inference speed and a simple deployment pipeline matter.
- **Transformer detectors:** DETR-style models, including Deformable DETR,
  DINO and related architectures, can provide strong global context and
  competitive localization.
- **Other established baselines:** Faster R-CNN, RetinaNet and hybrid CNN-
  transformer detectors are also valid choices.
- **Foundation-model fine-tuning:** a pretrained vision or vision-language
  foundation model can be fine-tuned, fully or with parameter-efficient
  methods such as adapters or LoRA. Participants should document the
  pretrained weights and any external data used.
- **Self-supervised learning (SSL):** the unannotated images may be useful for
  domain adaptation or representation learning before supervised fine-tuning.
  JEPA-style objectives are one example; other SSL methods are welcome if
  their use complies with the rules.

### Confidence and uncertainty

The `confidence` field should be treated as an estimate that can be calibrated,
not merely as a ranking score. Teams are encouraged to study reliability on a
held-out validation split and to report how their operating threshold relates
to the 5% false-alarm target.

Possible approaches include:

- **BALD:** Bayesian Active Learning by Disagreement can estimate epistemic
  uncertainty, for example with Monte Carlo dropout or an ensemble. High
  disagreement may indicate unfamiliar road conditions or out-of-distribution
  images.
- **Conformal prediction:** conformal methods can produce prediction sets or
  calibrated detection regions with an explicit coverage guarantee under their
  assumptions. Detection-specific adaptations should be fitted on a
  calibration split that is separate from training data.
- **Calibration:** temperature scaling, isotonic regression, class-specific
  thresholds and ensemble averaging can improve the relationship between
  confidence values and observed correctness.

Uncertainty estimates do not replace the required submission format. If they
are used, teams should explain how they are converted into predicted boxes,
confidence values and the final false-alarm operating point.

## Submission format

Submit one JSON Lines (`.jsonl`) file with one record per test image:

```json
{"image_id":"road_000001.jpg","predictions":[{"class_id":3,"confidence":0.91,"bbox":[120,80,540,410]}]}
```

Bounding boxes use pixel coordinates in `[x_min, y_min, x_max, y_max]`. Coordinates must be finite and satisfy `x_min < x_max` and `y_min < y_max`. Confidence values must be in `[0, 1]`.

The file must contain exactly one record for each test image, with no duplicate image IDs. Images with no predicted defect must use an empty `predictions` list.

An example is available in [`submission_example.jsonl`](submission_example.jsonl).

## Getting started

```bash
git clone https://github.com/<organizer>/<repository>.git
cd <repository>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Download RDD2022 from Kaggle for training and development. Do not commit the dataset or private test annotations to this repository.

```bash
python -m src.validate_submission submission_example.jsonl
```

## Suggested project structure

```text
data/                 # local data, ignored by git
notebooks/            # experiments
src/
  validate_submission.py
  train.py             # participant code
  predict.py           # participant code
submissions/          # local prediction files, ignored by git
```

## Rules

- All submitted predictions must be generated by the team submitting them.
- External pretrained weights and public datasets are allowed if disclosed in the submission report.
- Private test images and annotations must not be shared.
- Teams should provide enough information to reproduce their inference pipeline.
- The organizers may request code or a short technical report from top-ranked teams.

## Recommended submission report

Include:

- model architecture and pretrained weights;
- image resolution, augmentation and post-processing;
- confidence-threshold selection procedure;
- validation mIoU@50 and false-alarm rate;
- calibration or reliability analysis;
- compute used for training and inference.

## License and data notice

This repository contains challenge documentation and utilities. The RDD2022 images and annotations are not included. Participants must comply with the dataset's terms and the terms of any external pretrained model or dataset they use.

