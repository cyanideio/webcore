from django_faker import Faker
# this Populator is only a function thats return a django_faker.populator.Populator instance
# correctly initialized with a faker.generator.Generator instance, configured as above
populator = Faker.getPopulator()

from core.models import Gallery, Scene, SceneTemplate, Photo

populator.addEntity(Gallery, 10, {
    'score':    lambda x: populator.generator.randomInt(0,1000),
    'nickname': lambda x: populator.generator.email(),
})

insertedPks = populator.execute()
