import time
import threading

class VotingProcess:
    def __init__(self, id, total_processes, process_list):
        self.id = id
        self.total_processes = total_processes
        self.votes_received = 0
        self.process_list = process_list 
        self.lock = threading.Lock() 

    def request_cs(self):
        self.votes_received = 0
        print(f"Process {self.id} requests CS.")
        for p in self.process_list:
            if p.id != self.id:
                p.receive_vote(self.id)

    def receive_vote(self, sender_id):
        with self.lock:  
            self.votes_received += 1
            print(f"Process {self.id} received vote from process {sender_id}")
            if self.votes_received > self.total_processes // 2:
                self.enter_cs()

    def enter_cs(self):
        print(f"Process {self.id} enters CS")
        time.sleep(2)
        print(f"Process {self.id} exits CS")

process_list = []
for i in range(3):
    process_list.append(VotingProcess(i, 3, process_list))

def simulate(process):
    process.request_cs()

if __name__ == "__main__":
    threads = [threading.Thread(target=simulate, args=(p,)) for p in process_list]
    for t in threads:
        t.start()
    print("voting")
    for t in threads:
        t.join()
