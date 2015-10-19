from flask import current_app
from flask.ext.principal import Permission, RoleNeed, identity_loaded

admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))
author_permission = Permission(RoleNeed('author'))
reader_permission = Permission(RoleNeed('reader'))


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))