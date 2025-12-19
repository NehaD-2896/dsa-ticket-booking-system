# ================== TICKET BOOKING SYSTEM ==================

MAX_SEATS = 10
MAX_STACK = 20
MAX_QUEUE = 10


# ---------- LINKED LIST FOR BOOKING HISTORY ----------
class Node:
    def _init_(self, name, seat_no, status):
        self.name = name
        self.seat_no = seat_no
        self.status = status  # BOOKED / CANCELLED
        self.next = None


class BookingHistory:
    def _init_(self):
        self.head = None

    def add_record(self, name, seat_no, status):
        new_node = Node(name, seat_no, status)
        if not self.head:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def display(self):
        if not self.head:
            print("No booking history available.")
            return
        temp = self.head
        while temp:
            print(f"Passenger: {temp.name}, Seat: {temp.seat_no}, Status: {temp.status}")
            temp = temp.next


# ---------- MAIN SYSTEM ----------
class TicketBookingSystem:
    def _init_(self):
        self.seats = [0] * MAX_SEATS

        self.history = BookingHistory()

        # Stack (Cancellation history)
        self.stack = [None] * MAX_STACK
        self.top = -1

        # Circular Queue (Waiting list)
        self.queue = [None] * MAX_QUEUE
        self.front = -1
        self.rear = -1

    # ---------- STACK ----------
    def push_cancellation(self, name, seat_no):
        if self.top == MAX_STACK - 1:
            print("Cancellation stack full!")
            return
        self.top += 1
        self.stack[self.top] = (name, seat_no)

    def pop_cancellation(self):
        if self.top == -1:
            print("No cancellations to undo.")
            return None
        data = self.stack[self.top]
        self.top -= 1
        return data

    def show_cancellations(self):
        if self.top == -1:
            print("No cancellations yet.")
            return
        for i in range(self.top, -1, -1):
            print(f"Cancelled: {self.stack[i][0]}, Seat: {self.stack[i][1]}")

    # ---------- QUEUE ----------
    def enqueue_waiting(self, name):
        if (self.rear + 1) % MAX_QUEUE == self.front:
            print("Waiting list full!")
            return
        if self.front == -1:
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % MAX_QUEUE
        self.queue[self.rear] = name

    def dequeue_waiting(self):
        if self.front == -1:
            return None
        name = self.queue[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % MAX_QUEUE
        return name

    def show_waiting(self):
        if self.front == -1:
            print("Waiting list empty.")
            return
        i = self.front
        while True:
            print(self.queue[i])
            if i == self.rear:
                break
            i = (i + 1) % MAX_QUEUE

    # ---------- BOOKING ----------
    def book_ticket(self, name):
        for i in range(MAX_SEATS):
            if self.seats[i] == 0:
                self.seats[i] = 1
                self.history.add_record(name, i + 1, "BOOKED")
                print(f"Seat {i + 1} booked for {name}.")
                return
        print("No seats available. Added to waiting list.")
        self.enqueue_waiting(name)

    def cancel_ticket(self, seat_no):
        if seat_no < 1 or seat_no > MAX_SEATS or self.seats[seat_no - 1] == 0:
            print("Invalid seat number or seat not booked.")
            return

        self.seats[seat_no - 1] = 0

        # Find latest booking for this seat
        temp = self.history.head
        cancelled_name = None
        while temp:
            if temp.seat_no == seat_no and temp.status == "BOOKED":
                cancelled_name = temp.name
            temp = temp.next

        if cancelled_name:
            self.push_cancellation(cancelled_name, seat_no)
            self.history.add_record(cancelled_name, seat_no, "CANCELLED")
            print(f"Seat {seat_no} cancelled for {cancelled_name}.")

            waiting_person = self.dequeue_waiting()
            if waiting_person:
                self.book_ticket(waiting_person)

    def undo_cancellation(self):
        cancelled = self.pop_cancellation()
        if cancelled:
            self.book_ticket(cancelled[0])

    def show_seats(self):
        print(["Booked" if s else "Available" for s in self.seats])


# ---------- MENU ----------
system = TicketBookingSystem()

while True:
    print("\n--- Ticket Booking System ---")
    print("1. Book Ticket")
    print("2. Cancel Ticket")
    print("3. Show Booking History")
    print("4. Show Cancellation History")
    print("5. Show Waiting List")
    print("6. Show Seat Status")
    print("7. Undo Last Cancellation")
    print("8. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        name = input("Enter passenger name: ")
        system.book_ticket(name)

    elif choice == '2':
        seat_no = int(input("Enter seat number to cancel: "))
        system.cancel_ticket(seat_no)

    elif choice == '3':
        system.history.display()

    elif choice == '4':
        system.show_cancellations()

    elif choice == '5':
        system.show_waiting()

    elif choice == '6':
        system.show_seats()

    elif choice == '7':
        system.undo_cancellation()

    elif choice == '8':
        break

    else:
        print("Invalid choice.")