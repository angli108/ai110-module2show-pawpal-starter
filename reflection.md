# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
 
Three core tasks: 
1. add a pet
2. add/delete a task
3. see today's task 

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The Owner class stores the owner's name, a list of pets, and a reference to a Scheduler, with methods to add, remove, and edit pets.
The Pet class stores basic information about each pet: name, gender, and age.
The Task class acts as a data container holding a task's associated pet, activity, available time, priority, and owner preferences.
The Scheduler class manages all tasks through a task list, with methods to add, remove, and edit them.
                 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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




Notes:

(original)
Owner
    Attributes: 
        - name
        - constraints list 
        - pets list 
    Methods:
        - add constraints
        - remove constraints
        - edit constraints


Pet
    Attributes: 
        - name
        - gender
        - age
    Methods:
        - add pets
        - remove pets
        - edit pets
    
*can pet add itself, who adds a pet? 


Task (just a thing)
    Attributes: 
        - task list 
    Methods;
        - add tasks
        - remove tasks 
        - edit tasks 

*added task list but Task is the single thing, not list 

Scheduler (manages that thing) 
        Attributes: 
        - name





(Updated)
Owner
    Attributes: 
        - name
        - scheduler 
        - pets list 
    Methods:
        - add, remove, edit pets 

Pet
    Attributes: 
        - name
        - gender
        - age

Task (just a thing)
    Attributes: 
        - pet 
        - task activty 
        - time availble 
        - priority 
        - owner preference 

Scheduler (manages that thing) 
    Attributes: 
        - task list  
    Methods:
        - add, remove, edit task  


the owner manages the pets and scheduler 
the pet doesnt manage anything
the task holds constraints and knows the pet the task is associated with  
the scheudle manages the tasks  


(Point: constraints are fixed attributes and not objects
     No need for list of contriants. no need for schedule to add constraints, made when add task )


Mermaid.js

                                                                                            
  classDiagram                                                                            
      class Owner {
          +String name
          +addPet(pet: Pet)
          +removePet(pet: Pet)
          +editPet(pet: Pet)
      }

      class Pet {
          +String name
          +String gender
          +int age
      }

      class Task {
          +String taskActivity
          +String timeAvailable                                                             
          +int priority
          +String ownerPreference                                                           
      }           

      class Scheduler {
          +addTask(task: Task)
          +removeTask(task: Task)
          +editTask(task: Task)
      }                                                                    