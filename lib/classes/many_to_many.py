# article.py
class Article:
    all = []  # Single source of truth for all articles
    
    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise Exception("Title must be a string between 5 and 50 characters")
        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        # Title is immutable. Ignore any assignment.
        pass

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        if not isinstance(new_author, Author):
            raise Exception("author must be an instance of Author")
        self._author = new_author

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        if not isinstance(new_magazine, Magazine):
            raise Exception("magazine must be an instance of Magazine")
        self._magazine = new_magazine


# author.py

class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise Exception("Name must be a non-empty string")
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        pass

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        articles = self.articles()
        if not articles:
            return None
        return list({article.magazine.category for article in articles})


# magazine.py

class Magazine:
    all_magazines = []
    
    def __init__(self, name, category):
        self._name = name
        self._category = category
        Magazine.all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        # Only update if new_name is a string and between 2 and 16 characters, inclusive.
        if isinstance(new_name, str) and (2 <= len(new_name) <= 16):
            self._name = new_name
        # Otherwise, ignore the assignment.

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        # Only update if new_category is a non-empty string.
        if isinstance(new_category, str) and len(new_category) > 0:
            self._category = new_category
        # Otherwise, ignore the assignment.

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        # Return a unique list of authors who have written for this magazine.
        return list({article.author for article in self.articles()})

    def article_titles(self):
        article_list = self.articles()
        if not article_list:
            return None
        return [article.title for article in article_list]

    def contributing_authors(self):
        articles = self.articles()
        if not articles:
            return None
        
        author_count = {}
        for article in articles:
            author = article.author
            author_count[author] = author_count.get(author, 0) + 1
        
        # Return authors with more than 2 articles; if none, return None.
        authors = [author for author, count in author_count.items() if count > 2]
        return authors if authors else None

    @classmethod
    def top_publisher(cls):
        # Returns the magazine with the most articles or None if there are no articles.
        if not Article.all:
            return None
        
        count_dict = {}
        for article in Article.all:
            mag = article.magazine
            count_dict[mag] = count_dict.get(mag, 0) + 1
        
        if not count_dict:
            return None
            
        top_mag = max(count_dict, key=count_dict.get)
        return top_mag
