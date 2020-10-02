'''
Created on Jul 10, 2020

@author: XHG3
'''
import redis   # 导入redis 模块

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
r = redis.StrictRedis(connection_pool=pool)
print(r.dbsize())
# keys = r.keys()
# r.delete(*keys)
# r.set('food', 'beef')
# r.set('food1', 'prok')
# print(r.get('food'))
# r.set("foo","1")  # 0110001
# r.set("foo1","2")  # 0110010
# r.append("foo1","32")  # 0110010
# print(r.mget("foo","foo1"))  # ['goo1', 'baaanew']
# 
# r.lpush("list1", 'aa', 'ss', 'qa')
# 
# print(r.lrange('list1', 0, -1)) #print the list from first one to last
# print(r.llen("list1"))  # 列表长度
# print(r.lrange("list1", 0, 3))  # 切片取出值，范围是索引号0-3)
# print(r.keys())

# 批量模糊删除keys
# r.delete(*r.keys(pattern='*food*'))
# print(r.keys())
# 删除所有keys
# keys = r.keys()
# r.delete(*keys)

# print(r.keys())
# print(r.dbsize())
# print(r.lrange('Buddy diving', 0, -1))

# # 将数据保存到硬盘中（保存时阻塞）
# r.save()
# 
# # 删除当前数据库所有数据
# r.flushdb()



