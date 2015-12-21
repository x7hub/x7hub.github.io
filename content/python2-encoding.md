Date: 2015-5-29
Title: Python2字符编码问题小结
Category: Python
Tags: Python, Python2
Slug: python2_encoding

参考：

[Python docs - Unicode HOWTO](https://docs.python.org/2/howto/unicode.html)

[Python docs - Built-in Types](https://docs.python.org/2/library/stdtypes.html)

[Stack Overflow - Why does Python print unicode characters when the default encoding is ASCII?](http://stackoverflow.com/questions/2596714/why-does-python-print-unicode-characters-when-the-default-encoding-is-ascii)

## 理论

### 编码中的Unicode和UTF-8

`Unicode`是字符集，`UTF-8`是`Unicode`的一种编码方式，并列的还包括`UTF-16`、`UTF-32`等。

某个字符的`Unicode`通过查询标准得到，其`UTF-8`编码由`Unicode`码计算得到。


### Python2中的str和unicode

`str`和`unicode`是两个不同的类。

`str`存储的是已经编码后的字节序列，输出时看到每个字节用16进制表示，以`\x`开头。每个汉字会占用3个字节的长度。

```python
>>> a = '啊哈哈'
>>> type(a)
<type 'str'>
>>> a
'\xe5\x95\x8a\xe5\x93\x88\xe5\x93\x88'
>>> len(a)
9
>>> a[2]
'\x8a'
```

`unicode`是“字符”串，存储的是编码前的字符，输出是看到字符以`\u`开头。每个汉字占用一个长度。定义一个`Unicode`对象时，以`u`
开头。

```python
>>> b = u'哟呵呵'
>>> type(b)
<type 'unicode'>
>>> b
u'\u54df\u5475\u5475'
>>> len(b)
3
>>> b[2]
u'\u5475'
```

`str`可以通过`decode()`方法转化为`unicode`对象，参数指明编码方式。

```python
>>> a.decode('utf-8')
u'\u554a\u54c8\u54c8'
```

`unicode`可以通过`encode()`方法转化为`str`对象，参数指明编码方式。

```python
>>> b.encode('utf-8')
'\xe5\x93\x9f\xe5\x91\xb5\xe5\x91\xb5'
```

### 默认编码

Python2中的默认编码，有多个不同的变量。

1. 代码文件开头的`coding`

		# -*- coding: utf-8 -*-

	或

		# coding=utf-8


	指明代码文件中的字符编码，用于代码文件中出现中文的情况。

		% cat hello.py
		#! /usr/bin/env python
		# coding=utf-8
		print '泥壕'
		
		% python hello.py
		泥壕

	如果不设置，默认是`ascii`，当出现中文字符时就不能正常识别。

		% cat hello.py
		#! /usr/bin/env python
		print '泥壕'
		
		% python hello.py
		    File "hello.py", line 2
		SyntaxError: Non-ASCII character '\xe6' in file hello.py on line 2, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details


2. `sys.stdin.encoding`和`sys.stdout.encoding`

	`sdtin`和`stdout`输入输出使用的编码，包命令行参数和`print`输出，由`locale`环境变量决定。

	在`en_US.UTF-8`的系统中，默认值是`UTF-8`。

3. `sys.getdefaultencoding()`

	文件读写和字符串处理等操作使用的默认编码。

	默认值是`ascii`。

## 字符串拼接

`unicode`和`str`类型通过`+`拼接时，输出结果是`unicode`类型，相当于先将`str`类型的字符串通过`decode()`方法解码成`unicode`，再拼接。此时如果解码时没有明确指明编码类型，可能会出现错误。

```python
>>> a = '啊哈哈'
>>> b = u'哟呵呵'
>>>
>>> a + b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe5 in position 0: ordinal not in range(128)
>>>
>>> a.decode('utf-8') + b
u'\u554a\u54c8\u54c8\u54df\u5475\u5475'
```

错误提到`'ascii' codec can't decode byte 0xe5`，这是因为自动将`str`类型的变量按照默认的编码格式`sys.getdefaultencoding()`来解码，默认编码即`ascii`，而这个字符不在`ascii`的范围内，就出现了错误。

```python
>>> import sys
>>> reload(sys)
<module 'sys' (built-in)>
>>> sys.setdefaultencoding('utf-8')
>>>
>>> a = '啊哈哈'
>>> b = u'哟呵呵'
>>> a + b
u'\u554a\u54c8\u54c8\u54df\u5475\u5475'
```



## 文件读取和json解析

读文件得到的结果是`str`类型，以`\x`开头的十六进制表示。

	>>> f = open('t.txt')
	>>> a = f.read()
	>>> a
	'{"hello":"\xe5\x92\xa9"}\n'

而经过json解析后会自动转为`unicode`。

	>>> json.loads(a)
	{u'hello': u'\u54a9'}

## 输出

### 输出到文件

`str`类型可以输出到文件，而`unicode`类型必须先编码成`str`。

```python
>>> a = '啊哈哈'
>>> b = u'哟呵呵'
>>> a
'\xe5\x95\x8a\xe5\x93\x88\xe5\x93\x88'
>>> b
u'\u54df\u5475\u5475'
>>> 
>>> f = open('t.txt', 'w')
>>> f.write(a)
>>> f.write(b)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)
>>> f.write(b.encode('utf-8'))
```

`unicode`输出到文件时的错误是由于默认编码为`ascii`，无法自动完成编码过程。如果将`sys.getdefaultencoding()`编码设置成了`utf-8`就可以自动完成转换过程了。

```python
>>> import sys
>>> reload(sys)
<module 'sys' (built-in)>
>>> sys.setdefaultencoding('utf-8')
>>>
>>> f.write(b)
```


### 计算md5

同样，md5计算也要求输入的`unicode`先编码。

```python
>>> a = '啊哈哈'
>>> b = u'哟呵呵'
>>> import hashlib
>>> hashlib.md5(a).hexdigest()
'f38b302e2993ec3fdad79c4d76074b21'
>>> hashlib.md5(b).hexdigest()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)
>>> hashlib.md5(b.encode('utf-8')).hexdigest()
'c02dc06719bafeaf60505b11d3c0c90a'
```

### 输出到stdout

输出到`stdout`时，默认编码是`sys.stdout.encoding`，默认值取决于系统环境变量，所以`print`输出汉字时才可以不用指定`utf-8`。

```python
>>> import sys
>>> sys.stdout.encoding
'UTF-8'
>>> print u'\u54a9'
咩
```

而在`zh_CN.GB2312`的环境中，默认值不是`utf-8`，就不能正常输出了。

```python
>>> import sys
>>> sys.stdout.encoding
'ANSI_X3.4-1968'
>>> print u'\u54a9'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode character u'\u54a9' in position 0: ordinal not in range(128)
```


## 命令行参数读取

通过`sys.argv`或`argparse`得到的命令行参数都是编码后的`str`类型，以`\x`开头的十六进制表示。可以通过`sys.stdin.encoding`得到命令行传入的编码类型，解码成`unicode`。

```python
#! /usr/bin/env python
# coding = utf-8
import sys

print repr(sys.argv[1])
print sys.stdin.encoding
print repr(sys.argv[1].decode(sys.stdin.encoding))
```

输出结果。

```shell
~/workspace % python hello.py "哇嘿嘿"  
'\xe5\x93\x87\xe5\x98\xbf\xe5\x98\xbf'
UTF-8
u'\u54c7\u563f\u563f'
```

如果命令行环境已经改成`GB2312`等其他编码，python找不到与之匹配的编码类型，就会将默认编码`sys.stdin.encoding`设置成`ascii`，无法通过这种方法正常解码成`unicode`。


## 带\u的字符串转unicode

可能会遇到汉字被转换成unicode编码的形式表示的情况，即一个汉字被表示成了`\u????`的形式。

```python
>>> a = u'咩'
>>> a
u'\u54a9'
>>> b = '\u54a9'
>>> b
'\\u54a9'
```

上述`b`就是这样的情况。此时`b`是一个长度为6的字符串，而不是一个汉字。

要把`b`表示为汉字编码有两种方法。

1. unicode-escape编码。

		>>> unicode(b, 'unicode-escape')
		u'\u54a9'

	或

		>>> b.decode('unicode-escape')
		u'\u54a9'

2. eval拼接。

		>>> eval('u"' + b.replace('"', r'\"')+'"')
		u'\u54a9'
