# Evaluation protocol

## 1. Detection matching

For each image, predictions and ground-truth boxes are matched greedily in descending prediction-confidence order:

1. a prediction can match only a ground-truth box of the same class;
2. a match requires IoU >= 0.50;
3. each prediction and ground-truth box can be used at most once.

For matched pairs, IoU is the intersection-over-union of the two boxes. The image score is the mean IoU of matched pairs. If an image has no matched pair, its detection score is zero. `mIoU@50` is the mean image score across the evaluation set.

Organizers should publish whether predictions below a fixed confidence threshold are removed before matching. The recommended default is to evaluate all submitted predictions and use the confidence field only for matching order and reliability analysis.

## 2. False-alarm rate

An image is a negative image when its ground-truth annotation contains no defect box. A negative image is a false alarm when it contains at least one submitted prediction that passes the organizer's confidence threshold.

```text
FAR = false-alarm negative images / all negative images
```

If the test set contains no negative images, `Reliability@5` is reported as unavailable and is excluded from the final score; the organizers must disclose this exception.

## 3. Reliability@target

For target false-alarm rate `t` (default `t = 0.05`):

```text
Reliability@target = max(0, 1 - abs(FAR - t) / t)
```

This score is 1.0 at the target, 0.0 when the observed FAR is at least twice the target, and also 0.0 when the observed FAR is zero. The latter is intentional: the challenge rewards operating at the requested risk budget rather than simply suppressing every detection.

Organizers may publish a second diagnostic metric, such as recall at the selected operating point, but it must not replace the primary definition without announcing the change before the final test.

## 4. Final score

The default aggregate is:

```text
Final score = 0.80 * mIoU@50 + 0.20 * Reliability@5
```

The leaderboard must display `mIoU@50`, `FAR`, `Reliability@5` and `Final score` separately.

## 5. Reproducibility and ties

If two teams have the same final score, rank them by higher `mIoU@50`, then by lower absolute FAR error `abs(FAR - 0.05)`, then by earlier valid submission time.

