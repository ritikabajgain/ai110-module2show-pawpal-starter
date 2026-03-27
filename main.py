from pawpal_system import Owner, Pet, Task, Scheduler

# ============================================================
# SETUP — owner with two pets
# ============================================================
owner = Owner("Jordan", time_available=120)

mochi = Pet("Mochi", species="dog", age=3)
luna = Pet("Luna", species="cat", age=5)
owner.add_pet(mochi)
owner.add_pet(luna)

# ============================================================
# 1) CLEAN SCHEDULE — no conflicts
# ============================================================
print("=" * 55)
print("1) CLEAN SCHEDULE — tasks spread across time slots")
print("=" * 55)

mochi.add_task(Task("Morning walk", duration_minutes=30, priority="high",
                    category="walk", preferred_time="morning"))
luna.add_task(Task("Feed Luna", duration_minutes=10, priority="high",
                   category="feeding", preferred_time="morning"))
mochi.add_task(Task("Brush fur", duration_minutes=15, priority="low",
                    category="grooming", preferred_time="evening"))

scheduler = Scheduler(owner)
scheduler.generate_plan()
print(scheduler.explain_plan())

# ============================================================
# 2) SAME-PET CONFLICT — two big tasks for Mochi in the evening
# ============================================================
print("\n" + "=" * 55)
print("2) SAME-PET CONFLICT — Mochi gets two evening tasks")
print("=" * 55)

# These two evening tasks (45 + 30 = 75 min) exceed the 60 min evening budget
mochi.add_task(Task("Evening walk", duration_minutes=45, priority="high",
                    category="walk", preferred_time="evening"))
mochi.add_task(Task("Bath time", duration_minutes=30, priority="high",
                    category="grooming", preferred_time="evening"))

scheduler.generate_plan()
print(scheduler.explain_plan())

# ============================================================
# 3) CROSS-PET CONFLICT — Luna also needs evening care
# ============================================================
print("\n" + "=" * 55)
print("3) CROSS-PET CONFLICT — Luna added to the same evening slot")
print("=" * 55)

# Luna's evening task pushes the slot even further over budget
luna.add_task(Task("Play with feather toy", duration_minutes=20, priority="high",
                   category="enrichment", preferred_time="evening"))

scheduler.generate_plan()
print(scheduler.explain_plan())

# ============================================================
# 4) DIRECT detect_conflicts() CALL — inspect raw warnings
# ============================================================
print("\n" + "=" * 55)
print("4) RAW WARNINGS — detect_conflicts() returns a list")
print("=" * 55)

warnings = scheduler.detect_conflicts()
if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts found.")

print(f"\n  Total warnings: {len(warnings)}")
print("  (Program continues normally — warnings, not crashes.)")
