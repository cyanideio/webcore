import os, sys
import django
current_path = os.getcwd()
sys.path.append(current_path)
os.environ["DJANGO_SETTINGS_MODULE"] = "kada.settings"
django.setup()

from autofixture import AutoFixture, generators
from core.models import Gallery


# Ishiyaki
ishiyakiFixture = AutoFixture(Gallery, field_values={
#    'blog': generators.InstanceSelector(
#        Blog,
#        limit_choices_to={'name__ne':"Yoko Ono's blog"})
    'type_kbn': 1,        #Ishiyaki
})
print "inserting data......"
entries = ishiyakiFixture.create(20)

