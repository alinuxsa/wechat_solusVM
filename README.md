## 项目目前部署在heroku提供的免费空间

## 这只是个用来练习的项目

## 部分配置参数需要通过环境变量方式导入

**在本机测试，使用shell 导入环境变量 例如** 

```
export WECHAT_TOKEN=abcde
export WECHAT_ENCODING_AES_KEY=abcdef
export WECHAT_CORP_ID=abcdefg
export API_KEY=123-123-123
export API_HASH=12312312312313
export API_URL='https://myvm.hiformance.com/api/client/command.php'
```

企业号需要自己添加按钮 菜单内容均为`点击`

菜单ID 对应列表

| 菜单ID | 内容 | 说明 |
| ----- | ----- | ----- |
| 开机 | boot | vps开机 |
| 关机 | shutdown | vps关机 |
| 重启 | reboot | vps重启 |
| 状态查询 | click001 | 查询状态 |
| 关于| click002 | 说明 |


指令控制服务部分待完成,计划使用paramiko模块，或者使用ansible完成。
