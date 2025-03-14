# Hierarchy App

## Organization

0. Owner - Full Control
1. Principals - Full Control
2. Admins - View, Edit, Create
3. Developers - View
4. Contributors - View Allowed

## Project

0. Owner - Create, Read, Update, Delete
1. Admins - Create, Read, Update
2. Developers - Read

## Schema

https://dbdiagram.io/d

```
Table users {
  id integer [primary key]
  email email
}

Table organizations {
  id integer [primary key]
  name char[32]
  groups []
  followed_user_id integer
  created_at timestamp
}

Table projects {
  id integer [primary key]
  company_id integer [ref: > organizations.id]
  group_id integer [ref: > groups.id]
}

Table groups {
  id integer [primary key]
  member_id integer [ref: > members.id]
}

Table members {
  id integer [primary key]
  user_id integer [ref: > users.id]
  role_id CompanyRoles
}

enum Employees {
  Owner
  Principal
  Admin
  Developer
  Contributor
}

enum AppRoles {
  Creator
  Moderator
  Developer
}
```

## Проектирование моделей RBAC

Для упрощения проектирования использовать https://play.permify.co/?s=organizations-hierarchies

```
entity user {}

entity organization {

  relation owner @user
  relation manager @user
  relation developer @user
  relation member @user

  permission view_artifact = owner or maanger or (member not agent)
  permission delete_artifact = admin

  permission create_workspace = owner or manager or developer
  permission edit_workspace = owner or manager or developer
}
```

Hierarchical RBAC:

```
entity user {}

entity organization {

    // organizational roles
    relation admin @user
    relation member @user

}

entity application {
    // represents repositories parent organization
    relation parent @organization

    // represents owner of this application
    relation owner  @user

    // permissions
    permission edit   = parent.admin or owner
    permission delete = owner
}
```
