def review_annotations(annotations, allowed_labels):
    """
    Reviews AI annotation data for common quality issues.
    Flags missing labels, invalid labels, and low-quality text.
    """

    issues = []

    for item in annotations:
        # Missing label
        if item["label"] == "":
            issues.append(item["text"] + " (missing label)")

        # Invalid label
        elif item["label"] not in allowed_labels:
            issues.append(item["text"] + " (invalid label)")

        # Low-quality text
        if len(item["text"]) < 4:
            issues.append(item["text"] + " (text too short)")

    return issues


if __name__ == "__main__":
    annotations = [
        {"text": "Go", "label": "Process"},
        {"text": "Load Data", "label": "Process"},
        {"text": "OK", "label": ""},
        {"text": "Save", "label": "Store"}
    ]

    allowed_labels = ["Process", "Decision", "Input/Output", "Start/End"]

    issues = review_annotations(annotations, allowed_labels)

    print("QA Review Report:")
    for issue in issues:
        print("-", issue)
