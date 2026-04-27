from django.db import models


class PersonManager(models.Manager):
    def filtered(self, age_from, age_to, category, sort, size, page_num):
        query = self.select_related('category').filter(age__gte=age_from, age__lte=age_to)

        if category is not None and category.exists():
            cat_ids = [c.id for c in category]
            query = query.filter(category_id__in=cat_ids)

        if sort == 'name':
            query = query.order_by('name')
        elif sort == 'age':
            query = query.order_by('age', 'name')
        elif sort == 'category':
            query = query.order_by('category__name', 'name')

        offset = (page_num - 1) * size
        return list(query[offset:offset + size])


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'category'

    def __str__(self):
        return self.name


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='people')

    objects = PersonManager()

    class Meta:
        managed = False
        db_table = 'person'
