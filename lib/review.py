from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        pass

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        pass
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
        # Check the dictionary for  existing instance using the row's primary key
        pass
   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        pass

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        pass

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        pass

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        pass

def save(self):
    if self.id is None:
        CURSOR.execute(
            "INSERT INTO reviews (year, summary, employee_id) VALUES (?, ?, ?);",
            (self.year, self.summary, self.employee_id)
        )
        self.id = CURSOR.lastrowid
        self.__class__.all[self.id] = self
    else:
        self.update()
    CONN.commit()

@classmethod
def create(cls, year, summary, employee_id):
    review = cls(year, summary, employee_id)
    review.save()
    return review

@classmethod
def instance_from_db(cls, row):
    review_id, year, summary, employee_id = row
    if review_id in cls.all:
        return cls.all[review_id]
    review = cls(year, summary, employee_id, review_id)
    cls.all[review_id] = review
    return review

@classmethod
def find_by_id(cls, id):
    CURSOR.execute("SELECT * FROM reviews WHERE id = ?;", (id,))
    row = CURSOR.fetchone()
    return cls.instance_from_db(row) if row else None

def update(self):
    CURSOR.execute(
        "UPDATE reviews SET year = ?, summary = ?, employee_id = ? WHERE id = ?;",
        (self.year, self.summary, self.employee_id, self.id)
    )
    CONN.commit()

def delete(self):
    CURSOR.execute("DELETE FROM reviews WHERE id = ?;", (self.id,))
    CONN.commit()
    del self.__class__.all[self.id]
    self.id = None

@classmethod
def get_all(cls):
    CURSOR.execute("SELECT * FROM reviews;")
    rows = CURSOR.fetchall()
    return [cls.instance_from_db(row) for row in rows]

@property
def year(self):
    return self._year

@year.setter
def year(self, value):
    if isinstance(value, int) and value >= 2000:
        self._year = value
    else:
        raise ValueError("Year must be an integer >= 2000")

@property
def summary(self):
    return self._summary

@summary.setter
def summary(self, value):
    if isinstance(value, str) and value.strip():
        self._summary = value
    else:
        raise ValueError("Summary must be a non-empty string")

@property
def employee_id(self):
    return self._employee_id

@employee_id.setter
def employee_id(self, value):
    from lib.models.employee import Employee  # to avoid circular imports
    from lib import CURSOR

    CURSOR.execute("SELECT id FROM employees WHERE id = ?", (value,))
    if CURSOR.fetchone():
        self._employee_id = value
    else:
        raise ValueError("Employee ID must reference a valid Employee in the database")
