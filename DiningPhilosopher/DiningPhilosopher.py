import threading
import random
import time
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from queue import Queue

class Fork:
    def __init__(self, index: int, lock: threading.Lock, queue: Queue):
        """
        Fork class representing a fork on the dining table.

        Parameters:
        - index (int): The unique identifier of the fork.
        - lock (threading.Lock): A lock to handle fork access synchronization.
        - queue (Queue): A queue for communication between forks and philosophers.
        """
        self.index: int = index
        self.lock: threading.Lock = lock
        self.picked_up: bool = False
        self.owner: int = -1
        self.queue: Queue = queue

    def __enter__(self):
        return self

    def pickup(self, owner: int):
        """
        Attempt to pick up the fork.

        Parameters:
        - owner (int): The unique identifier of the philosopher attempting to pick up the fork.

        Returns:
        - bool: True if the fork is successfully picked up, False otherwise.
        """
        if self.lock.acquire(timeout=1):
            self.owner = owner
            self.picked_up = True
            self.queue.put((self.index, "pickup"))
            return True
        else:
            return False

    def put_down(self):
        """
        Put down the fork, releasing the lock.
        """
        self.lock.release()
        self.picked_up = False
        self.owner = -1
        self.queue.put((self.index, "put down"))

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        return f"F{self.index:2d} ({self.owner:2d})"

class Philosopher(threading.Thread):
    def __init__(self, index: int, left_fork: Fork, right_fork: Fork, spaghetti: int, queue: Queue):
        """
        Philosopher class representing a philosopher at the dining table.

        Parameters:
        - index (int): The unique identifier of the philosopher.
        - left_fork (Fork): The left fork the philosopher can use.
        - right_fork (Fork): The right fork the philosopher can use.
        - spaghetti (int): The initial count of spaghetti portions.
        - queue (Queue): A queue for communication between philosophers and forks.
        """
        super().__init__()
        self.index: int = index
        self.left_fork: Fork = left_fork
        self.right_fork: Fork = right_fork
        self.spaghetti: int = spaghetti
        self.eating: bool = False
        self.finished: bool = False
        self.queue: Queue = queue

    def run(self):
        """
        The main run loop for the philosopher, where they think and eat until spaghetti is finished.
        """
        while self.spaghetti > 0:
            self.think()
            self.eat()
        print(f"P{self.index} left the table.")
        self.finished = True

    def think(self):
        """
        Simulate the philosopher thinking by sleeping for a random amount of time.
        """
        time.sleep(1 + random.random() * 3)

    def eat(self):
        """
        Simulate the philosopher eating while acquiring both forks.
        """
        if self.finished:
            return

        while True:
            if self.left_fork.pickup(self.index):
                if self.right_fork.pickup(self.index):
                    break
                else:
                    self.left_fork.put_down()
            else:
                time.sleep(0.1)

        try:
            if self.finished:
                return

            self.spaghetti -= 1
            self.eating = True
            self.queue.put((self.index, "eating"))
            time.sleep(2 + random.random() * 2)
        finally:
            self.eating = False
            self.left_fork.put_down()
            self.right_fork.put_down()
            self.queue.put((self.index, "put down"))

    def __str__(self):
        return f"P{self.index:2d} ({self.spaghetti:2d})"

def animated_table(philosophers: list[Philosopher], forks: list[Fork], m: int):
    """
    Visualize the dining philosophers and forks using Matplotlib animation.

    Parameters:
    - philosophers (list[Philosopher]): List of philosopher instances.
    - forks (list[Fork]): List of fork instances.
    - m (int): Maximum spaghetti portions each philosopher has.
    """
    queue = Queue()

    # Matplotlib setup
    fig, ax = plt.subplots()
    # Additional setup code...

    def update(frame):
        """
        Update function for Matplotlib animation. Update the philosopher and fork visualizations.

        Parameters:
        - frame: Unused parameter required by Matplotlib animation.
        """
        # Visualization update code...

    ani = animation.FuncAnimation(
        fig, update, frames=range(100000), interval=10, blit=False
    )
    plt.show()

def table(philosophers: list[Philosopher], forks: list[Fork], m: int):
    """
    Simulate the dining table with philosophers and forks.

    Parameters:
    - philosophers (list[Philosopher]): List of philosopher instances.
    - forks (list[Fork]): List of fork instances.
    - m (int): Maximum spaghetti portions each philosopher has.
    """
    while sum(philosopher.spaghetti for philosopher in philosophers) > 0:
        # Console-based table visualization...

def main() -> None:
    """
    Main function to initialize and run the dining philosophers simulation.
    """
    n: int = 5
    m: int = 7
    forks: list[Fork] = [Fork(i, threading.Lock(), Queue()) for i in range(n)]
    philosophers: list[Philosopher] = [
        Philosopher(i, forks[i], forks[(i + 1) % n], m, forks[i].queue) for i in range(n)
    ]

    for i in range(n):
        right_fork_index = i
        left_fork_index = (i + n - 1) % n
        philosophers[i] = Philosopher(i, forks[right_fork_index], forks[left_fork_index], m, forks[i].queue)

    for philosopher in philosophers:
        philosopher.start()

    threading.Thread(target=table, args=(philosophers, forks, m), daemon=True).start()
    animated_table(philosophers, forks, m)

    for philosopher in philosophers:
        philosopher.join()

if __name__ == "__main__":
    main()
