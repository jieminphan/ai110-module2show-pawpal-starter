# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
My UML design includes classes "Pet", "Event", "Feeding", "Walk", and "Medication".

Pet:
- String name
- String species
- String breed
- Date brithDate
- String notes

Event:
- Int id
- DateTime timestamp
- String notes
- addFeeding()
- addWalk()
- addMedication()

Feeding:
- String foodName
- String amount

Walk:
- int durationWalked
- float distance

Medication:
- String name
- String dosage

**b. Design changes**

Yes. I added "Scheduled doses" under "Medication" as it is important for medication to be taken on time for the pets, whether it is chronic or minor.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

Some constraints that my scheduler consider are medication, time windows, recurring schedules, task duration, and other preferences. I decided what mattered more based on safety, feasibility and user impact. For example, medication is at the top of the list as it may cause a life or death situation if a dose was missed, or even just by being late. When feasible, the pet owners may choose their own schedules (like walking times etc) but medication will always take priority.

**b. Tradeoffs**

One tradeoff that the scheduler makes is the schedule for medication will always overwrite other schedules, unless it is important for the medications (eg food must be eaten before taken medication). This tradeoff is reasonable as it concerns the health of the pet, by prioritizing medications, it prevents high-risk incidents from taking place even if it might inconvenience the owner.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
