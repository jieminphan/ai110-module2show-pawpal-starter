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
	create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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
	timestamp = Column(DateTime, default=datetime.utcnow)
	notes = Column(Text, nullable=True)
	type = Column(String(50))

	pet = relationship("Pet", back_populates="events")

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
		self.engine = create_engine(url, echo=False)
		self.Session = sessionmaker(bind=self.engine)

	def create_tables(self) -> None:
		Base.metadata.create_all(self.engine)

	def get_session(self):
		return self.Session()


# --- Helper CRUD functions (minimal skeleton) ---
def add_owner(session, name: str, email: Optional[str] = None, phone: Optional[str] = None) -> Owner:
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
	pet = Pet(owner_id=owner_id, name=name, species=species, breed=breed, birth_date=birth_date, notes=notes)
	session.add(pet)
	session.commit()
	session.refresh(pet)
	return pet


def add_feeding(session, pet_id: str, timestamp: Optional[datetime] = None, food_type: Optional[str] = None, amount: Optional[str] = None, notes: Optional[str] = None) -> Feeding:
	evt = Feeding(pet_id=pet_id, timestamp=timestamp or datetime.utcnow(), food_type=food_type, amount=amount, notes=notes)
	session.add(evt)
	session.commit()
	session.refresh(evt)
	return evt


def add_walk(session, pet_id: str, timestamp: Optional[datetime] = None, duration_minutes: Optional[int] = None, distance_km: Optional[float] = None, notes: Optional[str] = None) -> Walk:
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
	return session.query(Pet).filter_by(owner_id=owner_id).all()


def list_events_for_pet(session, pet_id: str) -> List[Event]:
	return session.query(Event).filter_by(pet_id=pet_id).order_by(Event.timestamp.desc()).all()


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

