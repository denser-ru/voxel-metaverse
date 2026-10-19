#!/usr/bin/env python3
"""
Voxel Metaverse Project - AI Context Packer (2026)
Zero-dependency утилита для сборки высокоплотного контекста проекта
в единый XML-документ для анализа в Google AI Studio, Gemini и Claude.

Запуск:
    python tools/pack_context.py
    python tools/pack_context.py --output custom_context.xml
    python tools/pack_context.py --specs-only
"""

import argparse
import datetime
import os
import sys
from pathlib import Path


# Директории и паттерны, которые КАТЕГОРИЧЕСКИ запрещено включать в контекст
DEFAULT_IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "wasm_build",  # Тяжелые скомпилированные бинарники Wasm
    "dist",
    "build",
    "temp",
}

DEFAULT_IGNORE_EXTENSIONS = {
    ".wasm",
    ".data",
    ".sqlite",
    ".sqlite3",
    ".pyc",
    ".pyo",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".tar",
    ".gz",
    ".zip",
    ".log",
    ".mts",
    ".mts.bak",
}

# Расширения файлов, которые мы считаем текстовыми и полезными
ALLOWED_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".lua",
    ".json",
    ".yml",
    ".yaml",
    ".html",
    ".css",
    ".js",
    ".conf",
    ".gitignore",
}

MAX_FILE_SIZE_KB = 100  # Защита от случайного дампа гигантских файлов


def find_repo_root() -> Path:
    """Находит корень репозитория по наличию папки .git или README.md."""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists() or (parent / "README.md").exists():
            return parent
    return current.parent


def generate_tree(root_dir: Path, ignore_dirs: set[str]) -> str:
    """Генерирует компактное текстовое дерево файлов проекта."""
    lines = []

    def walk(directory: Path, prefix: str = ""):
        entries = sorted(
            [e for e in directory.iterdir() if e.name not in ignore_dirs],
            key=lambda x: (x.is_file(), x.name.lower()),
        )
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                sub_prefix = "    " if is_last else "│   "
                walk(entry, prefix + sub_prefix)

    lines.append(root_dir.name + "/")
    walk(root_dir)
    return "\n".join(lines)


def should_include_file(file_path: Path, specs_only: bool) -> bool:
    """Определяет, должен ли файл попасть в итоговую выжимку."""
    # Проверка на расширение
    if file_path.suffix.lower() in DEFAULT_IGNORE_EXTENSIONS:
        return False
    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS and file_path.name != "LICENSE":
        return False

    # Проверка на размер
    if file_path.stat().st_size > MAX_FILE_SIZE_KB * 1024:
        return False

    # Если включен режим specs-only, берем только Markdown, JSON и конфиги
    if specs_only:
        if file_path.suffix.lower() not in {".md", ".json", ".txt", ".yml", ".yaml"}:
            return False

    return True


def collect_files(root_dir: Path, specs_only: bool) -> list[Path]:
    """Рекурсивно собирает список целевых файлов с приоритизацией спецификаций."""
    collected = []

    for root, dirs, files in os.walk(root_dir):
        # Модифицируем dirs in-place, чтобы os.walk не заходил в игнорируемые папки
        dirs[:] = [d for d in dirs if d not in DEFAULT_IGNORE_DIRS]

        for file in files:
            p = Path(root) / file
            if should_include_file(p, specs_only):
                collected.append(p)

    # Приоритет сортировки: README и контракты первыми, затем спеки, затем код
    def priority_sort(path: Path) -> tuple[int, str]:
        rel = path.relative_to(root_dir).as_posix()
        if rel == "README.md":
            return (0, rel)
        if "workspace_0_shared_contracts" in rel:
            return (1, rel)
        if "PROJECT.md" in rel or "AGENTS.md" in rel or "llms.txt" in rel:
            return (2, rel)
        if "specs/" in rel:
            return (3, rel)
        return (4, rel)

    return sorted(collected, key=priority_sort)


def main():
    parser = argparse.ArgumentParser(
        description="Pack Voxel Metaverse project context into an AI-ready XML digest."
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="ai_context_pack.xml",
        help="Target output file path (default: ai_context_pack.xml in repo root)",
    )
    parser.add_argument(
        "--specs-only",
        action="store_true",
        help="Pack only architectural specs, configs, and passports (exclude source code)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the packed result directly to stdout instead of saving to a file",
    )
    args = parser.parse_args()

    root_dir = find_repo_root()
    output_path = (root_dir / args.output).resolve()

    print(f"🔍 Сканирование репозитория: {root_dir}")
    files_to_pack = collect_files(root_dir, args.specs_only)

    print(f"📦 Отобрано файлов для упаковки: {len(files_to_pack)}")
    file_tree = generate_tree(root_dir, DEFAULT_IGNORE_DIRS)

    out_lines = []
    out_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    out_lines.append(
        f'<project_context name="voxel_metaverse_project" generated_at="{datetime.datetime.now(datetime.timezone.utc).isoformat()}">'
    )

    out_lines.append("  <system_instructions>")
    out_lines.append(
        "    Этот XML-документ содержит высокоплотный контекст образовательной 3D-песочницы Voxel Metaverse.\n"
        "    Проект спроектирован по стандартам Spec-Driven Development (SDD) для автономной разработки мультиагентной системой Antigravity 2.0.\n"
        "    Используй эти спецификации для анализа текущего состояния, верификации инвариантов и проектирования дальнейших шагов."
    )
    out_lines.append("  </system_instructions>")

    out_lines.append("  <repository_structure>")
    out_lines.append("<![CDATA[")
    out_lines.append(file_tree)
    out_lines.append("]]>")
    out_lines.append("  </repository_structure>")

    out_lines.append("  <files>")
    total_bytes = 0

    for file_path in files_to_pack:
        rel_path = file_path.relative_to(root_dir).as_posix()
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            total_bytes += len(content.encode("utf-8"))
            out_lines.append(f'    <file path="{rel_path}">')
            out_lines.append("<![CDATA[")
            out_lines.append(content)
            out_lines.append("]]>")
            out_lines.append("    </file>")
        except Exception as e:
            print(f"⚠️ Ошибка чтения {rel_path}: {e}", file=sys.stderr)

    out_lines.append("  </files>")
    out_lines.append("</project_context>")

    full_output = "\n".join(out_lines)

    # Приблизительный подсчет токенов (~3.8 символа на токен для смешанного кода/текста)
    estimated_tokens = len(full_output) // 4

    if args.stdout:
        sys.stdout.write(full_output)
    else:
        output_path.write_text(full_output, encoding="utf-8")
        print("\n" + "=" * 50)
        print("🎉 УСПЕШНО УПАКОВАНО!")
        print(f"📁 Файл выгрузки:    {output_path}")
        print(f"📊 Размер на диске:  {total_bytes / 1024:.1f} KB")
        print(f"🧠 Оценка токенов:   ~{estimated_tokens:,} токенов")
        print("=" * 50)
        print("💡 Что делать дальше:")
        print("   1. Откройте Google AI Studio (или чат с Claude).")
        print(f"   2. Прикрепите файл {output_path.name} (или вставьте его содержимое).")
        print("   3. Задавайте вопросы по архитектуре, анализу кода или планам на Stage 2!")


if __name__ == "__main__":
    main()