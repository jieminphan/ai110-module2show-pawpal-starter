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

Using python -m pytest, I ran a series of tests that cover:
Sorting:
Sorting with empty task lists.
Sorting tasks with identical timestamps or priorities.
Sorting tasks with missing or null fields.
Sorting tasks with mixed types (e.g., some recurring, some one-time).

Recurring Tasks:
Recurring tasks that overlap with one-time tasks.
Recurring tasks that fall on leap days or daylight saving time changes.
Recurring tasks with invalid or zero intervals.
Recurring tasks that should end after a certain date or number of occurrences.

General Scheduler:
Scheduling tasks in the past or far future.
Tasks with conflicting times (overlaps).
Tasks with missing required fields (e.g., no pet assigned).
Handling of duplicate tasks.
Deleting or editing recurring tasks (does it affect all or just one occurrence?).

Testing these edge cases ensures real-world scenarios can be handled and prevents subtle bugs in scheduling logic. 

**b. Confidence**

My confidence level would be around 3. There are some features that I haven't had 100% working and am still in the process of testing.

---

## 5. Reflection

**a. What went well**

- I'm most satisfied with the fact that I managed this built this project using AI as a friend rather than as something to only write my code for me.

**b. What you would improve**

- I would maybe create accessibility features for users and language options.

**c. Key takeaway**

- Although AI is extremely helpful, they may not be right 100% of the time, thus fact-checking is very important.
