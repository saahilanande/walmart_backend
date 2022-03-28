Input:

An input file which would contain one line of input for each reservation request. The order of the lines in the file reflects the order in which the reservation requests were received. Each line in the file will be comprised of a reservation identifier, followed by a space, and then the number of seats requested. The reservation identifier will have the format: R####. Example: R001 2 R002 4 R003 4 R004 3

Output:

The program should output a file containing the seating assignments for each request. Each row in the file should include the reservation number followed by a space, and then a comma-delimited list of the assigned seats. Example: R001 I1,I2 R002 F16,F17,F18,F19 R003 A1,A2,A3,A4 R004 J4,J5,J6

Assumptions made while implementing the Algorithm:

    1.Cost of all the seats in the theatre are same.
    2.Seats are reserved on the First come first serve basis.
    3.Customers who reserves the seat first are offered better seats(seats that are far from the screen) than the customers who are reserve later.
    4.WhenApproach to the implement the solution:

Approach to the implement the solution:

    1.Algorithm uses Greedy approach with Priority Queue implemented using Linked List.
    2.Each Row is considered as a node and has the following attributes: name, totalSeats, pointer to next node,seatsOccupied and seatsEmpty
    3.New rows(I,H,G....A) are added when the seats to be reserved are greater than continguous seats empty in the Linked List. If seats in J are smaller than the seats requested a new node with name I is added to the linked list.
    4.If the row is Full, it is removed from the List and replaced with next row. Example if J is full it was deleted from the tree and I becomes the node.
    5.Program exits if the all the rows(nodes) are full or cannot accomodate the rest of the reservation with the vacant seats

Program Files:

    inputfile_gen.py: Uses random library to generate random reservation requests.
    filereader.py: Parse the given input file of above format into list of reservations
    greedySeatAllocation: Uses greedy approach to allocate seats.

How to run the program:

    Open Command prompt or terminal.
    Move to the directory where the program is stored. Make sure all the program files are in the same folder before running the program.
    The program accepts only text files of the format where each line in the file will be comprised of a reservation identifier, followed by a space, and then the number of seats requested. The reservation identifier will have the format: R####. as displayed above.
    Ensure python module logging is present.
    Type the following command in the Command Prompt or Terminal. python movietheater.py inputFilePath
    It takes input file path as system arrgument.
    The output generated is a text file, Each row in the file should include the reservation number followed by a space, and then a comma-delimited list of the assigned seats.
    Program also generate the debug logs for event logging.
