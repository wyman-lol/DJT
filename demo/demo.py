import memcache

# 连接memcache 也支持分布式
mc = memcache.Client(['127.0.0.1:11211'], debug=True)
mc.set('luwei', 'age18', 60)

mc.delete('luwei')
print(mc.get('luwei'))