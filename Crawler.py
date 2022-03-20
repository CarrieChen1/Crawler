from sys import stderr
    #This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
    #'Stderr: Standard error – The user program writes error information to this file-handle. Errors are returned via the Standard error" (stderr)
    #sys.stderr is similar to sys.stdout because it also prints directly to the Console. But the difference is that it only prints Exceptions and Error messages. (Which is why it is called Standard Error).
from math import log10
    #Python number method log10() returns base-10 logarithm of x for x > 0.
import os
    #This module provides a portable way of using operating system dependent functionality.
import requests
    #Requests is an HTTP library written in Python, based on urllib and using the Apache2 Licensed open source protocol, which is more convenient than urllib.
from bs4 import BeautifulSoup
    #BeautifulSoup is a library of python whose main content is to grab data from web pages
from actors_graph import ActorsGraph
from movie import Movie
    #"actors_graph" and "movie" are the name of another two python files written by the author

DEFAULT_MAX_MOVIE_COUNT = 10
DEFAULT_MAX_UNAVAILABLE_COUNT = 20
DEFAULT_RATING_FOLDER = 'Rating/'
    #assign value to the above 3 words,
    # maximum movie numbers:10
    # maximum unavailable number: 20
    # the directory that contains the file of the rating of the movie : Rating/

#Note: in the following lines: "attributes" would be used to describe the "properties" of the class variable
    # while the word "method" means the functions created for the class variable

#create a class variable,used to describe a collection of objects with the same properties and methods.
class Crawler(object):
    main_url = 'https://www.imdb.com/title/'
        #the website where we would like to get data
    rating_url_ending = 'ratings?ref_=tt_ov_rt'
        #the ending of the url

#define the struture of the class variable
    def __init__(self, movies_list_path,
                 max_movie_count=DEFAULT_MAX_MOVIE_COUNT,
                 max_unavailable_count=DEFAULT_MAX_UNAVAILABLE_COUNT,
                 rating_folder=DEFAULT_RATING_FOLDER):
        # Define the structure of the class variable. Because an instance variable is best defined directly in the __init__ method.
        self.movies_list_path = movies_list_path
        self.max_movie_count = max_movie_count
        self.max_unavailable_count = max_unavailable_count
        self.rating_folder = rating_folder
        self.create_project_dir(self.rating_folder)

        self.max_diff_movie = ''
        self.max_diff = 0
        # the previous lines(from 33 to 40) defines the 'attributes' of the class variables "Crawler"

#create a method for the class variable- create a project directory
    def create_project_dir(self, directory):
        if not os.path.exists(directory):
            print('Creating Project Folder' + directory)
            os.makedirs(directory)
            #os.path.exist:
            #The os.path module is mainly used to obtain the attributes of files, and exists means "exist",
            # so as the name suggests, os.path.exists() means to judge whether the file in parentheses exists,
            # and the parentheses can be the file path.

            #os.makedirs(name, mode=0o777, exist_ok=False)
            #effect: Used to create a multi-layer directory(while using os.mkdir for a single layer

#create a new method for the class variable: get the content of the web page
    def get_page_content(self, url):
        r = requests.get(url)
        # use the request module for simulating the action of asking for the website permission to get data (the website is defined as url in previous line)
        if not r.status_code == 200:
            raise RuntimeError('Problem accessing page data.')
        return r.text
        #if the status_code of the data is not 200,return the text string format of the requested data

#create a new method for the class variable: to get the name of the movie
    def get_movie_name(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        #use BeautifulSoup method to get the data and analyze them.
        all_h1 = soup.find_all('h1')
        #use beautifulsoup to find out all movie name which contains"h1"

        #figure out the "title"
        title = [x for x in all_h1 if 'itemprop="name"' in str(x)]
        #analyze within the titles if the text caught by Beautifulsoup in "all_h1" has a string which item properties is equal to name
        # if the length of the title is equal to 0, the title = the id which equals to the Title Year
        if len(title) == 0:
            title = [x for x in all_h1 if 'id="titleYear"' in str(x)]
            # if the number of words in the string is equal to 0, the title = the id which equals to the Title Year
            #  if the number of words in the string obtained from the above cell (cell 86) is still = 0, the title is defined to be the first word in "title_wrapper"
            if len(title) == 0:
                all_div = soup.find_all('div')
                title = [x for x in all_div if 'class="title_wrapper"' in str(x)]
                title = title[0].find_all('h1')[0].text
            # if the number of words in the string obtained from the previous cell(cell 86) is still not equal to 0,
            # the title is defined as the word in the split of "title" between "<" and ">"
            else:
                title = str(title[0]).split('>')[1].split('<')[0]
        # if the length of the title is not equal to 0, the title = the title is defined as the word in the split of "title" between "<" and ">"
        else:
            title = str(title[0]).split('>')[1].split('<')[0]
        print('Title: ' + title)
        return title
    #print the name of the movie

# create a new method for the class variable: to get the name of the movie director
    #the same method, and similar step as the way to get the title of the movie
    def get_director_name(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        all_spans = soup.find_all('span')
        director = [x for x in all_spans if 'itemprop="director"' in str(x)]
        if len(director) == 0:
            all_as = soup.find_all('a')
            director = [x for x in all_as if ('href="/name/nm' in str(x))]
            # print('director:' + director[2].text)
            if len(director) >= 3:
                director = director[2].text
            else:
                return ''
        else:
            director = str(director[0]).split('>')[-4].split('<')[0]
        return director

# create a new method for the class variable: to change the representation of the movie websites
    def change_movie_url(self, number, prefix):
        return prefix + max([6 - int(log10(number)), 0]) * '0' + str(number)

# create a new method for the class variable: to save the previously obtained results in a file in our computer
    def write_results_to_file(self, item):
        with open(self.movies_list_path, 'a') as f:
            f.write(str(item))

# create a new method for the class variable: to save the previously obtained results in a file in our computer
    def write_rating_results_to_file(self, item):
        filename = item.title + '.txt'
        with open(self.rating_folder + filename, 'a') as f:
            f.write(item.get_rating())

# create a new method for the class variable: to get the name of the movie actors
    #  the same method, and similar steps as the procedure of obtaining the "title of the movie"
    def get_movie_actors(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        all_tds = soup.find_all('td')
        cast_tds = [x for x in all_tds if 'itemprop="actor"' in str(x)]
        if len(cast_tds) == 0:
            cast_names = []
            tables = soup.find_all('table')
            cast_table = [x for x in tables if 'class="cast_list"' in str(x)]
            if len(cast_table) == 0:
                return []
            all_trs = cast_table[0].find_all('tr')
            for tr in all_trs[1:]:
                all_tds = tr.find_all('td')
                if len(all_tds) < 2:
                    continue
                all_as = all_tds[1].find_all('a')
                name = all_as[0].text
                name = name.replace(' ', '')
                name = name.replace('\n', '')
                cast_names.append(name)
        else:
            cast_span = [x.find_all('span') for x in cast_tds]
            cast_names = []
            for item in cast_span:
                for nestedItem in item:
                    cast_names.append(nestedItem.text)
        return cast_names

# create a new method for the class variable: to get the rating percentage of the movies
# the same method, and similar step as the procedure to get the "title of the movie"
    def get_rating_percentages(self, table_content):
        result = []
        all_tds = table_content.find_all('td')
        count = 0
        for td in all_tds:
            count += 1
            divs = td.find_all('div')
            if len(divs) >= 2:
                percentage = divs[1].text
            else:
                percentage = '-'
            if count % 3 == 2:
                percentage = percentage.replace(' ', '')
                percentage = percentage.replace('\n', '')
                percentage = percentage.replace('\xa0', '')
                percentage = percentage.replace('%', '')
                result.append(percentage)
        return result

# create a new method for the class variable: to get the rating percentage of the movies by demographic
# the same method, and similar step as the procedure to get the "title of the movie"
    def get_rating_by_demographic(self, table_content):
        # [[all], [males], [females]]
        # all , <18, 18-29, 30-44, 45+
        result = []
        all_trs = table_content.find_all('tr')
        for tr in all_trs[1:]:
            result.append([])
            all_tds = tr.find_all('td')
            for td in all_tds[1:]:
                divs = td.find_all('div')
                rating = divs[0].text
                result[-1].append(rating)
        return result[0][0], result

# create a new method for the class variable: to get the US & "non US" rating percentage by demographic
# the same method, and similar step as the procedure to get the "title of the movie"
    def get_us_non_us_rating(self, table_content):
        result = []
        vote_count = []
        all_tds = table_content.find_all('td')
        for td in all_tds:
            divs = td.find_all('div')
            if len(divs) >= 2:
                count = divs[1].text
                count = count.replace(' ', '')
                count = count.replace('\n', '')
            else:
                count = '-'
            vote_count.append(count)
            result.append(divs[0].text)
        return result[1], vote_count[1], result[2], vote_count[2]

# create a new method for the class variable: to get the rating percentage of the movies
# the same method, and similar step as the procedure to get the "title of the movie"
    def get_rating_information(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        all_tables = soup.find_all('table')
        rating_percentages = self.get_rating_percentages(all_tables[0])
        general_rating, rating_by_demographic = self.get_rating_by_demographic(all_tables[1])
        us_rating, us_votes, non_us_rating, non_us_votes = self.get_us_non_us_rating(all_tables[2])
        result = {'rating': general_rating, 'percentages': rating_percentages, 'demographic': rating_by_demographic,
                  'us': us_rating, 'non-us': non_us_rating}
        if us_votes > '300' and non_us_votes > '300' and not us_rating == '-' and not non_us_rating == '-':
            return result, 1
        return result, 0

# create a new method for the class variable: to summarize the rating information of the movies
    def all_rating_information(self, number):
        url = self.main_url + 'tt' + max([6 - int(log10(number)), 0]) * '0' + str(number) + '/' + self.rating_url_ending
        content = self.get_page_content(url)
        if 'No Ratings Available' in str(content) or content == -1:
            return {'rating': '-', 'percentages': '-', 'demographic': ['-', '-', '-'], 'us': '-', 'non-us': '-'}, 0
        # if no information contains, return "-"
        return self.get_rating_information(content)
        # if information contains, print it out

# create a new method for the class variable: to check the max_difference
    def check_if_max_diff(self, us, non_us, title):
        if abs(float(us) - float(non_us)) > self.max_diff:
        # check if the absolute value of the subtraction between US and non-US is large then max_difference
            self.max_diff = abs(float(us) - float(non_us))
            self.max_diff_movie = title

# create a new method for the class variable: crawl the website
    def crawl_the_website(self):
        movies = []
        count = 0
        actors_graph = ActorsGraph()
        count_not_found = 0

        #use "while" function to count the number of movies and unavailable ones
        while count < self.max_movie_count and count_not_found < self.max_unavailable_count:
            count += 1
            this_movie_url = self.change_movie_url(count, 'tt')
            print('Crawling... ' + str(count) + ' ... ' + this_movie_url, file=stderr)
           #try...except function is used when the cells below "try" not works, it will sequentially run the cells below "except"
            try:
                content = self.get_page_content(self.main_url + this_movie_url + '/')
                count_not_found = 0
                title = self.get_movie_name(content)
                director = self.get_director_name(content)
                actors = self.get_movie_actors(content)
                rating_information, consider_for_max_diff = self.all_rating_information(count)
                if consider_for_max_diff == 1:
                    self.check_if_max_diff(rating_information['us'], rating_information['non-us'], title)
                actors_graph.add_edges(actors)
                movies.append(Movie(title, director, actors, rating_information))
                self.write_results_to_file(movies[-1])
                self.write_rating_results_to_file(movies[-1])
            except RuntimeError as e:
                print(e, file=stderr)
                count_not_found += 1
        print('Movie with max us, non-us diff is: ' + self.max_diff_movie)
        return movies, actors_graph
    # find out the movie which has the maximum difference between US and Non-US voting, and print the information of it out
        # the information printed out includes the title, director, actors, rating_information and actors graph