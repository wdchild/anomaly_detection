
'''Since networks return person objects (memory values) that are hard to identify,
   this convenience function describes a network in terms of the IDs 
   of the persons in the network. This makes it easier to test whether
   a network is being correctly identified.'''
def describeNetwork(net):
    net_string = 'NETWORK: '
    for friend in net:
        net_string += str(friend.ID)
        net_string += ' '
    net_sring = net_string[:-1] # get rid of exta space
    return net_string

'''A class of person (purchaser) who has friends and a set of purchases.'''
class Person():
    people = [] 

    @classmethod
    def personWithIDexists(self, personID):
        #print('calling class method')
        exists = False
        for bloke in Person.people:
            #print(bloke)
            if (bloke.ID == personID):
                #print(bloke.ID, personID)
                exists = True
        return exists

    @classmethod
    def createPerson(self, ID):
        friends = set()
        purchases = []
        Person(ID, friends, purchases)

    @classmethod
    def getPerson(self, ID):
        for bloke in Person.people:
            if (bloke.ID == ID):
                #print('bloke found with ID {}'.format(ID))
                return bloke            
        return None

    def __init__(self, ID, friends, purchases):
        self.ID = ID
        self.friends = set()
        self.purchases = []
        Person.people.append(self)

    def description(self):
        print('person ID:' , self.ID)
        print('friends:' , self.listFriends())
        print('purchases:' , self.purchases)

    def addFriend(self, new_friend):
        # cannot befriend self in this system
        # print('self ID is: {}'.format(self.ID))
        # print('new_friend is: {}'.format(new_friend))
        if (new_friend.ID != self.ID):
            self.friends.add(new_friend)
            new_friend.friends.add(self) #bidirectional friendship
            #print('{} became friends with {} and vice versa'.format(self.ID, new_friend.ID))
            #print('{} now has these friends {}'.format(self.ID, self.listFriends()))
        else:
            print('Cannot befriend oneself.')

    def removeFriend(self, former_friend):
        if (former_friend in self.friends):
            self.friends.remove(former_friend)
            former_friend.friends.remove(self) # bidirectional relationship, must remove friends in both direction
            # print('{} is no longer friends with {} and vice versa'.format(self.ID, former_friend.ID))
        else:
            print('former_friend was not a friend, so cannot remove')

    def listFriends(self):
        num_friends = len(self.friends)
        friends_list = str()
        for f in self.friends:
            friends_list += str(f.ID)
            friends_list += (', ')
        friends_list = friends_list[:-2] #get rid of extra comma/sp
        if num_friends > 3:
            print('{} has {} friend(s): {}'.format(self.ID, num_friends, friends_list))
        return friends_list

    def localNetworkOfFriends(self, degree, network):
        #print('\nINITIAL degree: {} network: {}\n'.format(degree, describeNetwork(network)))
        if (degree == 1):
            #print('FIRST IF evaluating friend {}'.format(self.ID))
            network = self.friends | network #union of what was passed plus friends
            network.add(self)
            #print('After first-if union at deg = 1, degree: {} network: {}\n'.format(degree, describeNetwork(network)))
            return network
        else:
            #print('SECOND IF')
            #print('In second-if, degree: {} network: {}'.format(degree, describeNetwork(network)))

            for f in self.friends:
                #print('FOR STATEMENT')
                #print('Now doing friend {} with degree {}'.format(f.ID, degree-1))
                network = network | f.localNetworkOfFriends(degree-1, network)
                #print('returning network is {}'.format(describeNetwork(network)))
            return network
        print('At the end network is {}'.format(describeNetwork(network)))
        return network


    ''' Method to determine if a person exists in the People class'''
    ''' for development purposes, could remove during refactoring'''
    def exists(self):
        if (self in Person.people):
            return True
        return False













