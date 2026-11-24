# Challenge brief

## Why this challenge?

Road defects such as cracks and potholes are important signals for road maintenance and transport safety. A detector that performs well on a benchmark can still be difficult to trust in practice: camera conditions change, roads differ between regions, and false alarms can quickly overwhelm inspection teams.

This hackathon therefore evaluates both detection quality and operational reliability.

## Data

The development data is based on [RDD2022](https://www.kaggle.com/datasets/aliabdelmenam/rdd-2022), a road-damage image dataset. Organizers should publish the precise train/validation split, preprocessing rules and class mapping used for the event.

The final test set is supplied without annotations. Test images must not be manually annotated or augmented with information obtained from the hidden labels.

## Track

The default track is object detection with four classes:

1. longitudinal crack;
2. transverse crack;
3. alligator crack;
4. pothole.

Teams may use any detector, framework or training strategy that satisfies the rules.

## Recommended timeline

| Phase | Suggested duration |
| --- | ---: |
| Registration and data familiarization | 1 week |
| Model development | 2 weeks |
| Reliability and calibration experiments | 1 week |
| Final submissions | 2-3 days |
| Reproducibility checks and results | 1 week |

## Deliverables

Each team submits:

1. one prediction file in the required JSONL format;
2. a short technical report;
3. a disclosure of external data, pretrained weights and third-party code;
4. optionally, inference code for reproducibility.

## Reliability focus

Teams are encouraged to report more than a single confidence threshold. Useful analyses include:

- false-alarm rate versus confidence threshold;
- performance by defect class;
- performance by image source or geographic domain, when available;
- calibration curves and expected calibration error;
- sensitivity of results to image quality and weather conditions.

