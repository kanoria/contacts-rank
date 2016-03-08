#contacts-rank
#Rishav Kanoria

import sys
import json
import editdistance
import unittest
from pprint import pprint


def contacts_rank(search_term, contacts):

    """Accepts a search term and contacts and returns a list of contacts that contain the search term. 
    This list is ordered by a mix of priority based on whether any of the contact's fields begin with the search term
    and Levenshtein's Distance algorithm. The highest priority is for when the name field begins with the search term,
    then the nickname, followed by the email address field. If there are multiple matches that satisfy a certain priority level
    then those are sorted alphabetically, and then by that contact's distance value. For contacts that do not have a field that
    begins with the search term I use the distance value to rank the results. A system error will be raised if there are no matches"""
    
    matches = []

    #looping through each contact in the list of contacts supplied
    for contact in contacts:

        #setting the default priority level to the lowest
        #(this means the contact does not have a field that begins with the search term)
        priority = 4
        #setting the minimum distance to an arbitrary high value
        min_dist = 9999
        #flag to check if the contact has already been appended to the list of matches to avoid duplication
        appended = False

        #looping through each field in the selected contact
        for key in contact:
            #compare the search term and the value in the contact's selected field
            if search_term.lower() in contact[key].lower():
                #assigning priority levels to the contact based on if the value of various fields in the contact begins with the search term
                if contact[key].lower().startswith(search_term.lower()):
                    if key == 'name':
                        priority = 1
                    elif key == 'nickname' and priority>2:
                        priority = 2
                    elif key == 'email' and priority>3:
                        priority = 3
                #calculate the distance between the search term and the value in the contact's selected field
                distance = editdistance.eval(contact[key].lower(), search_term.lower()) 
                #check if the distance calculated above is lower than that of any field 
                #so that we retain the lowest distance across all fields of the contact
                if distance < min_dist: 
                    min_dist = distance
                #check if the selected contact has already been saved to the list of matches to avoid duplicates
                if not appended:
                    #saving the contact to a list of matches. The fourth element in this is the value used to rank
                    #items of the same priority and is populated below
                    matches.append([dict(contact), priority, min_dist, ''])
                    appended = True
        #overwrite the distance between the search term and the contact to 
        #save the lowest distance calculated after cycling through the various fields
        if min_dist != 9999:
            matches[len(matches)-1] = [dict(contact), priority, min_dist, '']

    #raise an error if no entries are found
    if matches == []:
        raise SystemExit('No entries found')

    #here we add the sorting logic so as to be able to use the automated sort
    for match in matches:
        #if priority 1 (i.e. the name field begins with the search term) we rank alphabetically
        if match[1] == 1:
            match[3] = match[0]['name']
        #if priority 2 (i.e. the nickname field begins with the search term) we rank alphabetically
        elif match[1] == 2:
            match[3] = match[0]['nickname']
        #if priority 3 (i.e. the email field begins with the search term) we rank alphabetically
        elif match[1] == 3:
            match[3] = match[0]['email']
        #else we rank by distance
        else:
            match[3] = match[2]

    #sort the list of matches by priority, by assigned sorting logic for items of
    #the same priority, and by distance if items still have the same rank
    matches.sort(key=lambda data:(data[1], data[3], data[2]))

    return matches

def main(search_term):
    contacts = ""
    #load the supplied contacts.json file
    with open('contacts.json') as contacts_file:
        contacts = json.load(contacts_file)

    #convert the search term to unicode to accept special characters
    search_term = search_term.decode('utf-8')

    #call contacts_rank to receive contacts that match the search term accepted from the user
    matches = contacts_rank(search_term, contacts)

    #loop through selected matches to extract just the contact info and ignore the ranking logic
    matching_contacts = [match[0] for match in matches]
    pprint(matching_contacts)
    
    return matching_contacts


class RunTests(unittest.TestCase):

    def test_lowercase(self):
        self.assertEqual(main('@yahoo'), [{u'name': u'Jenny J', u'email': u'jj@Yahoo.com'}])

    def test_uppercase(self):
        self.assertEqual(main('@YAHOO'), [{u'name': u'Jenny J', u'email': u'jj@Yahoo.com'}])

    def test_no_matches(self):
        with self.assertRaises(SystemExit):
            main('abcdefgh')


if __name__ == "__main__":
    #uncomment the following two lines to run unit tests
    #test_suite = unittest.TestLoader().loadTestsFromTestCase(RunTests)
    #unittest.TextTestRunner().run(test_suite)
    if len(sys.argv)>1:
        main(sys.argv[1])
    else:
        #raise an error if the user does not enter a search term
        raise SystemExit('Search term required')
