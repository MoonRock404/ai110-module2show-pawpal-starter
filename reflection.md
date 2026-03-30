# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    - four core data classes: owner, pet, task, and schedule
- What classes did you include, and what responsibilities did you assign to each? 
    - owner: personal information about the owner, pet info
    - pet: basic pet info, being able to manage tasks,
    - task: info about the task, time it takes, notes, is is re-occuring?
    - schedule: what the task is, time, reason behind task, what tasks are being tracked, minutes available

**b. Design changes**

- Did your design change during implementation?
    - Yes, it did
- If yes, describe at least one change and why you made it.
    - adding a pet field to Schedule

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - time and priority
- How did you decide which constraints mattered most?
    - budget was one of the most important thing to consider because if thats full than nothing can really work


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - it prioritizes the priority constraint over the time effciency constraint
- Why is that tradeoff reasonable for this scenario?
    - the trade off is reasonable in this situation because at least the owners will be able to get their task done (even if it isnt the most efficient one)

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used AI for understanding the code, debugging, and brainstorming.
- What kinds of prompts or questions were most helpful?
    - The prompts or questions that was most helpful were the ones that were super detailed and knew exactly what was wanted.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - some of the test cases AI gave was not nessacary because other test cases covered the functionality it was trying to test
- How did you evaluate or verify what the AI suggested?
    - I always made sure to understand what changes were being done to my code and why they were needed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - see if the mark_complete feature works, adding tasks work, soring by time, checks for daily occurances, and checks same time tasks to produce a warning if something is wrong.
- Why were these tests important?
    - these things test for basic functionallity in the code to see if it works as expected.

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
