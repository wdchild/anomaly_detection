#!/Users/danielchild/anaconda/bin/python3 *** REMOVE THIS WHEN SUBMITTING


'''This class handles the importing and exporting of JSON data that is found in the batch, log, and dump files. 
   Having a class is not strictly necessary but it makes it easier to compartmentalize its functions.
   Having this class also makes it possible to make other code more readable
   by focusing on the higher-level code.'''

import json
from person import *
from purchase import *
from statistics import pstdev # for population std dev (not sample)
import os

class EventHandler:
	degree = 0
	consec_purchase_count = 0

	def __init__(self, bp, sp, fp):
		print('Initiating handler.')
		self.batch_path = bp
		self.stream_path = sp
		self.flagged_path = fp


	def processBatchData(self):
		# cwd = os.getcwd()  # used to debug test file issues
		# print('Current directory according to event handler is:\n {}\n'.format(cwd))
		print('Processing batch data...')
		with open(self.batch_path, 'r') as f:
			lines = f.readlines()
			headerline = lines[0] # contains seed parameters 'degree' and 'transaction count'
			header = json.loads(headerline)
			EventHandler.degree = int(header['D'])
			EventHandler.consec_purchase_count = int(header['T'])

			dataLines = lines[1:]

			for line in dataLines:
				data = json.loads(line)
				self.createPeopleIfNeeded(data)

				if data['event_type'] == "purchase":
					self.savePurchase(data)

				elif data['event_type'] == "befriend":
					self.createFrienship(data)

				elif data['event_type'] == "unfriend":
					self.dissolveFriendship(data)

				else:
					print('UNRECOGNIZED EVENT')

	def createPeopleIfNeeded(self, event_data):
		'''If the people in the event do not exist, they need to be created.
		   In the case of a purchase, there is one person id to verify. If that person does not exist, you must create it.'''
		ev_type = event_data['event_type']
		if ev_type == 'purchase':
			blokeID = event_data['id']
			#print('the blokeID is {}'.format(blokeID))
			blokeExists = Person.personWithIDexists(blokeID)
			#print('blokeExists: {}'.format(blokeExists))
			if blokeExists == False:
				Person.createPerson(blokeID)
				#print('created bloke with ID {}'.format(blokeID))

		'''For befriending and unfriending events, both people must be checked to see if they exist'''
		'''REFACTOR this code when you get a chance'''
		if ev_type == 'befriend' or ev_type == 'unfriend':
			#print('CHECKING BEFRIEND / UNFRIEND')
			blokeID1 = event_data['id1']
			blokeID2 = event_data['id2']
			#print('the blokes involved are {} and {}'.format(blokeID1, blokeID2))
			blokeExists = Person.personWithIDexists(blokeID1)
			if blokeExists == False:
				#print('need to create first bloke')
				Person.createPerson(blokeID1)
				blokeExists = Person.personWithIDexists(blokeID1)
				#print('blokeExists: {}'.format(blokeExists))

			blokeExists = Person.personWithIDexists(blokeID2)
			if blokeExists == False:
				#print('need to create second bloke')
				Person.createPerson(blokeID2)
				blokeExists = Person.personWithIDexists(blokeID2)
				#print('blokeExists: {}'.format(blokeExists))

	# Used mainly to write out flagged data.
	# REFACTORED: input file and output file be made EventHandler attributes (DONE).
	def writeData(self, write_path, data_to_write):
		if os.path.exists(write_path):
			append_type = 'a' # append because it exists
		else:
			append_type = 'w' # make a new file

		print('\nDuring writeData relative write destination is:\n\t{}\n'.format(write_path))
		print('and the absolute write destination is\n\t{}\n'.format(os.path.abspath(write_path)))


		with open(write_path, append_type) as f_out:
			# print(f_out)
			# print('file path is absolute? {}'.format(os.path.isabs(write_path))) # this shows it is a relative path
			j_data = json.dumps(data_to_write)
			j_data = j_data + '\n'
			# print(type(j_data))
			print('data being written is:\n {}'.format(j_data))
			f_out.write(j_data)

	# Used to save purchase information when processing the batch_log
	def savePurchase(self, data):
		# print('PURCHASE EVENT')
		buyerID = data['id'] # strictly for readability
		purchaseAmt = float(data['amount'])
		buyer = Person.getPerson(buyerID)
		Purchase(buyerID, data['amount'], data['timestamp'])

	# This is the heart of the program for finding data to flag.
	# If there is a network of friends, a test is done to find average amt
	# of purchases by that network going back X transactions. Std-dev is then
	# found (population version (pstdev), not sample version), and if
	# the transaction is 3 SDs greater than the mean, then it is flagged for
	# writing to the flagged log.
	def handlePurchase(self, data):
		# print('PURCHASE EVENT')
		# print(Person.people)
		buyerID = data['id'] # strictly for readability
		purchaseAmt = float(data['amount'])
		buyer = Person.getPerson(buyerID)
		network_deg = EventHandler.degree
		network = buyer.localNetworkOfFriends(network_deg, set()) # pass in empty set as seed for recursive function
		# REFACTOR: you should make sure that the recursive function is a tail function so stacks don't consume too much memory
		# print('network_deg = {}'.format(network_deg))
		# print('{} has a social network of: {}'.format(buyerID, describeNetwork(network)))
		if network == set(): # i.e. if the network is empty
			# print('No network so cannot evaluate purchases.')
			# print('Just record transaction.')
			Purchase(buyerID, data['amount'], data['timestamp'])
			# print(Purchase.transactions)
		else:
			# print('Network exists, so need to see if sufficient purchase history to find anomaly.')
			# print(Purchase.transactions)
			network_as_list = []
			for friend in network:
				network_as_list.append(friend.ID)
				# print(friend.ID)
			# print(network_as_list)
			trans_count = EventHandler.consec_purchase_count
			# print(trans_count)
			relevant_transactions = Purchase.mostRecentNetworkTransactionsWithCount(trans_count, network_as_list)
			if len(relevant_transactions) >= 2: # you need at least two transactions
				mean = round(sum(relevant_transactions)/len(relevant_transactions), 2)
				# print('average is {}'.format(mean))
				stdev = round(pstdev(relevant_transactions), 2)
				# print('stddev is {}'.format(stdev))
				# print('purchase amt is {}'.format(purchaseAmt))
				if purchaseAmt > mean + 3 * stdev:
					# print('Flag the transaction!!!')
					flagged_transaction = data
					flagged_transaction['mean'] = str(mean) # the sample data uses strings, not numbers
					flagged_transaction['sd'] = str(stdev) # the sample data uses strings
					# print(flagged_transaction)
					print('Within handle data, when about to write, destination is\n\t{}\n'.format(self.flagged_path))
					print('and the absolute write destination is \n\t{}\n'.format(os.path.abspath(self.flagged_path)))
					self.writeData(self.flagged_path, flagged_transaction)
				else:
					#print('Transaction {} not big enough to flag.'.format(purchaseAmt))
					pass

	def createFrienship(self, data):
		# print(Person.people)
		firstID = data['id1']
		firstPerson = Person.getPerson(firstID)
		secondID = data['id2']
		secondPerson = Person.getPerson(secondID)
		firstPerson.addFriend(secondPerson) # addFriend() is bidirectional, so you don't need to reverse

	# data contains two people identified as id1 and id2, 
	def dissolveFriendship(self, data):
		firstID = data['id1']
		firstPerson = Person.getPerson(firstID)
		secondID = data['id2']
		secondPerson = Person.getPerson(secondID)
		firstPerson.removeFriend(secondPerson) # removeFriend() is bidirectional, so you don't need to reverse

	'''stream data is handled almost the same way as batch data except for a few small differences
	(1) the degree (D) and transaction count (T) variables do not need to be read
	(2) batch data may not need to flag transactions, but stream data does'''
	def processStreamData(self):
		print('\nProcessing stream data...')
		with open(self.stream_path, 'r') as f:
			print('During stream processing relative stream file location is\n\t{}\n'.format(self.stream_path))
			print('and the absolute stream file location is\n\t{}\n'.format(os.path.abspath(self.stream_path)))

			datalines = f.readlines()

			for line in datalines:
				data = json.loads(line)
				self.createPeopleIfNeeded(data)

				if data['event_type'] == "purchase":
					self.handlePurchase(data)

				elif data['event_type'] == "befriend":
					self.createFrienship(data)

				elif data['event_type'] == "unfriend":
					self.dissolveFriendship(data)

				else:
					print('UNRECOGNIZED EVENT')


