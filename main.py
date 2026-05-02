# main.py

from service import TicketBookingSystem

system = TicketBookingSystem()

while True:
    print("\n--- Ticket System ---")
    print("1. Book")
    print("2. Cancel")
    print("3. Undo")
    print("4. Seats")
    print("5. Waiting")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter name: ")
        print(system.book_ticket(name))

    elif choice == "2":
        seat = int(input("Enter seat number: "))
        print(system.cancel_ticket(seat))

    elif choice == "3":
        print(system.undo_cancellation())

    elif choice == "4":
        print("\n".join(system.show_seats()))

    elif choice == "5":
        print(system.show_waiting())

    elif choice == "6":
        break
