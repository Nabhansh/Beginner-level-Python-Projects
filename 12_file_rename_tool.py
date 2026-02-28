# ============================================================
# PROJECT 12: File Rename Tool
# ============================================================

import os
import re
from datetime import datetime

def list_files(folder, extension_filter=None):
    """List all files in a folder with optional extension filter."""
    try:
        files = []
        for f in os.listdir(folder):
            full_path = os.path.join(folder, f)
            if os.path.isfile(full_path):
                if extension_filter is None or f.lower().endswith(extension_filter.lower()):
                    files.append(f)
        return sorted(files)
    except PermissionError:
        print(f"  ❌ Permission denied: {folder}")
        return []
    except FileNotFoundError:
        print(f"  ❌ Folder not found: {folder}")
        return []

def preview_rename(old_name, new_name):
    return f"  {old_name:35s} → {new_name}"

def batch_rename(folder, operation, **kwargs):
    """Perform batch rename operations."""
    files = list_files(folder, kwargs.get("ext_filter"))

    if not files:
        print("  No files found!")
        return

    renames = []

    for filename in files:
        name, ext = os.path.splitext(filename)
        new_name = filename

        if operation == "prefix":
            new_name = kwargs["prefix"] + filename

        elif operation == "suffix":
            new_name = name + kwargs["suffix"] + ext

        elif operation == "replace":
            new_name = filename.replace(kwargs["find"], kwargs["replace_with"])

        elif operation == "uppercase":
            new_name = name.upper() + ext

        elif operation == "lowercase":
            new_name = name.lower() + ext

        elif operation == "titlecase":
            new_name = name.title() + ext

        elif operation == "remove_spaces":
            char = kwargs.get("char", "_")
            new_name = name.replace(" ", char) + ext

        elif operation == "add_numbering":
            idx = files.index(filename) + 1
            start = kwargs.get("start", 1)
            num = start + idx - 1
            pad = kwargs.get("pad", 3)
            sep = kwargs.get("sep", "_")
            new_name = f"{num:0{pad}d}{sep}{name}{ext}"

        elif operation == "regex":
            try:
                new_name_base = re.sub(kwargs["pattern"], kwargs["repl"], name)
                new_name = new_name_base + ext
            except re.error as e:
                print(f"  ❌ Regex error: {e}")
                return

        elif operation == "date_prefix":
            mod_time = os.path.getmtime(os.path.join(folder, filename))
            date_str = datetime.fromtimestamp(mod_time).strftime("%Y%m%d")
            new_name = f"{date_str}_{name}{ext}"

        elif operation == "remove_numbers":
            new_name = re.sub(r'\d+', '', name).strip("_- ") + ext

        elif operation == "change_ext":
            new_name = name + "." + kwargs["new_ext"].lstrip(".")

        if new_name != filename:
            renames.append((filename, new_name))

    if not renames:
        print("  No files would be renamed.")
        return

    print(f"\n  📋 Preview ({len(renames)} files):")
    print("  " + "─" * 70)
    for old, new in renames:
        print(preview_rename(old, new))
    print("  " + "─" * 70)

    confirm = input(f"\n  Apply these {len(renames)} renames? (y/n): ").strip().lower()
    if confirm != 'y':
        print("  ❌ Operation cancelled.")
        return

    success = 0
    errors = 0
    for old, new in renames:
        try:
            old_path = os.path.join(folder, old)
            new_path = os.path.join(folder, new)
            if os.path.exists(new_path):
                print(f"  ⚠️ Skip (exists): {new}")
                continue
            os.rename(old_path, new_path)
            success += 1
        except Exception as ex:
            print(f"  ❌ Error renaming {old}: {ex}")
            errors += 1

    print(f"\n  ✅ Done! {success} renamed, {errors} errors.")

def single_rename(folder):
    files = list_files(folder)
    if not files:
        print("  No files found!")
        return

    print(f"\n  Files in {folder}:")
    for i, f in enumerate(files, 1):
        print(f"  {i:3}. {f}")

    try:
        idx = int(input("\n  Select file number: ")) - 1
        if 0 <= idx < len(files):
            old = files[idx]
            new = input(f"  New name for '{old}': ").strip()
            if new:
                old_path = os.path.join(folder, old)
                new_path = os.path.join(folder, new)
                os.rename(old_path, new_path)
                print(f"  ✅ Renamed: {old} → {new}")
        else:
            print("  Invalid selection!")
    except ValueError:
        print("  Invalid input!")

def main():
    print("=" * 55)
    print("          📂 FILE RENAME TOOL")
    print("=" * 55)

    # Get folder
    folder = input("Enter folder path (or press Enter for current dir): ").strip()
    if not folder:
        folder = os.getcwd()

    if not os.path.isdir(folder):
        print(f"❌ Folder not found: {folder}")
        return

    print(f"  📁 Working in: {folder}")
    files = list_files(folder)
    print(f"  📄 {len(files)} files found\n")

    while True:
        print("\nOperations:")
        print("  1.  Add prefix to filenames")
        print("  2.  Add suffix to filenames")
        print("  3.  Find and replace in filenames")
        print("  4.  Convert to UPPERCASE")
        print("  5.  Convert to lowercase")
        print("  6.  Convert to Title Case")
        print("  7.  Replace spaces with _")
        print("  8.  Add sequential numbering")
        print("  9.  Add date prefix from file date")
        print("  10. Remove numbers from names")
        print("  11. Change file extension")
        print("  12. Regex rename (advanced)")
        print("  13. Rename single file")
        print("  14. List files")
        print("  15. Quit")

        choice = input("\nChoose operation: ").strip()

        if choice == '1':
            prefix = input("  Enter prefix: ")
            ext_f = input("  Filter by extension (e.g. .jpg, leave blank for all): ").strip() or None
            batch_rename(folder, "prefix", prefix=prefix, ext_filter=ext_f)

        elif choice == '2':
            suffix = input("  Enter suffix: ")
            ext_f = input("  Filter by extension: ").strip() or None
            batch_rename(folder, "suffix", suffix=suffix, ext_filter=ext_f)

        elif choice == '3':
            find = input("  Find text: ")
            replace_with = input("  Replace with: ")
            batch_rename(folder, "replace", find=find, replace_with=replace_with)

        elif choice == '4':  batch_rename(folder, "uppercase")
        elif choice == '5':  batch_rename(folder, "lowercase")
        elif choice == '6':  batch_rename(folder, "titlecase")

        elif choice == '7':
            char = input("  Replace spaces with (default=_): ").strip() or "_"
            batch_rename(folder, "remove_spaces", char=char)

        elif choice == '8':
            try:
                start = int(input("  Start number (default=1): ") or "1")
                pad   = int(input("  Pad zeros (default=3): ") or "3")
                sep   = input("  Separator (default=_): ") or "_"
            except ValueError:
                start, pad, sep = 1, 3, "_"
            batch_rename(folder, "add_numbering", start=start, pad=pad, sep=sep)

        elif choice == '9':  batch_rename(folder, "date_prefix")
        elif choice == '10': batch_rename(folder, "remove_numbers")

        elif choice == '11':
            new_ext = input("  New extension (e.g. txt): ").strip()
            old_ext = input("  Only change files with extension (leave blank for all): ").strip() or None
            batch_rename(folder, "change_ext", new_ext=new_ext, ext_filter=old_ext)

        elif choice == '12':
            pattern = input("  Regex pattern: ")
            repl    = input("  Replacement: ")
            batch_rename(folder, "regex", pattern=pattern, repl=repl)

        elif choice == '13': single_rename(folder)

        elif choice == '14':
            files = list_files(folder)
            print(f"\n  Files in {folder}:")
            for i, f in enumerate(files, 1):
                size = os.path.getsize(os.path.join(folder, f))
                print(f"  {i:3}. {f:40s} ({size:,} bytes)")

        elif choice == '15':
            print("\n👋 Goodbye!")
            break
        else:
            print("  Invalid choice!")

if __name__ == "__main__":
    main()
