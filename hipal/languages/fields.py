from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderOfField(models.PositiveIntegerField):
    """This is a class for custom order of fields"""
    def __init__(self, for_fields=None, *args, **kwargs):
        """Initliaze the fields"""
        self.for_fields = for_fields
        super().__init__(*args,**kwargs)
        
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                queryset = self.model.objects.all()
                if self.for_fields:
                    # filtering by objects with the same field values for the fields in "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    queryset = queryset.filter(**query)
                    # get the order of the last item
                    last = queryset.latest(self.attname)
                    value = last.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)