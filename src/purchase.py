class Purchase():
	transactions = [] 
	# a record of all transactions, may want to purge occasionally
	# to purge, you can decide on how many purchases to remove from
	# the front of the list
	# NOTE: if transactions are not streamed in chronological order (most recent last)
	# then you will have to sort transactions; I have assumed they are in order by timestamp

	@classmethod
	def mostRecentPurchasesWithCount(self, count):
		return Purchase.transactions[-count:]

	# Used for initial testing, not used in the current application.
	@classmethod
	def meanOfRecentPurchasesWithCount(self, count):
		transactions_to_tally = Purchase.mostRecentPurchasesWithCount(count)
		sum = 0
		num_trans = len(transactions_to_tally)
		for trans in transactions_to_tally:
			sum += trans.amount
			# print('this amount is {}'.format(trans.amount))
		# print('sum is {}'.format(sum))
		average = sum / num_trans
		# print('avg is {}'.format(average))

	# For the network description, rather than passing a "heavy" list of person objects,
	# we simply pass in a list of ID numbers
	@classmethod
	def mostRecentNetworkTransactionsWithCount(self, max_trans_count, net_people_IDs):
		recent_transactions = reversed(Purchase.transactions)
		in_network_transactions = [] # just storing the amounts
		# print(recent_transactions)
		# print('max trans {}'.format(max_trans_count))

		for t in recent_transactions:
			# print(t.personID, t.amount, t.timestamp)
			# print('person {} and network {}'.format(t.personID, net_people_IDs))
			if t.personID in net_people_IDs:
				# print('This transaction counts {} {}'.format(t.personID, net_people_IDs))
				in_network_transactions.append(t.amount)
				# print(len(in_network_transactions))
				if len(in_network_transactions) == max_trans_count:
					break
		return(in_network_transactions)

	def __init__(self, PID, amt, time):
		self.personID = PID
		self.amount = float(amt)
		self.timestamp = time
		Purchase.transactions.append(self) # add to the list of transactions
		# print(Purchase.transactions)


