# biuflower
Change check in position of QQ as a chustomized string  
用Python写的自定义QQ签到地点程序
单个py文件
# python版本2.x
# 使用方法
1. 同目录下创建`header.txt`文本文件，将抓取的手机签到数据包的header放入，*不需要*将`Content-Length`字段加入
2. windows用户在当前目录打开命令提示行输入`python biuflower.py`即可，linux用户添加执行权限后可以直接执行。
3. 在gc中填入群号，bkn填入抓取的bkn，poi为自定义地点字符串，点击biu花花执行

# 其他事项
- 另外windows用户可以[直接下载](https://github.com/chinuno-usami/biuflower/releases/)用py2exe打包的可执行文件使用，打开biuhuahua.exe即可
- bkn应该是和cookie对应的，只要cookie不过期bkn应该就不变，把bkn记录下来下次继续使用
- 方法由typcn提供 
