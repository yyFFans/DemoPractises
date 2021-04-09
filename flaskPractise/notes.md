#Flask

* [flash 不显示消息，flash消息需要在模板中进行渲染](https://blog.csdn.net/u010069176/article/details/52230320)
* flash消息 必须先设置 SECRET_KEY 为什么，防止伪造该站上的已登录用户
  "The session is unavailable because no secret "
  
        Flask中有个配置属性叫做SECRET_KEY

        其作用是：

        Flask（以及相关的扩展extension）需要进行加密

        所以需要这个密钥SECRET_KEY

        －》之所以需要加密，是因为有些涉及到安全的东西，需要加密

        －》这些东西包括：

        Flask本身相关的有：

        session
        其它一些第三方的库相关的有：

        Flask-Images（内部可能是图片处理用到的）
        Cookies相关的
        Flask-WTF的CSRF保护

* 表单示例用例中使用redirect避免出现刷新时浏览器重复上次提交的动作的理解
```pythion
Example 4-5. hello.py: Redirects and user sessions
from flask import Flask, render_template, session, redirect, url_for
@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'))
```
  点击submit按钮时会触发POST请求，调用index, validate_on_submit()返回true，由redirect函数再次触发GET请求index页面，调用index函数，validate_on_submit()返回false，最后调用render_template 刷新页面。
  刷新浏览器页面，会重新触发上一次的请求，不使用redirect会重新触发POST，出现浏览器提示重复提交表单数据；使用redirect后，由redirect触发了一次GET请求，刷新浏览器是触发的是GET请求，避免此重复提交错误，从debug日志也可以看出，点击提交按钮后，在POST后，有一次GET
127.0.0.1 - - [14/Jun/2020 11:13:19] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [14/Jun/2020 11:13:31] "POST / HTTP/1.1" 302 -
127.0.0.1 - - [14/Jun/2020 11:13:31] "GET / HTTP/1.1" 200 -

* 模板引擎使用理解
```
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block title %}Flasky{% endblock %}
{% block page_content %}
<div class="page-header">
  <h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
</div>
{{ wtf.quick_form(form) }}
{% endblock %}
```
```
{# bootstrap/wtf.html  quick_from #}
{% macro quick_form(form,
                    action="",
                    method="post",
                    extra_classes=None,
                    role="form",
                    form_type="basic",
                    horizontal_columns=('lg', 2, 10),
                    enctype=None,
                    button_map={},
                    id="",
                    novalidate=False) %}
......
{%- endmacro %}
```
`extends` 用于扩展已有模板，同名block块内容替换，即如果base.html中存在block title、page_content,则会被上面对应块内容所替换
`import xx as xxx` 用于引入某个模板文件，从而可以使用模板中的函数，wtf.quick_form，调用了所引用模板中的quick_from 宏，模板中用`macro`来定义，类似于函数功能;import 必须与as一起使用，不能单独使用
`include` 会将所引用文件内容全部包含进来
模板引擎中**关键字** 都被`{% keyWord %}`这种形式包裹

* 蓝图blueprint机制 简单理解
  蓝图描绘了应用的视图结构，即View中路由信息；真正绑定生效到应用是在应用注册蓝图时；
  蓝图机制带来的另一好处是不同蓝图下的路由函数可以同名，不会冲突
