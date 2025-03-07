# Real-Time Analytics

### Database

Requires careful consideration of the _data model_, _indexing_, and _query optimization_.
Relational database for real-time analytics must be able to handle high volumes of data, support fast data ingestion and provide newar real-time insights.
_Database Schema_ should be designd to optimize query performance and facilitate fast data retrieval.

- _Real-Time Data Ingestion:_ the ability to continuously ingest data and process it in near real-time is fundamental for real-time analytics.
- _Low Latency Query Processing:_ fast query processing to provide real-time insights.
- _Data Visualization:_ Tools to visualize real-time data and analytics results.
- _Alerting:_ Ability to set up alerts based on predefined conditions to monitor data in real-time.

### Entities and Attributes of Real-Time Analytics

_Entities_ serve as the building blocks of our database, representing the fundamental objects or concepts that need to be stred and managed.
_Attributes_ define the characteristics of each entity, such as its properties, relationships, or behavior.

1. **Event**

- _event_id (primary_key)_ - unique identifier for each event
- _event_type_ - type of event (click, purchase, sign-up)
- _timestamp_ - timestamp of when the event occurred
- _data_ - additional data associated with the event

2. **User**

- _user_id (primary_key)_ - unique identifier for each user
- _username_ - username of the user
- _email_ - email address of the user

3. **Pageview**

- _pageview_id (primary_key)_ - unique identifier for each pageview
- _event_id (Foreign Key referencing Event)_ - event associated with the pageview
- _user_id (Foreign Key referencing User)_ - user associated with the pageview
- _page_url_ - URL of the page visited

4. **Purchase**

- _purchase_id (primary_key)_ - unique identifier for each purchase
- _event_id (Foreign Key referencing Event)_ - event associated with the purchase
- _user_id (Foreign Key referencing User)_ - user associated with the purchase
- _product_id_ - identifier of the purchased product
- _quantity_ - quantity of the product purchased
- _amount_ - total amount of the purchase

### Relationships Between these Entities

1. **Event to User Relationship**

- _One-to-many relationship_: Each event can be associated with one user, but a user can have multiple events.
- _Foreign Key_: The `user_id` column in the `Event` table references the `user_id` column in the `User` table.

2. **PageView to Event Relationship**

- _One-to-many relationship_: Each pageview can be associated with one event, but an event can have multiple pageviews.
- _Foreign Key_: The `event_id` column in the `Pageview` table references the `event_id` column in the `Event` table.

3. **Purchase to Event Relationsihp**

- _One-to-many relations_: Each purchase can be associated with one event, but an event can have multiple purchases.
- _Foreign Key_: The `event_id` column in the `Purchase` table references the `event_id` column in the `Event` table.

### Improve Database Design

- _Normalization_ - ensure the database is normalized to minimize redundancy and dependency;
- _Indexing_ - implement appropriate indexes to speed up query performace;
- _Use Views for Complex Queries_ - Utilize views for complex queries to simplify data retrieval;
- _Maintenance_ - Schedule regular tasks, including vacuuming and indexing;
- _Cahcing_ - implement caching strategies to reduce the load on the database.

### Alembic

**Create migration environment:**
`alembic init alembic` - Create a new directory for Alembic migrations.

Added models to `alembic/env.py` and set up `sqlalchemy_url` file for autogenerate support

For generate migration file, run `alembic revision --autogenerate -m "commit"`.
For apply migration, run `alembic upgrade head`.

## References

1. [How to design a database for real-time analytics / GeeksforGeeks](https://www.geeksforgeeks.org/how-to-design-a-database-for-real-time-analytics/?ref=ml_lbp)
2. [Tutorial / alembic.sqlalchemy.org](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

# Real Time Reporting

- _Reporting Tools and Visualization_
- _Scalability_
- _Alert and Notifications_
- _Data Ingestion and Streaming_
- _Improved Decision Making_
- _Communication and Collaboration_

### Entities and Attributes of Real-Time Reporting

**User**: Represents users of the system.

- id (Primary Key): It is a unique identifier for each user in this user table.
- username: It describes users name for login.
- email: It describes the users email address for communication.

**Report**: Represents different types of reports that can be generated.

- id (Primary Key): It is a unique identifier for each report in this report table.
- subject: It describes the content of the report.
- description: It provides brief description of report.
- user_id: It is a foreign key(references USER_ID in the User entity).

**Transaction**: Represents financial transactions which are relevant to business operations.

- id (Primary key): It is a unique identifier for each transaction in this transaction table.
- user_id: It is a foreign key(references USER_ID in the User entity).
- amount: It describes the financial amount of the transaction.
- status: It describes the current status of the transaction.

**Role**: Represents the roles assigned to users.

- id (Primary Key): It is a unique identifier for each role in this role table.
- role_name: It describes the name of the role.
- description: It provides the brief description of role.

**Data**: Represents the actual data being reported on.

- id (Primary Key): It is a unique identifier for each data in this data table.
- data_type: It describes the type of the data.
- value: It describes the actual value of the data.

**Permission**: Represents the permissions granted to roles for accessing reports.

- id (Primary Key): It is a unique identifier for each permission in this permission table.
- report_id: It is a foreign key(references REPORT_ID in the Report entity).
- role_id: It is a foreign key(references ROLE_ID in the role entity).

### Relationships Between These Entities

**User-Report Relationships**

- It shows the One-to-Many Relationship.
- A User can create multiple Reports.

**Report-User Relationships**

- It shows the Many-to-One Relationship.
- Each Report is associated with one User.

**Data-Report Relationships**

- It shows the One-to-Many Relationship.
- Data is related to Reports.

**User-Transaction Relationships**

- It shows the One-to-Many Relationship.
- One User can generate many Transactions.

**Permission-Role Relationships**

- It shows the Many-to-One Relationship.
- Each Permission is associated with one Role.

**Permission-Report Relationships**

- It shows the Many-to-One Relationship.
- Each Permission is associated with one Report.

**Role-Permission Relationships**

- It shows the One-to-Many Relationship.
- Each Role can have multiple Permissions.

## References

1. [How to design a database for real-time reporting / GeeksforGeeks](https://www.geeksforgeeks.org/how-to-design-a-database-for-real-time-reporting/?ref=ml_lbp)
