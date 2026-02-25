import pandas
import csv
import numpy as np
import pandas as pd
print("Welcome to election analyzer.")

#read csvfile into a dataframe (had to use encoding wasn't working)

dataframe = pd.read_csv('FullDataUpdated.csv', encoding = 'latin-1')
dataframe['Full name'] = dataframe['Member first name'] + ' ' + dataframe['Member surname']
#this combines first and last name cols for option 2 later on
### This is a function that must be loaded before

# constructing party class, consisting of name, members, and votes courtesy of Peter's github
class Party:

    def __init__(self,name):
      self.name = name
      self.total_votes = 0
      self.num_mps = 0
      self.won_constituencies = []
    def add_votes(self, votes):
      self.total_votes += votes
    #adds votes to the party total
    def add_mp(self):
       self.num_mps += 1
    #adds up number of mps for a party
    def add_won_constituencies(self, constituency):
       self.won_constituencies.append(constituency)
    def __str__(self):
       return (f"Party: {self.name} , MPs: {self.num_mps}, "
               f"Votes: {self.total_votes} , Constituencies won: {len(self.won_constituencies)}")
    #records constituency won by the party

class MP:
#defining the class for members. this will encapsulate the mp data courtesy of Peter's data

  def __init__(self, name, constituency, partyname, votes):
      self.name = name
      self.constituency=constituency
      self.party = partyname
      self.votes = votes

  def __str__(self):
      return (f"MP: {self.name}, Constituency: {self.constituency}.")
  
class Constituency:
  def __init__(self, name, total_voters=0):
    self.name = name 
    self.total_voters = total_voters #total voters
    self.total_votes_cast = 0 
    self.mps = [] #the list of mp candidates
    
  def add_mp(self,mp):
    self.mps.append(mp)
    self.total_votes_cast += mp.votes
#using append to add a vote to mp
  
  def __str__(self): #returns summary of the constituency
      mp_summary = "\n  ".join([str(mp) for mp in self.mps])
      turnout = (self.total_votes_cast / self.total_voters * 100) if self.total_voters else 0

      return (f"Constituency: {self.name}\n"
            f"Total votes for this constituency: {self.total_votes_cast} ({turnout:.2f}% turnout)\n"
            f"MPs: {mp_summary}") # line above includes the voter turnout as percentage.

#fix menu and allow for submenus

def display_menu():
    #loop to display menu
    print("1. Party information") #make percentage of party votes another option here
    print("2. MPs Information")
    print("3. Constituency Information")
    print("4. Statistical Data")
    print("5. Exit program.")

def display_submenu():
   print('1. Find gender percentage by party:')
   print('2. Find gender percentage by Constituency:')
   print('3. Exit')

def menu():
   print("\nWelcome to Election analysis menu")
   while True:
    display_menu()
    try:
      selection = input("Enter your choice in the menu:").strip
    
      if selection == '1':
        option_one()
      elif selection == '2':
        option_two()
      elif selection == '3':
        option_three()
      elif selection == '4':
        option_four()               
      elif selection == '5':
        print('Exiting.')
        break
      else:
        raise ValueError("Invalid option selected.")
    except ValueError as e:
       print(f'Error: {e}.')
#try except case added for further error handling
    choice2 = input('\nDo you want to continue? Enter Y to continue, or any value to exit. ').lower()

    if choice2 == 'y':
       pass
    else:
       print('Exiting.')
       break #this allows code to break if the user is done instead of looping the menu
    #courtesy of lab tutor Apejoye

#submenu options begin here.

#for fourth option choices
# party
def option4party():
  partyname = input("enter party name:")
  partydata = dataframe[dataframe["First party"] == partyname]
  if not partydata.empty: #.empty seeing if there is any information in that column
    print(f"Gender dist. for '{partyname}': ") #Percentage dist.
    print(gender1percentage(partydata))
  else:
    print(f"No data found.")

def option4con():
  constituencyname = input("Enter constituency name:")
  constituencydata = dataframe[dataframe['Constituency name'] == constituencyname]
  if not constituencydata.empty:
    print (f"Gender of the '{constituencyname}' MP:") #shows gender of mp as a percent,100.
    print(gender1percentage(constituencydata))
  else:
   print(f'No data found.')



#options will begin here.
def option_one():
  party_name = input("Enter the party name (i.e. Lab, Con, LD):")
  partylist = dataframe[dataframe['First party'] == party_name]
  if not partylist.empty:
          total_votes = partylist['Valid votes'].sum()
          seats_won = partylist['Constituency name'].nunique()
          print(f"Party: {party_name}\nTotal Votes: {total_votes}\nSeats Won: {seats_won}")
  else:
          print("invalid option selected!")


#second option in menu.
def option_two(): #explain values[0]??
  mpname = input("Enter the MP's full name:")
  mplist = dataframe[dataframe['Full name'] == mpname]
  if not mplist.empty:
    party = mplist['First party'].values[0]
    constituency = mplist['Constituency name'].values[0]
    votes = mplist['Valid votes'].values[0]
    print(f"MP: {mpname} \nParty: {party} \nConstituency: {constituency}\nVotes: {votes}")
  else:
    print("Invalid option selected!")


#third option in menu.
def option_three():
  seatname = input("Enter the constituency name:")
  seatlist = dataframe[dataframe['Constituency name'] == seatname]
  if not seatlist.empty:
    constituency = Constituency(seatname, total_voters = seatlist['Electorate'].max()) #max returns largest item
    for _, row in seatlist.iterrows():
      constituency.add_mp(MP(row['Full name'], seatname, row['First party'], row['Valid votes']))
    print(constituency)
  else:
    print("Invalid option selected.")


#fourth option contained subsets/choices user makes
def option_four():
   while True:
      display_submenu()
      selection = input('Enter your choice:')
      if selection == '1':
         option4party()
      elif selection == '2':
         option4con()
      elif selection == '3':
         print('Returning to menu.')
         break
      else:
         print('Invalid option selected.')
#helper function.
def gender1percentage(subset):
  total_voters = len(subset) #length as a string in this subset
  if total_voters == 0:
    return "No data."
  gendercount = subset['Member gender'].value_counts(normalize=True) * 100
  percentages = {gender: round(percentage, 2) for gender, percentage in gendercount.items()}

  percentage_result = "\n".join([f"{gender}: {percentage}%" for gender, percentage in percentages.items()])
  return percentage_result

if __name__ == '__main__':
    menu()
#had to use stackexchange to figure out how to execute menu
