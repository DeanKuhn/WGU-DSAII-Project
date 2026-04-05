from colorama import Fore, init
import datetime
import time
import math

init(autoreset=True)

def print_banner():
    print(Fore.RED + "=" * 60)
    print(Fore.YELLOW + """
  ██╗    ██╗ ██████╗ ██╗   ██╗██████╗ ███████╗
  ██║    ██║██╔════╝ ██║   ██║██╔══██╗██╔════╝
  ██║ █╗ ██║██║  ███╗██║   ██║██████╔╝███████╗
  ██║███╗██║██║   ██║██║   ██║██╔═══╝ ╚════██║
  ╚███╔███╔╝╚██████╔╝╚██████╔╝██║     ███████║
   ╚══╝╚══╝  ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝
          """)
    print(Fore.CYAN + "     Data Structures and Algorithms II")
    print(Fore.RED + "=" * 60)
    print(Fore.WHITE + f"  Student : " + Fore.GREEN + "Dean Kuhn")
    print(Fore.WHITE + f"  ID      : " + Fore.YELLOW + "012897237")

def quit_service():
    print(Fore.RED + "=" * 60)
    print(Fore.YELLOW + """
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║    Thank you for using WGUPS!         ║
    ║    Have a great day.                  ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
    """)

def quit_or_return_home(keep_going):
    print(Fore.WHITE + "\nWould you like to quit (1) or go back to home (2)?")
    while (True):
        return_home = input(">>>")
        try:
            int(return_home)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if int(return_home) not in (1, 2):
            print("Please enter a valid number.")
            continue
        else:
            if int(return_home) == 1:
                keep_going = False
                print('')
                break
            if int(return_home) == 2:
                keep_going = True
                print('')
                break

    return keep_going

# checks if package has been delivered yet or not
def print_delivery_time(package_time, package):
    if package_time < package.delivery_time:
        return "N/A"
    else:
        return f"{package.delivery_time}"

def find_package_status(package_time, package, package_truck):
    if package_time < datetime.time(9, 5) and package.package_id in (6, 25, 28, 32):
        print(Fore.WHITE + "Package ID: " + Fore.GREEN + f"{package.package_id}"
              + Fore.WHITE + " | Status: " + Fore.CYAN + "DELAYED"
              + Fore.WHITE + " | Deadline: " + Fore.RED + f"{package.deadline}"
              + Fore.WHITE + " | Delivery Time: " + Fore.YELLOW + print_delivery_time(package_time, package))
    elif package_time >= package.delivery_time:
        print(Fore.WHITE + "Package ID: " + Fore.GREEN + f"{package.package_id}"
              + Fore.WHITE + " | Status: " + Fore.CYAN + "DELIVERED!"
              + Fore.WHITE + " | Deadline: " + Fore.RED + f"{package.deadline}"
              + Fore.WHITE + " | Delivery Time: " + Fore.YELLOW + print_delivery_time(package_time, package))
    elif package_time < package.delivery_time and package_time >= package_truck.departure_time:
        print(Fore.WHITE + "Package ID: " + Fore.GREEN + f"{package.package_id}"
              + Fore.WHITE + " | Status: " + Fore.CYAN + "EN ROUTE"
              + Fore.WHITE + " | Deadline: " + Fore.RED + f"{package.deadline}"
              + Fore.WHITE + " | Delivery Time: " + Fore.YELLOW + print_delivery_time(package_time, package))
    elif package_time < package_truck.departure_time:
        print(Fore.WHITE + "Package ID: " + Fore.GREEN + f"{package.package_id}"
              + Fore.WHITE + " | Status: " + Fore.CYAN + "AT HUB"
              + Fore.WHITE + " | Deadline: " + Fore.RED + f"{package.deadline}"
              + Fore.WHITE + " | Delivery Time: " + Fore.YELLOW + print_delivery_time(package_time, package))

def find_package_truck(package, truck1, truck2, truck3):
    package_truck = None
    if package in truck1.packages:
        package_truck = truck1
    elif package in truck2.packages:
        package_truck = truck2
    elif package in truck3.packages:
        package_truck = truck3

    return package_truck

def run_cli(mileage, ht, truck1, truck2, truck3):
    print_banner()
    play_quit_service = True
    keep_going = True
    choice = -1
    while(keep_going):
        print(Fore.RED + "=" * 60)
        print("\nWould you like to...")
        print(Fore.WHITE + "\n\t1. " + Fore.GREEN + "Check a single package at a given time?")
        print(Fore.WHITE + "\t2. " + Fore.CYAN + "Check all packages at a given time?")
        print(Fore.WHITE + "\t3. " + Fore.YELLOW + "View total mileage?")
        print(Fore.WHITE + "\t4. " + Fore.RED + "Quit?")
        print(Fore.WHITE + "\nType a number (1), (2), (3), or (4).")
        while (True):
            choice = input(">>>")
            try:
                int(choice)
            except ValueError:
                print("Please enter a valid number.")
                continue
            if int(choice) not in (1, 2, 3, 4):
                print("Please enter a valid number.")
            else:
                break

        # =====================================================================
        if int(choice) == 1:
            package_truck = None
            # ask for package id
            print(Fore.WHITE + "\nEnter package ID: ")
            while (True):
                package_id = input(Fore.WHITE + ">>> ")
                try:
                    int(package_id)
                except ValueError:
                    print("Please enter a valid package ID.")
                    continue
                if int(package_id) not in range(1, 41):
                    print("Please enter a valid ID.")
                else:
                    break

            # ask for time
            print("Enter time (HH:MM AM/PM): ")
            while True:
                package_time_input = input(Fore.WHITE + ">>> ")
                # convert time to datetime
                try:
                    package_time = datetime.datetimestrptime(package_time_input, "%I:%M %p").time()
                except ValueError:
                    print("Invalid time format.  Please use HH::MM AM/PM.")
                    continue
                break

            # find package info
            package_id = int(package_id)
            package = ht.lookup(package_id)
            # find what truck it was on
            package_truck = find_package_truck(package, truck1, truck2, truck3)

            print('')
            find_package_status(package_time, package, package_truck)
            keep_going = quit_or_return_home(keep_going)

        # =====================================================================
        if int(choice) == 2:
            package_truck = None
            # ask for time
            print("\nEnter time (HH:MM AM/PM): ")
            while True:
                package_time_input = input(Fore.WHITE + ">>> ")
                # convert time to datetime
                try:
                    package_time = datetime.datetime.strptime(package_time_input, "%I:%M %p").time()
                except ValueError:
                    print("Invalid time format.  Please use HH::MM AM/PM.")
                    continue
                break

            print('')
            for package in ht.get_array():
                if package is None or package == 'Deactivated':
                    continue
                time.sleep(0.1)
                package_truck = find_package_truck(package, truck1, truck2, truck3)
                find_package_status(package_time, package, package_truck)
            keep_going = quit_or_return_home(keep_going)

        # =====================================================================
        if int(choice) == 3:
            print(Fore.WHITE + "\nTotal mileage: " + Fore.YELLOW + f"{mileage:.2f}")
            keep_going = quit_or_return_home(keep_going)

        # =====================================================================
        if int(choice) == 4:
            play_quit_service = False
            quit_service()
            break

    # =========================================================================
    if play_quit_service:
        quit_service()

def ask_intro_questions():
    print("Welcome!  Please enter the capacity of each truck.")
    print("(must be between 10 and 30)")
    while (True):
        num_capacity = input(Fore.WHITE + ">>> ")
        try:
            int(num_capacity)
        except ValueError:
            print("Please enter a valid capacity.")
            continue
        if int(num_capacity) not in range(10, 31):
            print("Please enter a valid capacity.")
        else:
            break
    num_trucks = math.ceil(87 / int(num_capacity))
    print(f"Number of trucks (based off of capacity): {num_trucks}.")
    print("How many of these trucks can hold refrigerated items? (must be at least one)")
    while (True):
        num_refrig = input(Fore.WHITE + ">>> ")
        try:
            int(num_refrig)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if int(num_refrig) not in range(1, num_trucks):
            print("Please enter a valid number.")
        else:
            break
    return num_trucks, num_refrig, num_capacity