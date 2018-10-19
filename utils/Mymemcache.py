import memcache

# 连接memcache 也支持分布式
mc = memcache.Client(['127.0.0.1:11211'], debug=True)

# 封装几个常用方法 set/get/delete/ 判断key唯一

# 设置
def set_key(key=None, value=None, time=60):
    if key and value:
        mc.set(key=key, val=value, time=time)
        return True
    return False


# 获取
def get_key(key=None):
    if key:
        return mc.get(key)
    return None

# 删除
def delete_key(key=None):
    if key:
        mc.delete(key=key)
        return True
    return False