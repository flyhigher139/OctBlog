#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
# from flask.ext.principal import Permission, RoleNeed, UserNeed, identity_loaded
# from flask.ext.login import current_user
from flask_principal import Permission, RoleNeed, UserNeed, identity_loaded
from flask_login import current_user

# admin_need = RoleNeed('admin')
# editor_need = RoleNeed('editor')
# writer_need = RoleNeed('writer')
# reader_need = RoleNeed('reader')
su_need = RoleNeed('su')

su_permission = Permission(su_need)
admin_permission = Permission(RoleNeed('admin')).union(su_permission)
editor_permission = Permission(RoleNeed('editor')).union(admin_permission)
writer_permission = Permission(RoleNeed('writer')).union(editor_permission)
reader_permission = Permission(RoleNeed('reader')).union(writer_permission)


@identity_loaded.connect # Both of this and the following works
# @identity_loaded.connect_via(current_app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'username'):
        identity.provides.add(UserNeed(current_user.username))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'role'):
        # for role in current_user.roles:
        identity.provides.add(RoleNeed(current_user.role))
    
    # if current_user.is_superuser:
    if hasattr(current_user, 'is_superuser') and current_user.is_superuser:
        identity.provides.add(su_need)
        # return current_user.role

    identity.allow_edit = editor_permission.allows(identity)
    identity.allow_admin = admin_permission.allows(identity)
    identity.allow_write = writer_permission.allows(identity)