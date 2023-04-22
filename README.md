# ssh-sftp-processor
ssh 远程主机数据上传下载

依赖:
* `pip install paramiko`

## 运行
1. 在根目录下创建 config.ini:
类似:
```ini
[remote]
ssh_host=106.75.143.56
ssh_port=22
ssh_user=***
ssh_pass=***

```
2. 然后运行:
```python
python main.py
```