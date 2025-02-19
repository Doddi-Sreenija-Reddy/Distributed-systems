import time
import threading

class Process:
    def __init__(self, id, total_processes):
        self.id = id
        self.timestamp = 0
        self.queue = []
        self.cs_in_use = False
        self.total_processes = total_processes

    def request_cs(self):
        self.timestamp += 1
        print(f"Process {self.id} requests CS at timestamp {self.timestamp}")
        for p in process_list:
            if p.id != self.id:
                p.receive_request(self.id, self.timestamp)

    def receive_request(self, sender_id, sender_timestamp):
        if (self.timestamp < sender_timestamp) or (self.timestamp == sender_timestamp and self.id < sender_id):
            self.queue.append((sender_id, sender_timestamp))
        else:
            print(f"Process {self.id} grants permission to process {sender_id}")

    def enter_cs(self):
        if not self.cs_in_use:
            self.cs_in_use = True
            print(f"Process {self.id} enters CS")
            time.sleep(2)  # Simulate CS work
            self.release_cs()

    def release_cs(self):
        self.cs_in_use = False
        for sender_id, _ in self.queue:
            print(f"Process {self.id} releases CS to process {sender_id}")
        self.queue.clear()

# Initialize processes
process_list = [Process(i, 3) for i in range(3)]

# Simulate CS requests
def simulate():
    for p in process_list:
        p.request_cs()
        p.enter_cs()

if __name__ == "__main__":
    threads = [threading.Thread(target=simulate) for _ in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()