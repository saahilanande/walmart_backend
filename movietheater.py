#Author: Saahil Anande
#This program takes command line input of file path and show the path to the output file with allocated seats to reservation ID.


import  logging
from re import search
import sys
from filereader import inputParser
logging.basicConfig(filename='debug.log',level=logging.DEBUG)



seats = 20
output={}

class Node:

    def __init__(self,rowname,seats,currentNode,seatRequested,reservationID) -> None:

        self.name = rowname
        self.seatsOccupied = [0]*seats
        self.parent = currentNode
        self.isFull = False
        self.reserve_seat(seatRequested,reservationID)
        self.emptySeats = self.check_seat()
        self.subs=[None,None]

    def reserve_seat(self,seatRequested,reservationID):
        seatsAssigned=[]

        for seat in range(len(self.seatsOccupied)):
            if seatRequested != 0:
                if self.seatsOccupied[seat] == 0:
                    self.seatsOccupied[seat] = reservationID
                    seatRequested -= 1
                    seatsAssigned.append(self.name + str(seat + 1))
            else:
                break
        
        if reservationID in output:
            output[reservationID]+=","+",".join(seatsAssigned)
        else:
            output[reservationID]=",".join(seatsAssigned)

        return self.seatsOccupied

    def check_seat(self):
        counter=0
        for i in self.seatsOccupied:
            if i ==0:
                counter += 1
        return counter


class Null:
    def __init__(self,seats) -> None:
        self.name = None
        self.seatsPresent = [0]
        self.emptySeats = None
        self.subs=[None,None]
        self.seatsOccupied = [0]*seats
        self.parent=None
        self.level = 0

nullNode = Null(seats)

class SeatAssignment:

    def __init__(self) -> None:
        self.rows = 10
        self.column = 20
        self.seatsAvailable = self.column * self.rows
        self.lastInsert = None
        self.root = nullNode

    def initallookup(self,seatRequested):
        if self.root != nullNode:
            logging.debug("Root node already present")
            return self.lookup(self.root, seatRequested)

    def lookup(self, currentNode, seatRequested): # recursive function to look for seats with empty seats
        logging.debug("Current Node is: {} and vacant seat are {} and seat requested are {}".format( currentNode.name,currentNode.emptySeats,seatRequested))
        if currentNode.emptySeats >= seatRequested:
            return currentNode

        else:
            sub = currentNode.subs[1]

            if sub != None:
                logging.debug("Current Node is {} with vacant seats {}".format(currentNode.name,currentNode.emptySeats))
                logging.debug("Trying to find better match in other nodes.....")
                return self.lookup(sub, seatRequested)

            else:
                logging.debug("No existing vacant node found, creating a new node.....!")
                return None


    def inital_insert(self, seatRequested,reservationID,seats):
        if self.root != nullNode:
            self.lastInsert = self.insert(self.root,seatRequested,self.column,reservationID)
            self.Delete(self.lastInsert)

        else:
            logging.info("Adding new root row to the List")
            name = chr(self.column + 64)           #generate the row name
            self.root = Node(name,seats,None,seatRequested,reservationID)
            self.column -=1
            self.lastInsert = self.root
            self.seatsAvailable = self.seatsAvailable - seatRequested

    def insert(self,currentNode, seatRequested, column, reservationID):

        if seatRequested <= currentNode.emptySeats: #if there are seats avaliable in the row
            currentNode.seatsOccupied = currentNode.reserve_seat(seatRequested,currentNode.reservationID)
            currentNode.emptySeats = currentNode.check_seat() #update the empty seats
            self.seatsAvailable = self.seatsAvailable - seatRequested #update the avaliable seats

        elif seatRequested > currentNode.emptySeats: #if there no seat avaliable in the current node(row), lookup to find best place to add new node

            if currentNode.subs[1]:
                return self.insert(currentNode.subs[1],seatRequested,column,reservationID)

            elif currentNode.subs[1] == None and column > 0: #adding a new node (row) to the list

                name = chr(self.column + 64)
                currentNode.subs[1] = Node(name,seats,currentNode,seatRequested,reservationID) #creating a new node
                logging.info("Addign new row {} to the List".format(name))
                self.seatsAvailable = self.seatsAvailable - seatRequested #updating avaliable seats
                self.column -= 1    #subtrating one column

        return currentNode.subs[1]

    def Delete(self,currentNode):   # deleting the nodes(row) from the list for efficient search
        if currentNode.emptySeats == 0:
            logging.debug("deleted node {}".format(currentNode.name))

            if currentNode == self.root and currentNode.subs[1] is not None:

                currentNode.subs[1].parent= None
                self.root=currentNode.subs[1]
                return self.root

            elif currentNode!= self.root:
                currentNode.parent.subs[1]=currentNode.subs[1]
                if currentNode.subs[1]!=None:
                    currentNode.subs[1].parent=currentNode.parent
                    return currentNode.parent

            else:
                self.root=nullNode
                return self.root

    def verify_seats(self,seatRequested,reservationID): #checking if any back row with seats exists else call insert function
        logging.debug ("Reservation ID: {} Seat Requested : {} ".format(reservationID,seatRequested))
        canInsertSeats = False

        if seatRequested > 20:
            return canInsertSeats
        
        node = self.initallookup(seatRequested)

        if node == None and self.column > 0: #no empty seats in the row
            self.inital_insert(seatRequested,reservationID,seats)
            canInsertSeats = True
        
        elif node != None: #there are avaliable seats
            logging.debug("No need to add a new node reservation can be accomodated in {}".format(node.name))
            node.reserve_seat(seatRequested,reservationID)
            node.emptySeats = node.check_seat()
            parent = self.Delete(node)
            self.seatsAvailable = self.seatsAvailable - seatRequested #update the avaliable seats
            canInsertSeats = True

        elif self.column == 0:
            return canInsertSeats
        
        return canInsertSeats

    def split_insert(self,seatsRequested, reservationID): # spliting the later bookings to utilise the theater
        logging.info("splitting the booking")
        currentNode = self.root
        while currentNode != None and seatsRequested !=0:

            if currentNode.emptySeats <= seatsRequested:

                logging.debug('current node name:{} empty seats:{} current seat requested: {}'.format(currentNode.name,str(currentNode.seatsEmpty),str(seatsRequested)))
                currentNode.reserve_seat(currentNode.emptySeats,reservationID)
                seatsRequested -= currentNode.emptySeats
                currentNode.emptySeats = currentNode.check_seat()
                currentNode = currentNode.subs[1]

                if currentNode is not None:

                    self.Delete(currentNode.parent)

            else:
                logging.debug('current node name {} empty seats:{} seats requested: {}'.format(currentNode.name,str(currentNode.emptySeats),str(seatsRequested)))
                currentNode.reserve_seat(seatsRequested,reservationID)
                currentNode.emptySeats = currentNode.check_seat()
                seatsRequested -= seatsRequested
                self.Delete(currentNode)

        self.seatsAvailable = self.seatsAvailable - seatsRequested #update the avaliable seats

    def output_writing(self,data,output):
        logging.info("Program Finished....Writing seats allocated to the file")
        outfile= open("outfile.txt", 'w+')
        for eachReservationRequest in data:
            if eachReservationRequest[0] in output:
                outfile.write('{} {}\n'.format(eachReservationRequest[0],output[eachReservationRequest[0]]))
            else:
                outfile.write('{} {}\n'.format(eachReservationRequest[0], str(0)))



if __name__ == '__main__':
    try:
        filePath =sys.argv[1]
    except FileNotFoundError as error:
        print(error)


    data = inputParser(filePath)

    seatArrangement = SeatAssignment()
    not_inserted = []

    for eachReservation in data:
        if seatArrangement.seatsAvailable == 0:
            logging.info("Theatre is full no vacant seat available")
            break
        
        if not seatArrangement.verify_seats(eachReservation[1],str(eachReservation[0])):
            not_inserted.append(eachReservation)

    sorted_not_inserted_bookings=(sorted(not_inserted,key=lambda x:x[1]))
    more_inserted = []

    for eachReservation in sorted_not_inserted_bookings: # allocating remaining seats by splitting groups to utilize theater
        if seatArrangement.seatsAvailable == 0:
            logging.info("Theatre is full no vacant seat available")
            break
        elif eachReservation[1] > seatArrangement.seatsAvailable:
            continue
        else:
            more_inserted.append(eachReservation)
            seatArrangement.split_insert(eachReservation[1], str(eachReservation[0]))

    seatArrangement.output_writing(data,output)

        
    
    


# newres = Node(20,"saahil",1,3,"112233")
# temp = SeatAssignment()