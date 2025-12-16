def review_annotations(annotations, allowed_labels):

      """
    Reviews AI annotation data for common quality issues.
    Flags missing labels, invalid labels, and low-quality text.
    """
      
    issues = {}
    total_items = len(annotations)
    seen_texts = set()
    #duplicate detection
    for item in annotations:
        text = item["text"]
        label = item["label"]
        #makes sure each text has a set of issues
        if text not in issues:
            issues[text] = set()
        # Missing label      
        if label == "":
            issues[text].add("missing label")
        # Invalid label    
        elif label not in allowed_labels:
            issues[text].add("invalid label")
        # Low-quality text
        if len(text) < 4:
            issues[text].add("text too short")
        #Duplicate text    
        if text in seen_texts:
            issues[text].add("duplicate text")
        else:
            seen_texts.add(text)
            

    return issues, total_items

def summarize_issues(annotations, allowed_labels):
    # counts issue types
    missing_label = 0
    invalid_label = 0
    text_too_short = 0

    for item in annotations:
        if item["label"] == "":
            missing_label += 1
        elif item["label"] not in allowed_labels:
            invalid_label += 1

        if len(item["text"]) < 4:
            text_too_short += 1

    return missing_label, invalid_label, text_too_short

annotations = [
    {"text": "Start", "label": "Start/End"},
    {"text": "Go", "label": "Process"},
    {"text": "Check", "label": ""},
    {"text": "Go", "label": "Process"},      # duplicate
    {"text": "End", "label": "Stop"},
    {"text": "End", "label": "Stop"}          # duplicate
]

allowed_labels = ["Process", "Decision", "Input/Output", "Start/End"]


issues, total = review_annotations(annotations, allowed_labels)
missing, invalid, short_text = summarize_issues (annotations, allowed_labels)
items_with_issues = sum(1 for problems in issues.values() if problems)

print("QA Review Report")
print("----------------")
print("Total items:", total)
print("Items with issues:", items_with_issues)
print("Missing labels:", missing)
print("Invalid labels:", invalid)
print("Text too short:", short_text)

error_rate = (items_with_issues / total) * 100

print(f"\nError rate: {error_rate:.1f}%")


for text, problems in issues.items():
    if problems:
        print(f"{text}:")
        for problem in problems:
            print(f" - {problem}")


with open("qa_report.txt", "w") as report:
    report.write("QA Review Report\n")
    report.write("----------------\n")
    report.write(f"Total items: {total}\n")
    report.write(f"Items with issues: {items_with_issues}\n")
    report.write(f"Missing labels: {missing}\n")
    report.write(f"Invalid labels: {invalid}\n")
    report.write(f"Text too short: {short_text}\n")
    report.write(f"Error rate: {error_rate:.1f}%\n\n")

    for text, problems in issues.items():
        if problems:
            report.write(f"{text}:\n")
            for problem in problems:
                report.write(f" - {problem}\n")
)
