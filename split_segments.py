input_path = "input.txt"
output_path = "output.txt"
split_marker = "[chapter]"
default_max_chars = 20000
raw = input(f"Max characters ({default_max_chars}): ")
max_chars = int(raw) if raw.strip() else default_max_chars

def read_source_text():
    with open(input_path, "r", encoding="utf-8") as f:
        return f.read()

def split_into_chapters(text):
    parts = text.split(split_marker)
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    return parts

def is_bare_title(chapter):
    stripped = chapter.strip()
    if stripped == "":
        return False
    return "\n" not in stripped

def merge_bare_titles(chapters):
    merged = []
    pending_titles = []
    for chapter in chapters:
        if is_bare_title(chapter):
            pending_titles.append(chapter.strip())
            continue
        if pending_titles:
            prefix = "\n".join(pending_titles) + "\n"
            chapter = prefix + chapter.lstrip("\n")
            pending_titles = []
        merged.append(chapter)
    if pending_titles:
        merged.append("\n".join(pending_titles))
    return merged

def split_chapter_into_parts(chapter):
    if len(chapter) <= max_chars:
        return [chapter]
    lines = chapter.splitlines(keepends=True)
    total_chars = len(chapter)
    num_parts = -(-total_chars // max_chars)
    target_size = total_chars / num_parts
    parts = []
    current_lines = []
    current_size = 0
    for line in lines:
        current_lines.append(line)
        current_size += len(line)
        remaining_parts = num_parts - len(parts) - 1
        remaining_chars = total_chars - sum(len(p) for p in parts) - current_size
        if remaining_parts > 0 and current_size >= target_size and remaining_chars >= remaining_parts * 1:
            parts.append("".join(current_lines))
            current_lines = []
            current_size = 0
    if current_lines:
        parts.append("".join(current_lines))
    return parts

def build_segments(chapters):
    segments = []
    for chapter in chapters:
        segments.extend(split_chapter_into_parts(chapter))
    return segments

def write_segments(segments):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(segment.strip() for segment in segments))

def main():
    text = read_source_text()
    chapters = split_into_chapters(text)
    chapters = merge_bare_titles(chapters)
    segments = build_segments(chapters)
    write_segments(segments)
    print("Wrote {} segments to {}".format(len(segments), output_path))

if __name__ == "__main__":
    print("This splits by the [chapter] marker")
    main()
