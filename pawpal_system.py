from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
	Column,
	Date,
	DateTime,
	Float,
	ForeignKey,
	Integer,
	String,
	Text,
	Index,
	create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from contextlib import contextmanager

Base = declarative_base()


def gen_id() -> str:
	return str(uuid.uuid4())


class Owner(Base):
	__tablename__ = "owners"

	id = Column(String, primary_key=True, default=gen_id)
	name = Column(String, nullable=False)
	email = Column(String, nullable=True)
	phone = Column(String, nullable=True)

	pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")


class Pet(Base):
	__tablename__ = "pets"

	id = Column(String, primary_key=True, default=gen_id)
	owner_id = Column(String, ForeignKey("owners.id"), nullable=False)
	name = Column(String, nullable=False)
	species = Column(String, nullable=True)
	breed = Column(String, nullable=True)
	birth_date = Column(Date, nullable=True)
	notes = Column(Text, nullable=True)

	owner = relationship("Owner", back_populates="pets")
	events = relationship("Event", back_populates="pet", cascade="all, delete-orphan")


class Event(Base):
	__tablename__ = "events"

	id = Column(String, primary_key=True, default=gen_id)
	pet_id = Column(String, ForeignKey("pets.id"), nullable=False)
	# when the event occurred (e.g. time of feeding)
	timestamp = Column(DateTime, default=datetime.utcnow, index=True)
	# audit fields for record management
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	notes = Column(Text, nullable=True)
	type = Column(String(50))
	performed_by_id = Column(String, ForeignKey("owners.id"), nullable=True)

	pet = relationship("Pet", back_populates="events")
	performed_by = relationship("Owner", foreign_keys=[performed_by_id])

	__mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "event"}


class Feeding(Event):
	__tablename__ = "feedings"

	id = Column(String, ForeignKey("events.id"), primary_key=True)
	food_type = Column(String, nullable=True)
	amount = Column(String, nullable=True)

	__mapper_args__ = {"polymorphic_identity": "feeding"}


class Walk(Event):
	__tablename__ = "walks"

	id = Column(String, ForeignKey("events.id"), primary_key=True)
	duration_minutes = Column(Integer, nullable=True)
	distance_km = Column(Float, nullable=True)

	__mapper_args__ = {"polymorphic_identity": "walk"}


class Medication(Event):
	__tablename__ = "medications"

	id = Column(String, ForeignKey("events.id"), primary_key=True)
	name = Column(String, nullable=False)
	dosage = Column(String, nullable=True)
	start_date = Column(Date, nullable=True)
	end_date = Column(Date, nullable=True)
	schedule = Column(String, nullable=True)

	__mapper_args__ = {"polymorphic_identity": "medication"}


class Database:
		def __init__(self, url: str = "sqlite:///pawpal.db"):
			"""Initialize the database connection and session maker."""
			# For sqlite use `check_same_thread=False` to avoid threading errors in apps like Streamlit
			connect_args = {"check_same_thread": False} if url.startswith("sqlite:") else {}
			self.engine = create_engine(url, echo=False, connect_args=connect_args)
			self.Session = sessionmaker(bind=self.engine)

		def create_tables(self) -> None:
			"""Create all tables in the database."""
			Base.metadata.create_all(self.engine)

		def get_session(self):
			"""Get a new database session."""
			return self.Session()

		@contextmanager
		def session_scope(self):
			"""Provide a transactional scope around a series of operations."""
			session = self.get_session()
			try:
				yield session
				session.commit()
			except Exception:
				session.rollback()
				raise
			finally:
				session.close()


# --- Helper CRUD functions (minimal skeleton) ---
def add_owner(session, name: str, email: Optional[str] = None, phone: Optional[str] = None) -> Owner:
	"""Add a new owner to the database."""
	owner = Owner(name=name, email=email, phone=phone)
	session.add(owner)
	session.commit()
	session.refresh(owner)
	return owner


def add_pet(
	session,
	owner_id: str,
	name: str,
	species: Optional[str] = None,
	breed: Optional[str] = None,
	birth_date: Optional[date] = None,
	notes: Optional[str] = None,
) -> Pet:
	"""Add a new pet to the database."""
	pet = Pet(owner_id=owner_id, name=name, species=species, breed=breed, birth_date=birth_date, notes=notes)
	session.add(pet)
	session.commit()
	session.refresh(pet)
	return pet


def add_feeding(session, pet_id: str, timestamp: Optional[datetime] = None, food_type: Optional[str] = None, amount: Optional[str] = None, notes: Optional[str] = None) -> Feeding:
	"""Add a feeding event for a pet."""
	evt = Feeding(pet_id=pet_id, timestamp=timestamp or datetime.utcnow(), food_type=food_type, amount=amount, notes=notes)
	session.add(evt)
	session.commit()
	session.refresh(evt)
	return evt


def add_walk(session, pet_id: str, timestamp: Optional[datetime] = None, duration_minutes: Optional[int] = None, distance_km: Optional[float] = None, notes: Optional[str] = None) -> Walk:
	"""Add a walk event for a pet."""
	evt = Walk(pet_id=pet_id, timestamp=timestamp or datetime.utcnow(), duration_minutes=duration_minutes, distance_km=distance_km, notes=notes)
	session.add(evt)
	session.commit()
	session.refresh(evt)
	return evt


def add_medication(
	session,
	pet_id: str,
	name: str,
	dosage: Optional[str] = None,
	start_date: Optional[date] = None,
	end_date: Optional[date] = None,
	schedule: Optional[str] = None,
	timestamp: Optional[datetime] = None,
	notes: Optional[str] = None,
) -> Medication:
		"""Add a medication event for a pet."""
		evt = Medication(
			pet_id=pet_id,
			timestamp=timestamp or datetime.utcnow(),
			name=name,
			dosage=dosage,
			start_date=start_date,
			end_date=end_date,
			schedule=schedule,
			notes=notes,
		)
		session.add(evt)
		session.commit()
		session.refresh(evt)
		return evt


def list_pets_for_owner(session, owner_id: str) -> List[Pet]:
	"""List all pets for a given owner."""
	return session.query(Pet).filter_by(owner_id=owner_id).all()


def list_events_for_pet(session, pet_id: str) -> List[Event]:
	"""List all events for a given pet, ordered by timestamp descending."""
	return session.query(Event).filter_by(pet_id=pet_id).order_by(Event.timestamp.desc()).all()


# --- Pure Python agent-mode classes below ---
# --- Prescription / scheduling helpers ---


# --- Pure Python agent-mode classes (no SQLAlchemy) ---

# (Moved to end of file to avoid name conflicts)
class MedicationPrescription(Base):
	__tablename__ = "medication_prescriptions"

	id = Column(String, primary_key=True, default=gen_id)
	pet_id = Column(String, ForeignKey("pets.id"), nullable=False)
	name = Column(String, nullable=False)
	dosage = Column(String, nullable=True)
	start_date = Column(Date, nullable=True)
	end_date = Column(Date, nullable=True)
	schedule = Column(String, nullable=True)
	prescriber = Column(String, nullable=True)
	notes = Column(Text, nullable=True)

	pet = relationship("Pet")


class ScheduledDose(Base):
	__tablename__ = "scheduled_doses"

	id = Column(String, primary_key=True, default=gen_id)
	prescription_id = Column(String, ForeignKey("medication_prescriptions.id"), nullable=False)
	scheduled_at = Column(DateTime, nullable=False)
	status = Column(String, nullable=False, default="scheduled")

	prescription = relationship("MedicationPrescription")


def add_prescription(session, pet_id: str, name: str, dosage: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None, schedule: Optional[str] = None, prescriber: Optional[str] = None, notes: Optional[str] = None) -> MedicationPrescription:
	"""Add a medication prescription for a pet."""
	p = MedicationPrescription(pet_id=pet_id, name=name, dosage=dosage, start_date=start_date, end_date=end_date, schedule=schedule, prescriber=prescriber, notes=notes)
	session.add(p)
	session.commit()
	session.refresh(p)
	return p


def schedule_dose(session, prescription_id: str, scheduled_at: datetime) -> ScheduledDose:
	"""Schedule a dose for a prescription."""
	sd = ScheduledDose(prescription_id=prescription_id, scheduled_at=scheduled_at, status="scheduled")
	session.add(sd)
	session.commit()
	session.refresh(sd)
	return sd


# Indexes to improve common queries
Index("ix_pets_owner_id", Pet.owner_id)
Index("ix_events_pet_id", Event.pet_id)
Index("ix_events_timestamp", Event.timestamp)


__all__ = [
   "Database",
   "Owner",
   "Pet",
   "Event",
   "Feeding",
   "Walk",
   "Medication",
   "add_owner",
   "add_pet",
   "add_feeding",
   "add_walk",
   "add_medication",
   "list_pets_for_owner",
   "list_events_for_pet",
]

# --- Pure Python agent-mode classes (no SQLAlchemy) ---
class Task:
	def __init__(self, description: str, time: datetime, frequency: str = "once", completed: bool = False):
		"""Initialize a new task."""
		self.description = description
		self.time = time
		self.frequency = frequency
		self.completed = completed

	def mark_complete(self):
		"""Mark this task as complete."""
		self.completed = True

	def __repr__(self):
		"""Return a string representation of the task."""
		return f"<Task desc={self.description!r} time={self.time} freq={self.frequency} completed={self.completed}>"


class Pet:
	def __init__(self, name, species=None, breed=None, birth_date=None, notes=None, tasks=None):
		"""Initialize a new pet."""
		self.name = name
		self.species = species
		self.breed = breed
		self.birth_date = birth_date
		self.notes = notes
		self.tasks = tasks if tasks is not None else []

	def add_task(self, task: Task):
		"""Add a task to this pet."""
		self.tasks.append(task)

	def get_tasks(self):
		"""Get all tasks for this pet."""
		return self.tasks

	def __repr__(self):
		"""Return a string representation of the pet."""
		return f"<Pet name={self.name!r} species={self.species} tasks={len(self.tasks)} >"


class Owner:
	def __init__(self, name, email=None, phone=None, pets=None):
		"""Initialize a new owner."""
		self.name = name
		self.email = email
		self.phone = phone
		self.pets = pets if pets is not None else []

	def add_pet(self, pet: Pet):
		"""Add a pet to this owner."""
		self.pets.append(pet)

	def get_all_tasks(self):
		"""Get all tasks for all pets owned by this owner."""
		all_tasks = []
		for pet in self.pets:
			all_tasks.extend(getattr(pet, 'tasks', []))
		return all_tasks

	def __repr__(self):
		"""Return a string representation of the owner."""
		return f"<Owner name={self.name!r} pets={len(self.pets)} >"


class Scheduler:
	@staticmethod
	def warn_on_conflicts(tasks: list):
		"""
		Lightweight conflict detection: returns a warning message if any two tasks are scheduled at the same time.
		Does not raise errors or crash the program.
		Returns None if no conflicts, or a warning string if conflicts exist.
		"""
		conflicts = Scheduler.detect_conflicts(tasks)
		if conflicts:
			return f"Warning: {len(conflicts)} scheduling conflict(s) detected. Some tasks overlap in time."
		return None

	@staticmethod
	def detect_conflicts(tasks: list):
		"""
		Efficiently detect if any two tasks (for the same or different pets) are scheduled at the same time.
		Groups tasks by their scheduled time, then checks for conflicts only within each group.
		Returns a list of tuples: (task1, task2) for each conflict found.
		"""
		from collections import defaultdict
		# Group tasks by their scheduled time
		time_map = defaultdict(list)
		for task in tasks:
			time_map[task.time].append(task)

		conflicts = []
		# For each group of tasks at the same time, add all unique pairs as conflicts
		for task_list in time_map.values():
			if len(task_list) > 1:
				# Compare each pair only once
				for i in range(len(task_list)):
					for j in range(i + 1, len(task_list)):
						# Add the conflicting pair
						conflicts.append((task_list[i], task_list[j]))
		return conflicts

	@staticmethod
	def filter_tasks(tasks: list, completed: bool = None, pet_name: str = None):
		"""
		Filter tasks by completion status and/or pet name.
		:param tasks: List of Task objects (optionally with pet attribute or from a single pet)
		:param completed: True for completed, False for incomplete, None for all
		:param pet_name: Filter by pet name if provided
		:return: Filtered list of tasks
		"""
		filtered = tasks
		if completed is not None:
			filtered = [t for t in filtered if getattr(t, 'completed', False) == completed]
		if pet_name is not None:
			filtered = [t for t in filtered if hasattr(t, 'pet') and getattr(t.pet, 'name', None) == pet_name]
		return filtered

	@staticmethod
	def get_all_tasks_for_owner(owner: Owner):
		"""Get all tasks for a given owner."""
		return owner.get_all_tasks()

	@staticmethod
	def get_tasks_for_pet(pet: Pet):
		"""Get all tasks for a given pet."""
		return pet.get_tasks()

	@staticmethod
	def organize_tasks_by_time(tasks: list):
		"""Organize tasks by their scheduled time."""
		return sorted(tasks, key=lambda t: t.time)

	@staticmethod
	def mark_task_complete(task: Task, pet: 'Pet' = None):
		"""
		Mark a given task as complete. If the task is 'daily' or 'weekly', create the next occurrence automatically.
		:param task: The Task to mark complete
		:param pet: The Pet to which the task belongs (required for recurring tasks)
		"""
		task.mark_complete()
		from datetime import timedelta
		next_time = None
		if task.frequency == "daily":
			next_time = task.time + timedelta(days=1)
		elif task.frequency == "weekly":
			next_time = task.time + timedelta(weeks=1)
		if next_time and pet is not None:
			new_task = Task(
				description=task.description,
				time=next_time,
				frequency=task.frequency,
				completed=False
			)
			pet.add_task(new_task)

