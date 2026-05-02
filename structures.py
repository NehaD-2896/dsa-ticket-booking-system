import heapq

class BookingSystem:
    def __init__(self):
        # Using a Min-Heap for Priority Queue
        # Format: (priority_level, customer_name)
        # Lower number = Higher priority (e.g., 1 is VIP, 2 is Regular)
        self.booking_queue = []

    def add_request(self, name: str, vip: bool = False):
        priority = 1 if vip else 2
        heapq.heappush(self.booking_queue, (priority, name))
        print(f"Added {name} to queue with priority {priority}")

    def process_next_booking(self):
        if not self.booking_queue:
            return "No pending bookings."
        priority, name = heapq.heappop(self.booking_queue)
        return f"Processing booking for: {name} (Priority Level: {priority})"

# Quick Test
system = BookingSystem()
system.add_request("Alice", vip=False)
system.add_request("Bob", vip=True) # Bob joins later but is VIP
print(system.process_next_booking()) # Bob will be processed first!
