import sqlite3
import os
#Brief: I want to be able to give it a name, address, 
#number and email to record
#Ask for one after the other, prompt to put in none if no info

#I want to back it up to the cloud + give the user that option
#I want to be able to list contacts
#Description of relationship for use if same name when changing (updating/deleting)
os.system('mode con: cols=101')

def start():
    print("{: ^101s} \n {:^101s}".format("Do you wish to query a contact(s), add a new contact, update an existing contact or delete a contact?", "Commands: 'Query', 'Add', 'Delete', 'Update', 'Complete'"))
    s = input()
    if s.lower() == "add":
        add()
    elif s.lower() == "delete":
        delete()
    elif s.lower() == "update":
        update()
    elif s.lower() == "query":
        query()
    elif s.lower() == "complete":
        return
    else:
        print("Unknown command")
        start()

def add():
    print("If unsure of details type None")
    person = []
    i = 0
    print("Name: ", end="")
    person.append(input())
    print("Address: ", end="")
    person.append(input())
    print("Phone Number: ", end="")
    person.append(input())
    print("Email Address: ", end="")
    person.append(input())
    print("Relationship: ", end="")
    person.append(input())
    for attribute in person:
        person[i] = attribute.title()
        i += 1
    try:
        cursor.execute('''INSERT INTO contacts(name, address, phone_number, email, relationship) VALUES(?,?,?,?,?)''', (person[0], person[1], person[2], person[3], person[4]))
        db.commit()
        print("\n{:-^101s}".format("Contacts updated"))
    except Exception as e:
        db.rollback()
        raise e
    finally:
        continu()

def delete():
    print("Name of contact to be deleted: ",  end="")
    deletable = input()
    deletable = deletable.title()
    i = 0
    try:
        rows = cursor.execute('''SELECT name, address, phone_number, email, relationship FROM contacts WHERE name = ?''', (deletable, )).fetchall()
        lise = longest(rows)
        thing = "No. {:{:d}s} {:{:d}s} {:{:d}s} {:{:d}s} {:{:d}s}".format("Name", lise["lname"], "Address", lise["laddress"], "Phone Number", lise["lphone_number"], "Email", lise["lemail"], "Relationship", lise["lrelationship"])
        print(thing)
        print("-" * (len(thing) - 1))
        for row in rows:
            print("{:<4}{:{:d}s} {:{:d}s} {:{:d}s} {:{:d}s} {:{:d}s}".format(i, row[0], lise["lname"], row[1], lise["laddress"], row[2], lise["lphone_number"], row[3], lise["lemail"], row[4], lise["lrelationship"]))
            i += 1
        print("Number of contact to be deleted: ", end="")
        num = input()
        num = int(num)
        print("Are you sure you want to delete {:s} from your contact list? Y/N" .format(deletable), end="")
        x = input()
        x = x.lower()
        if x == "y":
            cursor.execute('''DELETE FROM contacts WHERE name = ? AND address = ? AND phone_number = ? AND email = ? AND relationship = ?''', (rows[num][0], rows[num][1], rows[num][2], rows[num][3], rows[num][4]))
            db.commit()
            print("Contact deleted")
        elif x == "n":
            print("Contact not deleted")
    except Exception as e:
        db.rollback()
        raise e
        print("No such contact within contact list")
    finally:
        continu()

def update():
    print("Name of contact to be updated: ",  end="")
    updatable_name = input()
    updatable_name = updatable_name.title()
    #Going to be an issue when 2 people have the same name
    #ID? Date met? Description?
    print("Information to be updated: Name, Address, Number, Email, Description of Relationship", updatable_info = input())
    print("Updated Information:", updated_info = input())
    updatable_info = updatable_info.lower()
    try:
        cursor.execute('''UPDATE contacts SET ? = ? WHERE name = ?''', (updatable_info, updated_info, updatable_name))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

def query():
    print("Name of contact: ", end="")
    name = input()
    name = name.title()
    sql_query = '''SELECT name, address, phone_number, email, relationship FROM contacts WHERE name = ?'''
    sql_query_two = cursor.execute(sql_query, (name, ))
    rows = sql_query_two.fetchall()
    lise = longest(rows)
    thing = "{:{:d}s} {:{:d}s} {:{:d}s} {:{:d}s} {:{:d}s}".format("Name", lise["lname"], "Address", lise["laddress"], "Phone Number", lise["lphone_number"], "Email", lise["lemail"], "Relationship", lise["lrelationship"])
    print(thing)
    print("-" * (len(thing) - 1))
    if len(thing) - 1 > 101:
        os.system('mode con: cols=?', len(thing))
    for row in rows:
        print("{:{:d}s} {:{:d}s} {:{:d}s} {:{:d}s} {:{:d}s}".format(row[0], lise["lname"], row[1], lise["laddress"], row[2], lise["lphone_number"], row[3], lise["lemail"], row[4], lise["lrelationship"]))

def continu():
    print("Do you wish to continue? (Y/N) ", end="")
    a = input()
    if a.lower() == "y":
        start()
    elif a.lower() == "n":
        return
    else:
        print("Not a valid response")
        continu()

def longest(rows):
    lise = {}
    cursor.execute('''SELECT LENGTH(name) FROM contacts ORDER BY LENGTH(name) DESC LIMIT 1''')
    leng = cursor.fetchone()
    if leng[0] >= 4:
        lise['lname'] = leng[0] + 2
    else:
        lise['lname'] = 6
    cursor.execute('''SELECT LENGTH(address) FROM contacts ORDER BY LENGTH(address) DESC LIMIT 1''')
    leng = cursor.fetchone()
    if leng[0] >= 7:
        lise['laddress'] = leng[0] + 2
    else:
        lise['laddress'] = 9
    cursor.execute('''SELECT LENGTH(phone_number) FROM contacts ORDER BY LENGTH(phone_number) DESC LIMIT 1''')
    leng = cursor.fetchone()
    if leng[0] >= 12:
        lise['lphone_number'] = leng[0] + 2
    else:
        lise['lphone_number'] = 14
    cursor.execute('''SELECT LENGTH(email) FROM contacts ORDER BY LENGTH(email) DESC LIMIT 1''')
    leng = cursor.fetchone()
    if leng[0] >= 7:
        lise['lemail'] = leng[0] + 2
    else:
        lise['lemail'] = 9
    cursor.execute('''SELECT LENGTH(relationship) FROM contacts ORDER BY LENGTH(relationship) DESC LIMIT 1''')
    leng = cursor.fetchone()
    if leng[0] >= 12:
        lise['lrelationship'] = leng[0] + 2
    else:
        lise['lrelationship'] = 14
    return lise

try:
    db = None
    try:
        db = sqlite3.connect(r"C:\sqlite\db\pythonsqlite.db")
    except Error as e:
        print(e)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts(name TEXT, address TEXT, phone_number TEXT unique, email TEXT unique, relationship TEXT)''')
    db.commit()
except Exception as e:
    db.rollback()
    raise e


print("{:}\n{:-^101s}\n{:}\n".format(('-' * 101),"Welcome to your Command Line Contact Storage System", ('-' * 101)))
start()
db.close()
