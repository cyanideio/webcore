# def friend_verify_has_key(ori_class):
#     def get_object_list(self, request):
#         same = list(set(request.GET.keys()).intersection(set(self.verify_keys)))
#         for key in self.verify_keys:
#             if not key in same:
#                 return Friend.objects.none()
#         return super(ori_class, self).get_object_list(request)

#     ori_class.get_object_list = get_object_list
#     return ori_class