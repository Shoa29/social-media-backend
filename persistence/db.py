import mysql.connector

class SocialStorage(object):
  def __init__(self):
    """
    Initializing Mysql DB Connection
    """
    self.mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="dreams",
      database="Social_Listed"
    )
    self.cursor = self.mydb.cursor()
    self.mydb.commit()

  def createUserTable(self):
    """
    Create table for users if does not exist
    :return:
    """
    self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, UNIQUE(username))")
    self.mydb.commit()

  def createConnectionsTable(self):
    """
    Create table for user friend requests if does not exist
    :return:
    """
    self.cursor.execute("CREATE TABLE IF NOT EXISTS connections (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), friend VARCHAR(255), pending INT)")
    self.mydb.commit()

  def createUsers(self, username):
    """
    Creates new user
    :param username: unique username
    :return: error or success response
    """
    self.createUserTable()
    sql = "SELECT * FROM users WHERE username = %s"
    val = (username,)
    self.cursor.execute(sql, val)
    if self.cursor.fetchone():
      return 400
    else:
      sql = "INSERT INTO users (username) VALUES (%s)"
      self.cursor.execute(sql, val)
      self.mydb.commit()
      return 201

  def connectFriends(self, user, friend):
    """
    Function to connect friend requests to users
    :param user:
    :param friend:
    :return: error or success response
    """
    self.createConnectionsTable()
    sql = "SELECT * FROM users WHERE username = %s"
    val = (user,)
    self.cursor.execute(sql, val)
    res = self.cursor.fetchone()
    sql = "SELECT * FROM users WHERE username = %s"
    val = (friend,)
    self.cursor.execute(sql, val)
    res1 = self.cursor.fetchone()
    if res is None or res1 is None:
      return 404
    sql = "SELECT * FROM connections WHERE username = %s AND friend = %s"
    val = (user, friend)
    self.cursor.execute(sql, val)
    res = self.cursor.fetchone()
    if res:
      return 400
    sql = "SELECT * FROM connections WHERE username = %s AND friend = %s"
    val = (friend, user)
    self.cursor.execute(sql, val)
    res = self.cursor.fetchone()
    if res:
      pending = 0
      sql = "UPDATE connections SET pending = %s WHERE username = %s"
      val = (pending, friend)
      self.cursor.execute(sql, val)
      self.mydb.commit()
    else:
      pending = 1
    sql = "INSERT INTO connections (username, friend, pending) VALUES (%s, %s, %s)"
    val = (user, friend, pending)
    self.cursor.execute(sql, val)
    self.mydb.commit()
    return 200

  def getFriends(self, username):
    """
    Get List of Friends of a user
    :param username: unique username
    :return: list of friends
    """
    sql = "SHOW TABLES LIKE 'connections'"
    self.cursor.execute(sql)
    res = self.cursor.fetchone()
    if res:
      sql = "SELECT * FROM users WHERE username = %s"
      val = (username,)
      self.cursor.execute(sql, val)
      if self.cursor.fetchone() is None:
        return 400
      sql = "SELECT friend FROM connections WHERE username = %s AND pending = %s"
      val = (username,0)
      self.cursor.execute(sql, val)
      friends = self.cursor.fetchall()
      if friends:
        return list(friends)
      else:
        return 404
    else:
      return 400




