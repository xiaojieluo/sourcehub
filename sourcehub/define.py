#错误码定义文件

errors = {
    -1: 'unknow',
    0: 'user not found.',
    1: 'Hello',
    305: 'No effect on updating/deleting a document.',
    401: 'Unauthorized.',
    101: "Object doesn't exist",
    104: 'Missing object id.',
    4112: 'SESSION_TOKEN_EXPIRED',
}



# parser = reqparse.RequestParser()
# parser.add_argument('where', type=str, location="args")
# parser.add_argument('order', type=str, location="args")


# def explode_order(args):
#     order_list = list()
#     if args != None:
#         order_list = args.split(',')
#     return order_list


# def explode_where(where_dict):
#     """处理url中的 where字段，
#     # TODO
#     Arguments:
#         where_dict {[type]} -- [description]

#     Returns:
#         [type] -- [description]
#     """
#     res = {}
#     if where_dict is None:
#         return res
#     where = json.loads(where_dict)

#     for key, value in where.items():
#         # 如果 value 为 dict , 则表示有其他选项参数， 需要进一步处理合并
#         if isinstance(value, dict):
#             # 处理具体到值的时候
#             tmp = ''
#             for k, v in value.items():
#                 # 合并产生新 key 值
#                 tmp = '{}__{}'.format(key, k.strip('$'))
#             res.update({tmp: v})
#             current_app.logger.debug(res)
#             print(res)
#         else:
#             res = where
#     print(res)
#     return res

# class APIResource(Resource):
#     """继承 Resource , 实现 exclude 和 order 等参数过滤器

#     Args:
#         Resource ([type]): [description]
#     """
#     pass