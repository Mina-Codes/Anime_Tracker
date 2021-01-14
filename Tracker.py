import random

with open('anime_list.txt', 'r') as file: #read the text file and store the data into a list
    data_set = file.read().splitlines()
    


counter = 0
for line in data_set: #splits categories by the tab space between them into different items in a list
    new_line = line.split('\t')
    data_set[counter] = new_line #update the list
    counter+=1

for line in data_set: #checks for the anime titles that contain the number of episodes, and in order to read and compare the numbers
    #they will have to be cast into integers (always read as strings), and so the brackets are stripped and the string is separated
    if len(line) > 5:
        print(line)
        line[len(line)-1] = line[len(line)-1].strip('[').strip(']')
        line[len(line)-1] = line[len(line)-1].split(', ')
        for num in range(len(line[len(line)-1])):
            line[len(line)-1][num] = int(line[len(line)-1][num])
            


def SearchSeries(lookfor): #name of the series is passed to this function, and
    #it is examined if it exists as part of one of the titles and the position of said title is returned
    counter = 0
    for element in data_set:
        if lookfor in element[0]:
            return counter
        counter += 1
    return False

def AddEpisode(series, watched):
    position = SearchSeries(series) #SearchSeries function will return the position of the series passed in the dataset

    if len(data_set[position]) == 5: #if there is no existent category for number of episodes, then a new list will be created
        new_list = []
        if type(watched) == int: #if one number was inputted and cast into an integer, append it to the list
            new_list.append(watched)
        else:
            for episode in watched: # If it was a list, append each item from the list to the new list separately
                new_list.append(episode)
        data_set[position].append(new_list)

    elif len(data_set[position]) > 5: #if there is already category, no need for a new list, directly supplement to the existent list
        if type(watched) == int:
            data_set[position][len(data_set[position])-1].append(watched)
        else:
            for episode in watched:
                data_set[position][len(data_set[position])-1].append(episode) #placed into the last category in an anime title list 

    data_set[position][len(data_set[position])-1].sort() #sort the number of episodes from least to greatest
    CheckNumEp(data_set[position]) #


def UpdateText(): #writes whats on the data set to the text file
    with open('anime_list.txt', 'w') as file:
        for line in data_set:
            for count in range(len(line)):
                if count == len(line)-1:
                    file.write(str(line[count])) #if its the last category, cast it into a string so it can be written (in case its a list of episodes)

                else:
                    file.write(line[count] +'\t')
            file.write('\n')


def FindRate():
    for pos in range(len(data_set[0])): #finds the position of rating in the anime titles list (they're all aligned)
        if 'rating' in data_set[0][pos]:
            return pos

def NumCheck(the_list): #checks if numbers are in order
    rate = FindRate()
    counter = 0
    
    for pos in range(len(the_list)):
        if float(the_list[counter][rate]) < float(the_list[counter +1][rate]): #cast the strings into floats so they can be compared numerically,
            #as well, it compares if the second number is larger than the first, then it is not in order from greatest to least, and thus false is returned
            found = False
            return found
        else:
            found = None

        if counter < len(the_list)-2: #add counter as long as it is not larger than the length of the list
            counter +=1 
            
    return found #found will be returned as none if there is no descrepancy in the order of rating

def OrganizeRate(the_list, counter):
    start = False
    if counter == 0:
        start = True
        
    while True:
        if NumCheck(the_list) == None:
            return the_list
        else:
            max_num = 0
            rate_num = FindRate()
            for element in range(counter, len(the_list)):
                if float(the_list[element][rate_num]) > max_num:
                    max_num = float(the_list[element][rate_num])
                    pos_max = element

            the_list[pos_max], the_list[counter] = the_list[counter], the_list[pos_max]

            if counter < len(the_list)- 1:
                counter += 1

        if start:
            the_list = OrganizeRate(the_list, counter)
            counter +=1
        else:
            return the_list

def RecommendGenre(the_genre):
    recommend_list = []
    for element in data_set:
        for lookfor in element:
            if the_genre in lookfor and len(element) == 5:
                recommend_list.append(element)
    count = 0
    if len(recommend_list) == 0:
        return None
    else:
        recommend_list = OrganizeRate(recommend_list, count) #(count will be passed as a measure of conidition)organize the recommended anime according to rating
        return recommend_list[:4] #return the first 4 animes


def WatchSeries(): #checks if there are any anime titles with six categories (num of episodes is num 6) and adds it to the list of watched/watching series
    watched_list = []
    for series in range(len(data_set)):
        if len(data_set[series]) == 6:
            watched_list.append(data_set[series][0])
        else:
            pass
    return watched_list


def CheckNumEp(series):
    for episode in series[len(series)-1]:
        occur_num = series[len(series)-1].count(episode)
        if occur_num > 1:
            for delete in range(occur_num - 1):
                series[len(series)-1].remove(episode)
                    


def CheckEpisode(series):
    series_pos = SearchSeries(series)
    for category in range(len(data_set[0])):
       if 'episode' in data_set[0][category]:
           pos = category

    return int(data_set[series_pos][pos])
        
def PickupEpisode(series):
    pos = SearchSeries(series)
    
    if len(data_set[pos]) == 6:
        counter = 1
        for episodes in data_set[pos][len(data_set[pos])-1]:
        
            if episodes != counter:
                return counter
            elif episodes == len(data_set[pos][len(data_set[pos])-1]) and counter == len(data_set[pos][len(data_set[pos])-1]) and counter < CheckEpisode(series):
                return counter + 1
            elif counter == CheckEpisode(series):
                return 'Completed'
            if counter < CheckEpisode(series):
                counter += 1    
                


number = True
while number == True:
    UpdateText()
    options = ['Look for watched series', 'Add Episode to a series', 'Recommend Series based on genre', 'Pick-up where you left off', 'Help', 'Quit']
    print('\n\nHello, this program will allow you ')
    counter = 1
    for option in options: #print the options which are held in a list
        print(counter, '. ', option)
        counter += 1
    print('\n')
    user_choice = input('Which of the options would you like to explore? *enter the number* ') #ask the user for the option number he wants to use
    print('\n')

    if user_choice == '1': #if 1,
        watched_series = WatchSeries()
        counter = 1
        if len(watched_series) == 0:
            print('You have not watched any series yet.')
        for series in watched_series:
            print(counter,'. ',series, '\n')
        
    elif user_choice == '2': #if 2, 
        userinput = input('What series do you want to add to?')
        ret_series = SearchSeries(userinput.title())
        
        if type(ret_series) == bool:
            print('There is no such series')

            
        else:
            print('The series name: ', data_set[ret_series][0])
            userinput = input('Enter the episodes you have watched (please enter commas between each number): ')
            ep_list = userinput.replace(' ','').split(',')
            
            for char in range(len(ep_list)):
                if ep_list[char].isdigit() == True:
                    ep_list[char] = int(ep_list[char])
            print(ep_list, 'looooo')
            AddEpisode(data_set[ret_series][0], ep_list)
            
            
    elif user_choice == '3': #if 3, 
        user_choice = input('What genre are you looking for?')
        recomm_list = RecommendGenre(user_choice.title())
        counter = 1
        if recomm_list == None:
            print('Sorry, there is no such genre.')
        else:
            for series in recomm_list:
                print(counter, '. ' ,series[0], '\t rating: ',series[FindRate()],)
                counter += 1
            
    elif user_choice == '4':
        print('Watched Series: ')
        watched_series = WatchSeries()
        counter = 1
        
        if len(watched_series) == 0:
            print('None')

        else:
            for series in watched_series:
                print(counter,'. ',series, '\n')
                counter +=1 
            userchoice = int(input('Which of the above series do you want to continue watching?[Enter series number] '))
            ep_pick = PickupEpisode(watched_series[userchoice - 1]) #pass the name of the series to the function, and the episode to continue watching will be sent back
            print('Episode to pick up from: ', ep_pick)
    elif user_choice == '5': #help
        print('''
This program holds a database containing anime titles.
It allows the user to keep track of the episodes they have watched per series,
and continue from where they left off. As well, this program suggests for the user
anime title based on genre chosen.
            ''')

    elif user_choice == '6': #end the loop and program
        number = False
