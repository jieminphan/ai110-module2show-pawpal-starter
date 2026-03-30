from datetime import datetime, timedelta
from pawpal_system import OwnerPlan as Owner, PetPlan as Pet, Task, Scheduler

# Create an owner
owner = Owner(name="Alex Kim", email="alex@example.com", phone="555-1234")

# Create two pets
pet1 = Pet(name="Buddy", species="Dog", breed="Labrador", birth_date=datetime(2020, 5, 1))
pet2 = Pet(name="Mittens", species="Cat", breed="Siamese", birth_date=datetime(2021, 8, 15))

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create tasks for pets (with different times)
now = datetime.now()
task1 = Task(description="Morning Walk", time=now.replace(hour=8, minute=0), frequency="daily")
task2 = Task(description="Feed Breakfast", time=now.replace(hour=7, minute=30), frequency="daily")
task3 = Task(description="Vet Appointment", time=now.replace(hour=15, minute=0), frequency="once")

# Assign tasks to pets
pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)

# Gather all tasks for today
all_tasks = Scheduler.get_all_tasks_for_owner(owner)
today = now.date()
todays_tasks = [t for t in all_tasks if t.time.date() == today]

# Organize tasks by time
sorted_tasks = Scheduler.organize_tasks_by_time(todays_tasks)

# Print today's schedule
print("Today's Schedule:")
for task in sorted_tasks:
    print(f"- {task.time.strftime('%H:%M')}: {task.description} (Pet: {'Buddy' if task in pet1.tasks else 'Mittens'})")
