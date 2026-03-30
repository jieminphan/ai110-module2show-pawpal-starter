from datetime import datetime
from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(description="Feed Buddy", time=datetime(2026, 3, 30, 8, 0))
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="dog")
    assert len(pet.tasks) == 0
    task = Task(description="Walk Buddy", time=datetime(2026, 3, 30, 9, 0))
    pet.add_task(task)
    assert len(pet.tasks) == 1
