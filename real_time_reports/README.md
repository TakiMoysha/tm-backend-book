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
