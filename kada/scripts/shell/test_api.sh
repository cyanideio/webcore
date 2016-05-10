cd scripts/yaml/
echo '测试影集..'
pyresttest http://localhost:8000/ gallery.yaml
echo '测试服务..'
pyresttest http://localhost:8000/ service.yaml
echo '测试关注关系..'
pyresttest http://localhost:8000/ friend.yaml
