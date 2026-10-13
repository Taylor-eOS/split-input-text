input_path = "input.txt"
split_marker = "[chapter]"
fallback_marker = "\n\n"
top_n = 10

def read_source_text():
    with open(input_path, "r", encoding="utf-8") as f:
        return f.read()

def select_split_marker(text):
    global split_marker
    if not text.lstrip().startswith(split_marker):
        split_marker = fallback_marker

def split_into_chapters(text):
    parts = text.split(split_marker)
    return [part for part in parts if part.strip() != ""]

def build_chapter_stats(chapters):
    stats = []
    for index, chapter in enumerate(chapters, start=1):
        char_count = len(chapter)
        word_count = len(chapter.split())
        preview = chapter.strip().replace("\n", " ")[:80]
        stats.append({
            "index": index,
            "char_count": char_count,
            "word_count": word_count,
            "preview": preview,
        })
    return stats

def print_report(stats):
    total_chapters = len(stats)
    if total_chapters == 0:
        print("No chapters found using marker: {!r}".format(split_marker))
        return
    total_chars = sum(s["char_count"] for s in stats)
    total_words = sum(s["word_count"] for s in stats)
    print("Total chapters found: {}".format(total_chapters))
    print("Total characters: {}".format(total_chars))
    print("Total words: {}".format(total_words))
    print("Average characters per chapter: {:.1f}".format(total_chars / total_chapters))
    print("Average words per chapter: {:.1f}".format(total_words / total_chapters))
    print("")
    print("Top {} longest chapters by word count:".format(min(top_n, total_chapters)))
    ranked = sorted(stats, key=lambda s: s["word_count"], reverse=True)
    for rank, s in enumerate(ranked[:top_n], start=1):
        print("{}. Chapter {} - {} words, {} chars - \"{}...\"".format(
            rank, s["index"], s["word_count"], s["char_count"], s["preview"]))

def main():
    text = read_source_text()
    select_split_marker(text)
    print("Splitting by {!r}".format(split_marker))
    chapters = split_into_chapters(text)
    stats = build_chapter_stats(chapters)
    print_report(stats)

if __name__ == "__main__":
    main()
