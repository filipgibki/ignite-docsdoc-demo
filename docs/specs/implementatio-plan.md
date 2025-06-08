## Functionality Outline

This outline details the progressive changes to a frontend-only To-Do List application. The application will maintain task data in memory and load initial demo data from a static file.

### Version 1: The Basic To-Do List with In-Memory Persistence (Baseline)

* **Core Functionality:** A simple to-do list that operates entirely in the browser's memory. It loads an initial set of tasks from a static file.
* **Initial Data Loading:**
    * On application startup, tasks will be loaded from a static `data.json` file (e.g., fetched via `fetch('/data.json')`).
    * **Example `data.json` structure:**
        ```json
        [
          { "id": 1, "title": "Buy groceries", "completed": false },
          { "id": 2, "title": "Call mom", "completed": true }
        ]
        ```
    * If `data.json` cannot be loaded or is empty, the application starts with an empty list.
* **Persistence:** All task manipulations (add, update, delete) will only affect the data in the application's memory. This means data will **not persist** if the browser tab is closed or refreshed.
* **UI Layout & Elements:**
    * **Main View:** A single, **centered container** on the page.
    * **Input Area:**
        * A **text input field** at the top of the container with a placeholder like "What needs to be done?".
        * An "**Add Task**" button next to the input field.
    * **Task List Area:**
        * Below the input area, a vertically stacked list of tasks.
        * Each task is displayed in a row containing:
            * A **checkbox** on the left to indicate its `completed` status.
            * The task `title` (as text) next to the checkbox.
            * A "**Delete**" button on the far right of the row.
    * **Styling:** When a task's `completed` status is `true`, its title text is styled with a **line-through**.

---

### Version 2: Adding Priority Levels

* **Core Functionality:** Introduce priority levels to help organize tasks.
* **Data Model Change (in-memory):** The task object will now include a `priority` property.
    ```
    { "id": 1, "title": "My first task", "completed": false, "priority": "Medium" }
    ```
* **UI Layout & Elements:**
    * **Input Area Changes:**
        * A **dropdown menu (select input)** is added next to the text input, allowing the user to choose a priority: "**Low**", "**Medium**", or "**High**".
    * **Task List Area Changes:**
        * Next to the task title, a **colored badge or tag** is displayed to indicate the priority.
            * **Low:** Green badge
            * **Medium:** Orange badge
            * **High:** Red badge
    * No other layout changes. The core structure remains the same.

---

### Version 3: Adding Task Descriptions

* **Core Functionality:** Allow for more detailed task information.
* **Data Model Change (in-memory):** The task object will now include a `description` property.
    ```
    { "id": 1, "title": "My first task", "completed": false, "priority": "Medium", "description": "This is a more detailed note about the task." }
    ```
* **UI Layout & Elements:**
    * **Input Area Changes:**
        * A **multi-line text area (textarea)** is added below the main title input for the `description`. This can be initially hidden and shown on-demand, or always visible.
    * **Task List Area Changes:**
        * The task row is redesigned to be a "**card**" with two vertical sections.
        * The top section of the card contains the checkbox, title, priority badge, and delete button as before.
        * The bottom section contains the `description` text.
        * An "**Expand/Collapse**" icon (like a chevron down/up arrow) could be added to each task card to show or hide the description, keeping the initial view clean.

---

### Version 4: Filtering and Sorting Tasks

* **Core Functionality:** Allow users to filter and sort the task list to find things more easily.
* **Data Model Change:** No changes to the underlying task data model.
* **UI Layout & Elements:**
    * **Filter/Sort Bar:** A new **horizontal bar** is added between the input area and the task list.
    * **Filter Controls:**
        * "**Filter by Status**" buttons: "**All**", "**Active**", "**Completed**".
    * **Sort Controls:**
        * "**Sort by**" dropdown menu: "**Default**", "**Priority (High-Low)**", "**Title (A-Z)**".
    * **Logic:** The application will re-render the in-memory task list based on the selected filter and sort options.