#!/bin/bash
if [[ $1 = '' ]]; then
	host='http://localhost:8000/'
fi
if [[ $1 = 'local' ]]; then
	host='http://localhost:8000/'
fi
if [[ $1 = 'remote' ]]; then
	host='http://dev.kadashow.com:8000/'
fi
cd scripts/yaml/
echo $host
echo '测试影集..'
pyresttest $host gallery.yaml
echo '测试服务..'
pyresttest $host service.yaml
echo '测试关注关系..'
pyresttest $host friend.yaml
echo '测试评论..'
pyresttest $host comment.yaml
echo '测试消息..'
pyresttest $host message.yaml