import json

input_path = "input.json"
top_n = 10

def read_records():
    records = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                print("Skipping line {}: not valid JSON".format(line_number))
                continue
            text = record.get("text")
            if not isinstance(text, str):
                print("Skipping line {}: missing or non-string 'text' field".format(line_number))
                continue
            records.append(record)
    return records

def build_entry_stats(records):
    stats = []
    for index, record in enumerate(records, start=1):
        text = record["text"]
        char_count = len(text)
        word_count = len(text.split())
        preview = text.strip().replace("\n", " ")[:80]
        stats.append({
            "index": index,
            "label": record.get("label"),
            "page": record.get("page"),
            "char_count": char_count,
            "word_count": word_count,
            "preview": preview,
        })
    return stats

def print_report(stats):
    total_entries = len(stats)
    if total_entries == 0:
        print("No entries with a 'text' field found in: " + input_path)
        return
    total_chars = sum(s["char_count"] for s in stats)
    total_words = sum(s["word_count"] for s in stats)
    print("Total entries found: {}".format(total_entries))
    print("Total characters: {}".format(total_chars))
    print("Total words: {}".format(total_words))
    print("Average characters per entry: {:.1f}".format(total_chars / total_entries))
    print("Average words per entry: {:.1f}".format(total_words / total_entries))
    print("")
    print("Top {} longest entries by word count:".format(min(top_n, total_entries)))
    ranked = sorted(stats, key=lambda s: s["word_count"], reverse=True)
    for rank, s in enumerate(ranked[:top_n], start=1):
        print("{}. Entry {} (label={}, page={}) - {} words, {} chars - \"{}...\"".format(
            rank, s["index"], s["label"], s["page"], s["word_count"], s["char_count"], s["preview"]))

def main():
    records = read_records()
    stats = build_entry_stats(records)
    print_report(stats)

if __name__ == "__main__":
    main()
