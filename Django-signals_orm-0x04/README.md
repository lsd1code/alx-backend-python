# Self referential foreign key

- Foreign key field within a model that points back to the same model
- This allows you to model hierarchical or recursive relationships where instances of a model can be related to other instances in the model

```python
class Model(model.Model):
    field1 = models.CharField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
```

- `on_delete` argument: this must be specified on every `ForeignKey()` method

- `blank=True(form) & null=True(db)`: this allows the field to be optional(nullable)

# `select_related`

-

# `prefetch_related`

- returns a queryset that will automatically retrieve, in a single batch, related objects for each of the specified lookups
- designed to stop the deluge of DB queries that are performed 

# `Custom Manager`

- Provides a way to encapsulate database queries and add `table-level` functionality to your models
- Custom managers allow you to define custom methods within your manager to perform common or complex queries that apply to entire model 