# ============================================================
# PROJECT 10: Task Planner
# ============================================================

import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(tasks):
    print("\n--- ADD NEW TASK ---")
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty!")
        return

    description = input("Description (optional): ").strip()

    print("Priority: 1=High 🔴  2=Medium 🟡  3=Low 🟢")
    priority_map = {"1": "High", "2": "Medium", "3": "Low"}
    priority = priority_map.get(input("Choose (1/2/3, default=2): ").strip(), "Medium")

    due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format, skipping due date.")
            due_date = ""

    category = input("Category (e.g. Work, Personal, Study): ").strip() or "General"

    task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "category": category,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task '{title}' added successfully!")

def view_tasks(tasks, filter_type="all"):
    PRIORITY_ICON = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

    if filter_type == "pending":
        filtered = [t for t in tasks if not t["completed"]]
        title = "PENDING TASKS"
    elif filter_type == "done":
        filtered = [t for t in tasks if t["completed"]]
        title = "COMPLETED TASKS"
    else:
        filtered = tasks
        title = "ALL TASKS"

    if not filtered:
        print(f"\nNo tasks found.")
        return

    # Sort by priority
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    filtered.sort(key=lambda x: (x["completed"], priority_order.get(x["priority"], 2)))

    print(f"\n{'='*60}")
    print(f"  📋 {title} ({len(filtered)} tasks)")
    print(f"{'='*60}")

    categories = {}
    for task in filtered:
        cat = task["category"]
        categories.setdefault(cat, []).append(task)

    for cat, cat_tasks in categories.items():
        print(f"\n  📁 {cat.upper()}")
        print(f"  {'─'*50}")
        for task in cat_tasks:
            status = "✅" if task["completed"] else "⬜"
            prio   = PRIORITY_ICON.get(task["priority"], "🟡")
            due    = f"  📅 {task['due_date']}" if task["due_date"] else ""
            print(f"  {status} [{task['id']:3}] {prio} {task['title']}{due}")
            if task["description"]:
                print(f"       └─ {task['description']}")

def complete_task(tasks):
    view_tasks(tasks, "pending")
    try:
        task_id = int(input("\nEnter task ID to mark complete: "))
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task:
            task["completed"] = True
            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_tasks(tasks)
            print(f"✅ Task '{task['title']}' marked as complete!")
        else:
            print("Task not found!")
    except ValueError:
        print("Invalid ID!")

def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_id = int(input("\nEnter task ID to delete: "))
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task:
            confirm = input(f"Delete '{task['title']}'? (y/n): ").lower()
            if confirm == 'y':
                tasks.remove(task)
                save_tasks(tasks)
                print("🗑️ Task deleted!")
        else:
            print("Task not found!")
    except ValueError:
        print("Invalid ID!")

def search_tasks(tasks):
    keyword = input("Search keyword: ").strip().lower()
    results = [t for t in tasks if keyword in t["title"].lower()
                or keyword in t["description"].lower()
                or keyword in t["category"].lower()]
    if results:
        print(f"\nFound {len(results)} task(s):")
        view_tasks(results)
    else:
        print("No tasks match your search.")

def show_stats(tasks):
    total    = len(tasks)
    done     = sum(1 for t in tasks if t["completed"])
    pending  = total - done
    high     = sum(1 for t in tasks if not t["completed"] and t["priority"] == "High")

    print(f"\n{'='*40}")
    print("  📊 TASK STATISTICS")
    print(f"{'='*40}")
    print(f"  Total tasks:     {total}")
    print(f"  Completed:       {done} ✅")
    print(f"  Pending:         {pending} ⬜")
    print(f"  High priority:   {high} 🔴")
    if total > 0:
        print(f"  Completion rate: {done/total*100:.1f}%")

def main():
    tasks = load_tasks()
    print("=" * 50)
    print("         📝 TASK PLANNER")
    print("=" * 50)

    while True:
        pending_count = sum(1 for t in tasks if not t["completed"])
        print(f"\n  [{pending_count} pending tasks]")
        print("  1. ➕ Add task")
        print("  2. 📋 View all tasks")
        print("  3. ⬜ View pending tasks")
        print("  4. ✅ View completed tasks")
        print("  5. ✔️  Complete a task")
        print("  6. 🗑️  Delete a task")
        print("  7. 🔍 Search tasks")
        print("  8. 📊 Statistics")
        print("  9. 🚪 Quit")

        choice = input("\nChoose: ").strip()
        if choice == '1':   add_task(tasks)
        elif choice == '2': view_tasks(tasks)
        elif choice == '3': view_tasks(tasks, "pending")
        elif choice == '4': view_tasks(tasks, "done")
        elif choice == '5': complete_task(tasks)
        elif choice == '6': delete_task(tasks)
        elif choice == '7': search_tasks(tasks)
        elif choice == '8': show_stats(tasks)
        elif choice == '9':
            print("\nBye! Stay productive! 💪")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
