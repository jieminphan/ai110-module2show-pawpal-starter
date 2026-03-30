
import pytest
from datetime import datetime, timedelta, date
from pawpal_system import Database, add_owner, add_pet, add_feeding, add_walk, Pet, Feeding, Walk

def test_add_feeding_and_check_fields():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        pet = add_pet(session, owner_id=owner.id, name="Buddy", species="dog")
        feeding = add_feeding(session, pet_id=pet.id, timestamp=datetime(2026, 3, 30, 8, 0), food_type="kibble", amount="1 cup")
        assert feeding.pet_id == pet.id
        assert feeding.food_type == "kibble"
        assert feeding.amount == "1 cup"

def test_add_walk_and_query():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        pet = add_pet(session, owner_id=owner.id, name="Buddy", species="dog")
        walk = add_walk(session, pet_id=pet.id, timestamp=datetime(2026, 3, 30, 9, 0), duration_minutes=30, distance_km=2.0)
        assert walk.pet_id == pet.id
        assert walk.duration_minutes == 30
        assert walk.distance_km == 2.0

def test_query_events_sorted_by_time():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        pet = add_pet(session, owner_id=owner.id, name="Buddy", species="dog")
        add_feeding(session, pet_id=pet.id, timestamp=datetime(2026, 3, 30, 19, 0))
        add_feeding(session, pet_id=pet.id, timestamp=datetime(2026, 3, 30, 7, 0))
        add_feeding(session, pet_id=pet.id, timestamp=datetime(2026, 3, 30, 12, 0))
        events = session.query(Feeding).filter_by(pet_id=pet.id).order_by(Feeding.timestamp).all()
        times = [evt.timestamp for evt in events]
        assert times == sorted(times)

def test_add_duplicate_feeding():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        pet = add_pet(session, owner_id=owner.id, name="Buddy", species="dog")
        f1 = add_feeding(session, pet_id=pet.id, timestamp=datetime(2026, 3, 30, 8, 0))
        f2 = add_feeding(session, pet_id=pet.id, timestamp=datetime(2026, 3, 30, 8, 0))
        feedings = session.query(Feeding).filter_by(pet_id=pet.id).all()
        assert len(feedings) == 2

def test_add_feeding_with_missing_time():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        pet = add_pet(session, owner_id=owner.id, name="Buddy", species="dog")
        feeding = add_feeding(session, pet_id=pet.id)
        assert feeding.timestamp is not None

def test_multiple_feedings_for_recurring():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        pet = add_pet(session, owner_id=owner.id, name="Buddy", species="dog")
        times = [datetime(2026, 3, 30, 8, 0) + timedelta(days=i) for i in range(3)]
        for t in times:
            add_feeding(session, pet_id=pet.id, timestamp=t)
        feedings = session.query(Feeding).filter_by(pet_id=pet.id).order_by(Feeding.timestamp).all()
        assert len(feedings) == 3
        for i, f in enumerate(feedings):
            assert f.timestamp == times[i]

def test_query_empty_feedings():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        pet = add_pet(session, owner_id=owner.id, name="Buddy", species="dog")
        feedings = session.query(Feeding).filter_by(pet_id=pet.id).all()
        assert feedings == []

def test_feeding_in_past():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        pet = add_pet(session, owner_id=owner.id, name="Buddy", species="dog")
        past_time = datetime.now() - timedelta(days=1)
        feeding = add_feeding(session, pet_id=pet.id, timestamp=past_time)
        assert feeding.timestamp < datetime.now()

def test_add_pet_with_null_name():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        with pytest.raises(Exception):
            add_pet(session, owner_id=owner.id, name=None)

def test_update_feeding_notes():
    db = Database("sqlite:///test.db")
    db.create_tables()
    with db.session_scope() as session:
        owner = add_owner(session, name="Alice")
        pet = add_pet(session, owner_id=owner.id, name="Buddy", species="dog")
        feeding = add_feeding(session, pet_id=pet.id, timestamp=datetime(2026, 3, 30, 8, 0), notes="first note")
        feeding.notes = "updated note"
        session.commit()
        updated = session.query(Feeding).filter_by(id=feeding.id).first()
        assert updated.notes == "updated note"