#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Evan Malina, 2021-Nov-21, Updated file to add, delete, write CD data 
# Evan Malina, 2021-Nov-28, Updated for error handling and binary
#------------------------------------------#

import pickle # pickle used for writing/reading binary

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
# updated strFileName to binary on 11/28/2021
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    # TODOne add functions for processing here
    """Functions I added for processing CD data into a table"""
    @staticmethod
    def input_CD(strNum, strCDTitle, str_Artist, table):
        """Function to add inputs into table
        
        Args:
            strNum (string): First input is the ID number
            strCDTitle (string): Second input is album Title
            str_Artist (string): 3rd input is album artist (TYPO)
            table (list): current inventory list of dictionaries
            
        Returns:
            table (list): a list of dictionaries of CD entries 
        """
        # intID = int(strNum) #convert string to integer
        dicRow = {'ID': strNum, 'Title': strCDTitle, 'Artist': str_Artist}
        table.append(dicRow)
        return table
    
    @staticmethod
    def delete_CD(delNum, table):
        """Function to find and delete a specific ID from inventory
        Args:
            delNum (int): ID to delete from inventory
            table (list): cd inventory table
            
        Returns:
            table (list): cd inventory table
    
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == delNum:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        return table

               
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            objFile = open(file_name, 'rb')
            table = pickle.load(objFile)
            # print(table)
            objFile.close()
            return table
        except FileNotFoundError as e:
            print('File not found')
            print('Built in error info: ')
            print(type(e), e, e.__doc__, sep='\n')
            table = []
            return table            
 

    @staticmethod
    def write_file(file_name, table):
        # TODone Add code here
        """Function to save the CD to file
        Args:
            file_name (str): file name for saving
            table (list): current inventory of CDs.  A list of dictionaries
        
        Returns: none
        """
        
        objFile = open(file_name, 'wb')
        # print(table)
        pickle.dump(table, objFile)
        objFile.close()
                
# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    # TODone add I/O functions as needed
    @staticmethod
    def add_data():
        """requests user to input new CD information
        
        Args: none
            
        Returns: tuple of 3;
        var1 (int): ID number
        var2 (str): CD title
        var3 (str): CD artist
        """
        print('Please enter a new CD ID, Title and Artist')
        while True:
            try:
                var1 = int(input('Enter ID: ').strip())
                break
            except ValueError as e:
                print('That is not an integer.  Please input an integer...')
                print('Built in error info: ')
                print(type(e), e, e.__doc__, sep='\n')
                                
        var2 = input('What is the CD\'s title? ').strip()
        var3 = input('What is the Artist\'s name? ').strip()
        return(var1, var2, var3)


    
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            print(lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # TODOne move IO code into function
        strID, strTitle, stArtist = IO.add_data()
        # 3.3.2 Add item to the table
        # TODOne move processing code into function
        DataProcessor.input_CD(strID, strTitle, stArtist, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except ValueError as e: 
                print('That is not an integer. Please input an integer')
                print('Built in error info: ')
                print(type(e), e, e.__doc__, sep='\n')
        # 3.5.2 search thru table and delete CD
        # TODone move processing code into function
        DataProcessor.delete_CD(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODO move processing code into function
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            ('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




