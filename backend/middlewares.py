# class UnixTimestampMiddleware:
#     def resolve(self, next, root, info, **args):
#         if info.field_name in ('created', 'modified', 'dateJoined', 'lastLogin'):
#             print(dir(info.variable_values))
#             print(info.variable_values)
#             print(dir(info.context))
#         return next(root, info, **args)
