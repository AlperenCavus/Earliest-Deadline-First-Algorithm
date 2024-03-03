import matplotlib.pyplot as plt
from math import gcd

class Task:
    def __init__(self, name, execution_time, period, deadline_multiplier):
        self.name = name
        self.execution_time = execution_time
        self.period = period
        self.deadline_multiplier = deadline_multiplier
        self.deadline = period * deadline_multiplier
        self.priority = None  # Priority will be set during task prioritization

def edf_algorithm(tasks):
    time = 0
    completed_tasks = []

    # Calculate the Least Common Multiple (LCM) of periods
    lcm = tasks[0].period
    for task in tasks[1:]:
        lcm = lcm * task.period // gcd(lcm, task.period)

    gantt_chart = []

    # Dictionary to track current execution times for each task
    current_execution_times = {task.name: 0 for task in tasks}

    while time <= lcm:
        # Task prioritization - set priorities for tasks
        for task in tasks:
            task.priority = task.deadline - time

        # Task scheduling - sort tasks based on their deadlines and priority
        tasks.sort(key=lambda x: (x.deadline, -x.priority))

        # Task scheduling - select the task with the earliest deadline for execution
        current_task = tasks[0]

        # Adjust the starting time to avoid overlapping
        current_execution_time = current_execution_times[current_task.name]
        start_time = max(time, current_execution_time)

        # Task execution
        gantt_chart.append((current_task.name, start_time, start_time + current_task.execution_time))
        time = start_time + current_task.execution_time

        # Update task parameters for the next period
        current_task.deadline += current_task.period
        current_task.priority = None  # Reset priority, it will be set during the next task prioritization

        # Update current execution time for the task
        current_execution_times[current_task.name] = time

        # Check termination conditions
        completed_tasks.append(current_task)

    return gantt_chart

def draw_gantt_chart(gantt_chart):
    fig, gnt = plt.subplots()

    gnt.set_xlabel('Time')
    gnt.set_ylabel('Tasks')

    task_rows = {}  # Dictionary to track the row for each task

    for i, task in enumerate(gantt_chart):
        task_name, start_time, end_time = task

        if task_name not in task_rows:
            # If the task is not in the dictionary, assign it a new row
            task_rows[task_name] = len(task_rows)

        row = task_rows[task_name]

        gnt.broken_barh([(start_time, end_time - start_time)], (row, 0.5), facecolors=('blue'))

    plt.yticks(range(len(task_rows)), list(task_rows.keys()))
    plt.xticks(range(0, max(task[2] for task in gantt_chart) + 1, 1))
    plt.show()

if __name__ == "__main__":
    tasks = [
        Task("Task1", 2, 5, 1),
        Task("Task2", 3, 7, 1),
        Task("Task3", 1, 4, 1),
    ]

    gantt_chart = edf_algorithm(tasks)

    for task in gantt_chart:
        print(f"Executing {task[0]} at time {task[1]}")

    draw_gantt_chart(gantt_chart)
