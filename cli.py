from colorama import Fore, init
from datetime import datetime
import math

init(autoreset=True)


# define permissions for each role
ROLE_PERMISSIONS = {
    "user": {
        "single_status",
        "address_lookup",
        "help",
    },
    "supervisor": {
        "single_status",
        "all_status",
        "address_lookup",
        "total_mileage",
        "fleet_summary",
        "truck_manifest",
        "kpi_report",
        "help"
    },
}


# banner artwork
def print_banner():
    print(Fore.RED + "=" * 60)
    print(Fore.YELLOW + """
    ╔══════════════════════════════════════╗
    ║                                      ║
    ║        WGUPS Routing Service         ║
    ║                                      ║
    ╚══════════════════════════════════════╝""")
    print(Fore.CYAN + "     Data Structures and Algorithms II")
    print(Fore.RED + "=" * 60)
    print(Fore.WHITE + "  Student : " + Fore.GREEN + "Dean Kuhn")
    print(Fore.WHITE + "  ID      : " + Fore.YELLOW + "012897237")


def quit_service():
    print(Fore.RED + "=" * 60)
    print(Fore.YELLOW + """
    ╔══════════════════════════════════════╗
    ║                                      ║
    ║    Thank you for using WGUPS!        ║
    ║    Have a great day.                 ║
    ║                                      ║
    ╚══════════════════════════════════════╝
    """)


def get_active_packages(ht):
    return [p for p in ht.get_array() if p is not None and p != "Deactivated"]


def get_truck_by_package_id(package_id, package_to_truck):
    return package_to_truck.get(package_id)


def build_package_to_truck_map(trucks):
    package_to_truck = {}
    for truck in trucks:
        for package in truck.packages:
            package_to_truck[package.package_id] = truck
    return package_to_truck


def parse_time_input(prompt):
    print(prompt)
    while True:
        package_time_input = input(Fore.WHITE + ">>> ")
        try:
            return datetime.datetime.strptime(package_time_input, "%I:%M %p").time()
        except ValueError:
            print("Invalid time format. Please use HH:MM AM/PM.")


def prompt_int_input(prompt, valid_values=None):
    print(prompt)
    while True:
        raw_value = input(Fore.WHITE + ">>> ")
        try:
            value = int(raw_value)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if valid_values is not None and value not in valid_values:
            print("Please enter a valid number.")
            continue
        return value


def get_status_as_of(time, package, truck):
    if package.delay_time is not None and time < package.delay_time:
        return "DELAYED"
    if truck is None or time < truck.departure_time:
        return "AT HUB"
    if package.delivery_time is not None and time >= package.delivery_time:
        return "DELIVERED"
    return "EN ROUTE"


def print_delivery_time(time, package):
    if package.delivery_time is None or time < package.delivery_time:
        return "N/A"
    return f"{package.delivery_time}"


def print_package_status_line(package_time, package, package_truck):
    status = get_status_as_of(package_time, package, package_truck)
    print(
        Fore.WHITE + "Package ID: " + Fore.GREEN + f"{package.package_id}"
        + Fore.WHITE + " | Status: " + Fore.CYAN + status
        + Fore.WHITE + " | Deadline: " + Fore.RED + f"{package.deadline}"
        + Fore.WHITE + " | Delivery Time: " + Fore.YELLOW + print_delivery_time(package_time, package)
    )


def handle_package_lookup_by_id_time(context):
    package_to_truck = context["package_to_truck"]
    package_ids = {p.package_id for p in context["packages"]}
    package_id = prompt_int_input("\nEnter package ID:", valid_values=package_ids)
    package_time = parse_time_input("Enter time (HH:MM AM/PM):")
    package = context["ht"].lookup(package_id)
    package_truck = get_truck_by_package_id(package.package_id, package_to_truck)
    print("")
    print_package_status_line(package_time, package, package_truck)


def handle_all_packages_at_time(context):
    package_to_truck = context["package_to_truck"]
    package_time = parse_time_input("\nEnter time (HH:MM AM/PM):")
    print("")
    for package in context["packages"]:
        package_truck = get_truck_by_package_id(package.package_id, package_to_truck)
        print_package_status_line(package_time, package, package_truck)


def handle_address_lookup(context):
    print("\nEnter full or partial address:")
    query = input(Fore.WHITE + ">>> ").strip().lower()
    if not query:
        print("Address query cannot be empty.")
        return

    matches = [p for p in context["packages"] if query in p.address.lower()]
    if not matches:
        print("No packages matched that address query.")
        return

    print(Fore.CYAN + f"\nFound {len(matches)} package(s):")
    for package in sorted(matches, key=lambda p: p.package_id):
        print(
            Fore.WHITE + f"Package {package.package_id} | "
            + f"{package.address} | deadline {package.deadline}"
        )


def handle_total_mileage(context):
    print(Fore.WHITE + "\nTotal mileage: " + Fore.YELLOW + f"{context['total_mileage']:.2f}")
    print(Fore.WHITE + "Latest truck return: " + Fore.YELLOW + f"{context['latest_return']}")


def handle_fleet_summary(context):
    print(Fore.CYAN + "\n=== Fleet Summary ===")
    print(f"Total mileage: {context['total_mileage']:.2f}")
    print(f"Latest truck return: {context['latest_return']}")
    print(f"Total refrigeration violations: {context['total_refrig_violations']}")
    print(f"Total delay violations: {context['total_delay_violations']}")
    for stats in context["truck_stats"]:
        print(
            f"Truck {stats['truck_id']} | packages: {stats['package_count']} | "
            f"mileage: {stats['mileage']:.2f} | return: {stats['return_time']}"
        )


def handle_truck_manifest(context):
    print(Fore.CYAN + "\n=== Truck Manifests ===")
    for truck in context["trucks"]:
        print(
            f"\nTruck {truck.truck_id} | departure {truck.departure_time} | "
            f"refrigerated: {truck.refrigerated_capable}"
        )
        for package in sorted(truck.packages, key=lambda p: p.package_id):
            print(
                f"  Package {package.package_id} | {package.address} | "
                f"deadline {package.deadline} | delay {package.delay_time} | refrig {package.refrigerated}"
            )


def handle_kpi_report(context):
    total = len(context["packages"])
    delivered_on_time = 0
    delayed_at_hub = 0
    refrigerations_misassigned = 0

    for package in context["packages"]:
        truck = context["package_to_truck"].get(package.package_id)
        if package.delay_time is not None:
            delayed_at_hub += 1
        if truck is not None and package.refrigerated and not truck.refrigerated_capable:
            refrigerations_misassigned += 1
        if package.delivery_time is not None and package.deadline is not None:
            if package.delivery_time <= package.deadline:
                delivered_on_time += 1

    on_time_pct = (delivered_on_time / total * 100.0) if total else 0.0
    print(Fore.CYAN + "\n=== KPI Report ===")
    print(f"Packages total: {total}")
    print(f"Delivered by deadline: {delivered_on_time}")
    print(f"On-time percentage: {on_time_pct:.2f}%")
    print(f"Packages with delay constraints: {delayed_at_hub}")
    print(f"Refrigeration misassignments: {refrigerations_misassigned}")


def handle_help(_context):
    print(Fore.CYAN + "\nHelp:")
    print("- User role can query package status, address matches, and mileage.")
    print("- Supervisor role can also view fleet, manifest, and KPI reports.")
    print("- Time format is always HH:MM AM/PM (example: 09:30 AM).")


def select_role():
    print(Fore.WHITE + "\nSelect access role:")
    print(Fore.GREEN + "\t1. User")
    print(Fore.YELLOW + "\t2. Supervisor")
    while True:
        role_choice = input(">>> ").strip()
        if role_choice == "1":
            return "user"
        if role_choice == "2":
            return "supervisor"
        print("Please enter 1 or 2.")


def build_menu_actions(role):
    base_actions = [
        ("single_status", "Check a single package at a given time", handle_package_lookup_by_id_time),
        ("all_status", "Check all packages at a given time", handle_all_packages_at_time),
        ("address_lookup", "Lookup packages by address", handle_address_lookup),
        ("total_mileage", "View total mileage", handle_total_mileage),
        ("help", "Help", handle_help),
        ("fleet_summary", "View fleet summary", handle_fleet_summary),
        ("truck_manifest", "View truck manifests", handle_truck_manifest),
        ("kpi_report", "View KPI report", handle_kpi_report),
    ]
    allowed = ROLE_PERMISSIONS[role]
    return [action for action in base_actions if action[0] in allowed]


def run_cli(context):
    print_banner()
    role = select_role()
    keep_going = True

    while keep_going:
        print(Fore.RED + "=" * 60)
        print(Fore.WHITE + f"\nRole: " + Fore.YELLOW + f"{role.upper()}")
        print("\nWould you like to...")
        actions = build_menu_actions(role)
        for index, (_, label, _) in enumerate(actions, start=1):
            print(Fore.WHITE + f"\t{index}. " + Fore.GREEN + f"{label}?")
        quit_choice = len(actions) + 1
        print(Fore.WHITE + f"\t{quit_choice}. " + Fore.RED + "Quit?")
        print(Fore.WHITE + f"\nType a number (1) to ({quit_choice}).")

        choice = prompt_int_input("", valid_values=set(range(1, quit_choice + 1)))
        if choice == quit_choice:
            quit_service()
            break

        permission, _, handler = actions[choice - 1]
        if permission not in ROLE_PERMISSIONS[role]:
            print(Fore.RED + "Unauthorized command for this role.")
            continue

        handler(context)
        print(Fore.WHITE + "\nWould you like to quit (1) or go back to home (2)?")
        return_home = prompt_int_input("", valid_values={1, 2})
        keep_going = return_home == 2

    if keep_going is False:
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
    num_trucks = math.ceil(100/ int(num_capacity))
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
    return num_trucks, int(num_refrig), int(num_capacity)