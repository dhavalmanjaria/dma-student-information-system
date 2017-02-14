from django.test import TestCase
from user_management.models.all_permissions import AllPermissions
from user_management.management.commands import initgroups


class ModelRolePermissionsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        global cmd
        cmd = initgroups.Command()

    def testPermsMatchModel(self):
        model_perms = set()
        for p in AllPermissions._meta.permissions:
            model_perms.add(p[0])

        role_perms = set()
        for k, v in initgroups.PERMISSIONS_BY_ROLE.items():
            for p in v:
                role_perms.add(p)

        self.assertEquals(model_perms, role_perms)
