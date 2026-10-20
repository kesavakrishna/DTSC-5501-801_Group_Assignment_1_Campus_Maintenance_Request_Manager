"""
Data Structures and Algorithms Class
Group Assignment

This program will satisfy the Part 14 Workload portion of the assignment

Fall 2026
"""


from random import *
import os
import contextlib
import time
from statistics import median




## Note! That the comments about the simulation are way down lower
## in this code (the questions in Part K) as a commented out section.





# Let's first go gather all the stuff we need from the other .py files
from linked_request_list import LinkedRequestList
from array_request_list import ArrayRequestList
from maintenance_request import MaintenanceRequest

# Next, let's write a small little function to take both my Dynamic Array
#       and also Ben's Linked List and see if they both run okay
#       when you ask them to do those 4 methods. 
#       The four methods to doublecheck are:
#                  findById
#                  insertAt
#                  removeAt
#                  getAt
#       And to pull this off, we'll also have to test append and __str__,
#       to put things in the lists and also then to see what's happening.

def OrionPrivateDoublecheck():
    A = ArrayRequestList()
    B = LinkedRequestList()

    print()
    print()
    print("Let's put three maintenance requests into the lists")
    
    test1a = MaintenanceRequest(1, "ABCD", "Plumbing", 1, 100, "OPEN")
    test1b = MaintenanceRequest(1, "ABCD", "Plumbing", 1, 100, "OPEN")
    A.append(test1a)
    B.append(test1b)

    test2a = MaintenanceRequest(2, "GYM", "Lights", 4, 105, "OPEN")
    test2b = MaintenanceRequest(2, "GYM", "Lights", 4, 105, "OPEN")
    A.append(test2a)
    B.append(test2b)

    test3a = MaintenanceRequest(3, "ZZ", "Smoke Detector", 3, 113, "OPEN")
    test3b = MaintenanceRequest(3, "ZZ", "Smoke Detector", 3, 113, "OPEN")
    A.append(test3a)
    B.append(test3b)

    print()
    print()
    print(A.__str__())
    print()
    print()
    print(B.__str__())

    print()
    print()
    print("Now let's test findById")

    print()
    print()
    print(A.findById(2))
    print()
    print()
    print(B.findById(2))

    print()
    print()
    print("Now let's test insertAt")

    test4a = MaintenanceRequest(4, "G", "No Hot Water", 1, 150, "OPEN")
    test4b = MaintenanceRequest(4, "G", "No Hot Wate", 1, 150, "OPEN")
    A.insertAt(1, test4a)
    B.insertAt(1, test4b)

    print()
    print()
    print(A.__str__())
    print()
    print()
    print(B.__str__())

    print()
    print()
    print("Now let's test removeAt")

    A.removeAt(2)
    B.removeAt(2)

    print()
    print()
    print(A.__str__())
    print()
    print()
    print(B.__str__())

    print()
    print()
    print("Now let's test getAt")

    print()
    print()
    print(A.getAt(1).building)
    print()
    print()
    print(B.getAt(1).building)

    print()


#OrionPrivateDoublecheck()

# Cool! The above call worked out just fine. Time to program the new stuff.



def make_10000_random_maintenance_requests(seed_randomseed):

    seed(seed_randomseed)

    # Let's make 10000 random maintenance requests.
    
    # We need 10000 request_ids... I think those could just be assigned
    #       in order from 1 through 10000

    list_of_request_IDs = []
    for i in range(10000):
        list_of_request_IDs.append(i+1)

    # We need 10000 random buildings. Let's make a small list of all the
    #       hypothetical building names for some kind of apartment complex

    building_names = ["TLRS", "BUCK", "CPMP", "FLHS", "SPSK",
                      "IPRC", "FLYC", "RAMY", "GASR", "MCOL",
                      "HALE", "ABSA", "SSKN", "CHEY", "KCHN",
                      "KCEN", "GVAS", "KTCH", "RPMP", "SWLL",
                      "FBST", "ATLS", "OBSV", "JILA", "ZUNI",
                      "NTCR", "ROBN", "ECCS", "FIRE", "THTR",
                      "ITLL", "LMBR", "PTRM", "DUAN", "WALN",
                      "LIBY", "PDPS", "ECAD", "BHRN", "DACR",
                      "REED", "VHCL", "HPCF", "PFPS", "GONG",
                      "HLMS", "INFO", "UCTR", "AERO", "STNW",
                      "LITR", "XDCB", "CEDU", "BISN", "OBSR",
                      "TNDR", "VPMP", "ATHN", "LDAR", "KITW",
                      "ECME", "BLWR", "MCFL", "MRTN", "WLRD",
                      "HFOC", "CKRL", "TRAN", "DRLN", "WILD",
                      "GROC", "WARD", "MUEN", "UINT", "PDLP",
                      "BIOT", "ADEN", "DRLS", "FISK", "JNCO",
                      "HAZM", "CHKR", "PORC", "GRGE", "GROU",
                      "RPRK", "TETN", "ECCR", "DHLL", "SMTH",
                      "MSSC", "JESS", "LESS", "KOBL", "ECNW",
                      "VOLE", "COTT", "ONKA", "KVCU", "WSTE"]
    list_of_buildings = []
    for i in range(10000):
        list_of_buildings.append(choice(building_names))

    # Next we need a list of 10000 random categories
    #       To quote the assignment: HVAC systems, electrical problems,
    #       plumbing, broken equipment, classroom technology, or other
    #       facility issues.

    category_names = ["HVAC", "ELEC", "PLUM", "EQUI", "TECH", "FACI",
                      "ALAR", "TRAS", "SPIL", "RODE", "VERM", "MESS",
                      "BIOH", "NUCL", "ROBO", "INCI", "UNKN"]
    list_of_categories = []
    for i in range(10000):
        list_of_categories.append(choice(category_names))

    # Next we need a list of 10000 random priorities

    priority_names = [1, 2, 3, 4]
    list_of_priorities = []
    for i in range(10000):
        list_of_priorities.append(choice(priority_names))

    # New we need a list of reported_times. To do this, let's add
    #       a random amount of time to the previous one.

    time_cursor = 0
    list_of_reported_times = []
    for i in range(10000):
        time_cursor += randrange(1, 11)
        list_of_reported_times.append(int(time_cursor))

    # Lastly we need a list of 10000 statuses

    list_of_status = ["OPEN"] * 10000

    list_of_MRs = []

    for i in range(10000):
        MR = MaintenanceRequest(list_of_request_IDs[i],
                                     list_of_buildings[i],
                                     list_of_categories[i],
                                     list_of_priorities[i],
                                     list_of_reported_times[i],
                                     list_of_status[i])
        list_of_MRs.append(MR)

    return list_of_MRs, list_of_request_IDs, time_cursor


def make_20000_operations(list_of_MRs, list_of_request_IDs,
                          time_cursor, seed_randomseed):

    # We're group 4, so that assigns us --> D: Audit and cleanup

    # I see that we'll need to do this:
    # For findById, look up an existing ID 80% of the time and a missing ID 20%.
    # To pull that off, we'll need to keep track of what IDs are in the data.
    #       Maybe we can use list_of_request_IDs for this.
    #       And use -1 for the missing ones.

    seed(seed_randomseed)

    building_names = ["TLRS", "BUCK", "CPMP", "FLHS", "SPSK",
                      "IPRC", "FLYC", "RAMY", "GASR", "MCOL",
                      "HALE", "ABSA", "SSKN", "CHEY", "KCHN",
                      "KCEN", "GVAS", "KTCH", "RPMP", "SWLL",
                      "FBST", "ATLS", "OBSV", "JILA", "ZUNI",
                      "NTCR", "ROBN", "ECCS", "FIRE", "THTR",
                      "ITLL", "LMBR", "PTRM", "DUAN", "WALN",
                      "LIBY", "PDPS", "ECAD", "BHRN", "DACR",
                      "REED", "VHCL", "HPCF", "PFPS", "GONG",
                      "HLMS", "INFO", "UCTR", "AERO", "STNW",
                      "LITR", "XDCB", "CEDU", "BISN", "OBSR",
                      "TNDR", "VPMP", "ATHN", "LDAR", "KITW",
                      "ECME", "BLWR", "MCFL", "MRTN", "WLRD",
                      "HFOC", "CKRL", "TRAN", "DRLN", "WILD",
                      "GROC", "WARD", "MUEN", "UINT", "PDLP",
                      "BIOT", "ADEN", "DRLS", "FISK", "JNCO",
                      "HAZM", "CHKR", "PORC", "GRGE", "GROU",
                      "RPRK", "TETN", "ECCR", "DHLL", "SMTH",
                      "MSSC", "JESS", "LESS", "KOBL", "ECNW",
                      "VOLE", "COTT", "ONKA", "KVCU", "WSTE"]

    category_names = ["HVAC", "ELEC", "PLUM", "EQUI", "TECH", "FACI",
                      "ALAR", "TRAS", "SPIL", "RODE", "VERM", "MESS",
                      "BIOH", "NUCL", "ROBO", "INCI", "UNKN"]

    priority_names = [1, 2, 3, 4]

    num_MRs = len(list_of_MRs)

    operations_list = []

    for i in range(global_num_operations_yo):

        operation = []
        
        time_cursor += randrange(1, 11)
        
        roll_a_die = random()

        if roll_a_die <= 0.4:
            # 40% chance that we findById
            operation.append("findById")
            
            roll_a_die_2 = random()
            if roll_a_die_2 <= 0.8:
                # 80% of the time it's a valid ID in the database
                ID = choice(list_of_request_IDs)
                operation.append(ID)
            else:
                # 20% of the time it's a missing ID not in the database
                ID = -1
                operation.append(ID)
            operations_list.append(operation)

            # ["findById", ID]
            

        elif roll_a_die <= 0.7:
            # 30% chance that we insertAt
            operation.append("insertAt")

            # Make the new MR
            ID = 1_000_000 + i
            building = choice(building_names)
            category = choice(category_names)
            priority = choice(priority_names)
            
            new_MR = MaintenanceRequest(ID,
                                     building,
                                     category,
                                     priority,
                                     time_cursor,
                                     "OPEN")
            
            # Pick a random place to insert it somewhere
            #       between the 20th percentile and the 80th
            lower_limit = num_MRs // 5
            upper_limit = num_MRs - (num_MRs // 5)
            random_index = randrange(lower_limit, upper_limit + 1)

                    ## Note, I'm interpreting 'middle' to be someplace
                    ##       kinda random in the center someplace, not
                    ##       the literal middle element. 

            # Record the insertion
            operation.append(random_index)
            operation.append(new_MR)
            operations_list.append(operation)

            # Update the parameters
            list_of_request_IDs.insert(random_index, ID)
            num_MRs += 1

            # ["insertAt", random_index, new_MR]

        elif roll_a_die <= 0.9:
            # 20% chance we removeAt
            operation.append("removeAt")

            # Pick a random place to remove somewhere
            #       between the 20th percentile and the 80th
            lower_limit = num_MRs // 5
            upper_limit = num_MRs - (num_MRs // 5)
            random_index = randrange(lower_limit, upper_limit + 1)

            # Do the removal
            operation.append(random_index)
            operations_list.append(operation)

            # Update the parameters
            list_of_request_IDs.pop(random_index)
            num_MRs -= 1

            # ["removeAt", random_index]

        else:
            # 10% chance we getAt
            
            # Get a completely random one this time
            random_index = randrange(0, num_MRs)

            # store the getAt request
            operation.append("getAt")
            operation.append(random_index)
            operations_list.append(operation)

            # ["getAt", ID]

    return operations_list


def build_structure(list_of_MRs, linkedList_or_not):

    # Make either the Linked List or the Dynamic Array object and place the
    #       starting MRs into it. This is kept out of the timed replay: building
    #       10000 requests is slow (every append checks for a duplicate ID)
    #       and is not part of the workload.

    if linkedList_or_not is True:
        Obj = LinkedRequestList()
    else:
        Obj = ArrayRequestList()

    for MR in list_of_MRs:
        Obj.append(MR)

    return Obj


def simulation(Obj, operations_list):

    # Replay the operation sequence on an already-built structure

    for operation in operations_list:
        whats_the_job = operation[0]

        if whats_the_job == "findById":
            # ["findById", ID]
            Obj.findById(operation[1])

        elif whats_the_job == "insertAt":
            # ["insertAt", random_index, new_MR]
            Obj.insertAt(operation[1], operation[2])

        elif whats_the_job == "removeAt":
            # ["removeAt", random_index]
            Obj.removeAt(operation[1])

        elif whats_the_job == "getAt":
            # ["getAt", ID]
            Obj.getAt(operation[1])

    return Obj




"""

Part 14, Part K analysis... (Orion's first notes, written before any benchmark.
The team's final workload predictions are in the Predictions section at the top of analysis.ipynb.)



Orion here. The assignment guide asks us to answer this question:

Before benchmarking, state which operations dominate, predict which implementation fits
better and why, and name one workload change that could change your recommendation. 

Sure! So... As far as I know (although the Big-O part of the assignment is Ben's to do),
findById should be O(n), having to linearly search through each type of list to find
its querry. We have an estimated 20000 * 40% = 8000 of those. 

insertAt should be O(1) for my Dynamic Array, and O(n) for Ben's Linked List.
We have an estimated 20000 * 30% = 6000 of those.

Oh! But even my dynamic array still has to shuffle over everything, making it O(n).

removeAt should be similar to insertAt. About 4000 of those. They're O(n).

Lastly, getAt is O(1) for Orion's and O(n) for Ben's. There are 2000 of those or so.

I'm going to predict that for the Dynamic array the getAt will take hardly any time
at all compared to the other three actions, while aught (?) to dominate the behavior.

This is just a prediction. But I'm going to think that due to them being O(n), that
for Ben's all 4 operations will be relatively balanced, each taking up at least more
than maybe 5% of the runtime? While for Orion's, the first three operations will be
fairly balanced (more than 5% each), but will completely dominated getAt.

Let's see if that prediction comes true!


Part of me thinks that due to the vanishing getAt, my Dynamic Array might run faster.
But ... nah. Can't be. It has to do so much updating of the entire array all the time.
Things like insertAt, for Ben's linked list can just traverse the array, snap in the
new element, and be done! Whereas my Dynamic Array always has to travel the rest updating.

I'm going to guess (?) that the Linked List, due to its simplicity, will out perform
the Dynamic Array.

If the primary work task was getAt, then the Dynamic Array structure would be WAY faster.
Possibly 1000x faster!

"""


# Now let's run those simulations and see what happens!

# Run both structures on the identical sequence, time the whole replay,
# report the median of at least 5 runs, and record the final collection size.


def the_experiment(num_trials, num_operations, seed_randomseed=42):

    print()
    print()
    print("Now let's run a simulation benchmark testing both types")
    print("of lists for speed!")

    global global_num_operations_yo
    global_num_operations_yo = num_operations

    # Make the starting MRs and ONE fixed operation sequence from the seed.
    #       Every run, on both structures, replays this same sequence.
    list_of_MRs, list_of_request_IDs, time_cursor = make_10000_random_maintenance_requests(
        seed_randomseed)
    operations_list = make_20000_operations(list_of_MRs,
                                            list(list_of_request_IDs),
                                            time_cursor,
                                            seed_randomseed)

    op_counts = {}
    for operation in operations_list:
        op_counts[operation[0]] = op_counts.get(operation[0], 0) + 1
    print("Operation counts:", op_counts)

    results = {}

    for name, linkedList_or_not in (("Linked List", True), ("Dynamic Array", False)):
        times = []
        final_num_MRs = []
        for i in range(num_trials):
            # The replay changes the structure, so build a fresh one every run (not timed)
            Obj = build_structure(list_of_MRs, linkedList_or_not)
            start_time = time.perf_counter()
            simulation(Obj, operations_list)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
            final_num_MRs.append(Obj.count())

            # Adding a tiny progress bar
            print(name + ": run " + str(i + 1) + " of " + str(num_trials) + " done")

        results[name] = {"median_seconds": median(times), "final_sizes": final_num_MRs}

    print()
    print()
    print("We did " + str(num_trials) + " runs of the same " + str(num_operations)
          + " operations on each structure.")
    print("... These were the results:")
    for name, result in results.items():
        print()
        print("The " + name + " median runtime was:")
        print("       " + str(result["median_seconds"]) + " seconds.")
        print("It resulted in final MR array sizes of:")
        print(result["final_sizes"])

    results["operation counts"] = op_counts
    return results


if __name__ == "__main__":
    the_experiment(5, 20000)
