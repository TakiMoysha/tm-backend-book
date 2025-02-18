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
