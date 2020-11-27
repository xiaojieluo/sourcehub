## 注册
注册一个新用户与创建一个新的普通对象之间的不同点在于 username 和 password 字段都是必需的。
password 字段会以和其他的字段不一样的方式处理，它在储存时会被加密而且永远不会被返回给任何来自客户端的请求。

<!-- 你可以让 LeanCloud 自动验证邮件地址，做法是进入 控制台 > 存储 > 设置 > 用户账号，勾选 用户注册时，发送验证邮件。 -->

<!-- 这项设置启用了的话，所有填写了 email 的用户在注册时都会产生一个 email 验证地址，并发回到用户邮箱，用户打开邮箱点击了验证链接之后，用户表里 emailVerified 属性值会被设为 true。你可以在 emailVerified 字段上查看用户的 email 是否已经通过验证。
+ -->

<!-- 你还可以在 控制台 > 存储 > 设置 > 用户账号，勾选未验证邮箱的用户，禁止登录。 -->

为了注册一个新的用户，需要向 user 路径发送一个 POST 请求，你可以加入一个新的字段，例如，创建一个新的用户有一个电话号码:

```bash
curl -X POST \
  -H "X-SH-Id: {{x_sh_id}}" \
  -H "X-SH-Key: {{x_sh_key}}" \
  -H "Content-Type: application/json" \
  -d '{"username":"hjiang","password":"f32@ds*@&dsa","phone":"18612340000"}' \
  https://API_BASE_URL/1.1/users
```