# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
 
Three core tasks: 
1. add a pet
2. add task to take pet to vet
3. see today's task 

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The Owner class stores the owner's name, a list of pets, and a reference to a Scheduler, with methods to add, remove, and edit pets.
The Pet class stores basic information about each pet: name, gender, and age.
The Task class acts as a data container holding a task's associated pet, activity, available time, priority, and owner preferences.
The Scheduler class manages all tasks through a task list, with methods to add, remove, and edit them.

classDiagram
    class Owner {
        +String name
        +addPet(pet)
        +removePet(pet)
        +editPet(pet)
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
        +addTask(task)
        +removeTask(task)
        +editTask(task)
    }

    Owner "1" *-- "1" Scheduler : has
    Owner "1" *-- "0..*" Pet : owns
    Scheduler "1" o-- "0..*" Task : manages
    Task "0..*" --> "1" Pet : for

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
  Yes my design changed, I orginally had the scheduler own the task list, but then I changed it to Pet. Also I changed the Scheduler to query across pets, not hold tasks itself.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
I decided on time avaible, priority, owner preference, frewquency, completion time, and due date. I decided that time is the most important aspect, such as conflicting time is addressed, and priority so owners have more control over what matters.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
A tradeoff my scheduler makes is that it can sort by priority or by time, but not both at once.A pet owner checking their morning schedule has a clear mental model they already know their pet's walk is high priority, and they already know feeding happens at 7am. They don't need the app to weigh those against each other.One simple sort is enough for each of those decisions.                                          
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
During this project I used AI to help improve my initial UML design, create test cases for me, and to help refator based on the improvements I wanted to make on the project. The kind of prompts that were most helpful were ones that are very detailed. I found online that following PACE framework helps (Purpose, Action, Context, Explain/Format).

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
The AI suggested replacing the loop in detect_conflicts() with a shorter one-liner using intertool.combinations. Although the shorter version would look cleaner, it was harder to understand at a glance. The original loop made it obvious what was happening. Since both versions work the same way, the original was kept because it was easier to read.
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

I felt most satisfied when I looked at the finished product. Starting from a blank UML diagram and ending up with a working Streamlit app with real scheduling logic felt like a big jump. It felt satisfying to see what I brainstromed for the four classes in action in the live demo.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
The biggest thing I'd fix is making data save between sessions, right now everything disappears when you refresh the page. I'd also add a time picker so users can't accidentally type a time the app can't understand.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that I have to be specific when communicating with AI and that it is a support tool where I should be the main brain for this project. 


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