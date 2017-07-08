QUICK NOTES

### About the test: sometimes passes, sometimes fails.
For some reason, my program sometims pass the test and sometimes doesn't. I cannot figure out why.
It works fine if you simply run run.sh, but the problem seems to start when running run_tests.sh.
Writing to flagged_purchases.json works fine at the higher level directory, but when run_tests.sh
creates temporary and other tests, sometimes writing works and sometimes it doesn't. I have not figured
out what is doing this.

Even if I am not accepted into this becauses run_tests won't pass, I would love a pointer on what
is causing these erratic results.


APPROACH

The approach used to solve this challenge problem is quite simple.
I used Python out of expedience, not because it would be the fastest way
to execute the problem, but simply because it's the fastest language for me
to prototype a solution.

There are three main classes in this application: EventHandler, Person, and Purchase.

Most of the heavy lifting is done by a class 'EventHandler'
which was initially intended as a singleton until I realized Python does not handle singletons
as easily as Objective-C. (I'd never tried it before in Python.) The EventHandler
reads in files and processes data. In the case of batch data, it stores the key
'degree' (D) and 'transaction count' (T) values in class variables. Processing by 
the EventHandler instance is done in two batches using the methods:

- processBatchData
- processStreamData

The batch data method determines the event type and either creates friendships, dissolves
friendships, or handles purchases. Newly identified people are created as needed using
the Person class (see below). Purchases are created using the Purchase class (see below),
and their data is stored in a Purchase class variable.

The stream data method likewise devides handling by event type (handling purchases, 
creating friendships, or dissolving friendships), but takes the extra step of looking at each
purchase, determining who was involved, determining whether that person has a network of friends,
and then determining the mean of purchases by people in the network, the std. dev. of those
purchases, and flagging (and storing) any purchases that are mean + 3 * SD.

The Person class is used to track people. The person class has three fields
- ID (the ID number of the person, stored as an int)
- friends (stored as a set so as to prevent duplicates)
- purchases (not strictly necessary and would be removed if I had time to refactor)

The Person class also has a class variable 'people' (stored as a list)

Important methods in the Person class include
- addFriend, which operates bidirectionally so if you add B to A, A is also B's friend.
- removedFriend, which is also bidirectional
- localNetworkOfFriends, which determines the network in accordance with the 'degree' specified

I added a couple of class methods .. getPerson (by ID) and createPerson (with ID) .. for convenience
when processing data in the event handler. Looking back, the latter could be substituted with the
__init__method, though createPerson seemed useful at the time. Would refactor if I had more time.

I should mention that the localNetworkOfFriends methods employs a recursive function to identify
the friendship network. If networks got really large, I might refactor to ensure that it is a tail
recursive function to prevent stack frames from loading up. However, I didn't seem to have a problem,
so I didn't bother changing it. It seems to work fine.

Finally, the Purchase class is used to store purchases. Each purchase is stored in a class variable
'transactions' (for which I used a list). I assumed that data was coming in reverse
chronological order. And since all the data in both the sample batch and sample event data seemed
to have the same time stamp, I didn't bother doing much with time, lacking specificity on how it
would be presented. This assumption made it easier to get the 'last X transactions in a network',
(simply reverse the list of transactions by people in the network, and take the last 50)
though obviously if transactions were not in any order, I would have to rework that part of the program.

THINGS THAT NEED TO BE CLEANED UP / REFACTORED
(1) I'm so used to Objective-C that I frequently use camel case instead of underscores. Many variables
 and attributes should be converted to Python style.

(2) If purchase events were going to come in a certain order (chronological or reverse chronological),
 I might have to adjust the way transactions were read off of the list.

(3) If there were no order to transactions, then the transaction list would have to be sorted.

(4) Currently, all of the people are stored in memory (the class variable Person.people) and
all of the transactions are also stored in memory (Purchase.transactions). With big data, this is
madness, esp. in the case of transactions. To fix this, during the batch data processing step,
batch data records that have been converted to Purchase objects should be stored in a file for later use.
Then, whenever you had to process stream data, you could read in the file. Also, if there were a smaller
limit on the number of relevant transactions, one could selectively import only the transactions that were
needed.

(5) The biggest problem currently is that the initial batch data takes over 10 minutes to process
on my rather old computer with only 8GB of memory. I don't have much experience with 'big data' 
so I have no idea if that is normal or not. The most obvious fix would be to store the data 
directly in a file as I created each Purchase object. The event stream data was handled quite quickly
(1000 records in a second or two), so I was not otherwise worried about the overall approach.
I will try to add some kind of indication that the program is running so that the user doesn't think it is
frozen (it wasn't ... everything got processed).

HIERARCHY
log_input contains a variety of batch file sizes. It was tedious to test basic functions using
huge amounts of data

my favorite editor (Atom) broke (others having similar problem) so I experimented with others and
settled on Sublime





