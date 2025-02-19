import threading
import time
import random

class MutualExclusion:
    def __init__(self, num_processes):
        self.num_processes = num_processes
        self.votes = [0] * num_processes  # Votes received by each process
        self.condition = threading.Condition()
        self.lock = threading.Lock()

    def voting_mutual_exclusion(self, process_id):
        print(f"Process {process_id} requesting votes.")

        with self.condition:
            self.votes[process_id] = 0  # Reset votes before requesting
            self.request_votes(process_id)

            # Wait until the process receives more than half the votes
            while self.votes[process_id] <= self.num_processes // 2:
                self.condition.wait()

        print(f"Process {process_id} received votes: {self.votes[process_id]}")

        if self.votes[process_id] > self.num_processes // 2:
            self.enter_critical_section_voting(process_id)
        else:
            print(f"Process {process_id} did not receive enough votes.")

        print(f"Process {process_id} exiting critical section.\n")

    def request_votes(self, process_id):
        with self.condition:
            for i in range(self.num_processes):
                if i != process_id:
                    granted_vote = random.choice([True, False])
                    if granted_vote:
                        self.votes[process_id] += 1
                    print(f"Process {i} voted {'YES' if granted_vote else 'NO'} for Process {process_id}")

            # Notify all waiting processes after voting is done
            self.condition.notify_all()

    def enter_critical_section_voting(self, process_id):
        with self.lock:
            print(f"\n Process {process_id} enters critical section (voting scheme) ")
            time.sleep(1)  # Simulate critical section execution
            print(f" Process {process_id} exits critical section.\n")

if __name__ == "__main__":
    num_processes = 5
    mutual_exclusion = MutualExclusion(num_processes)
    processes = list(range(num_processes))  # Process IDs: 0, 1, 2, 3
    thread_voting = []

    for process_id in processes:
        thread = threading.Thread(target=mutual_exclusion.voting_mutual_exclusion, args=(process_id,))
        thread_voting.append(thread)
        thread.start()

    for thread in thread_voting:
        thread.join()


