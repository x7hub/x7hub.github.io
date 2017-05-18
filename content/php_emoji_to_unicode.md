Date: 2015-12-17
Title: Emoji表情传输和保存：对非BMP范围的Unicode字符的处理
Category: PHP
Tags: Emoji, Unicode, PHP, Lua
Slug: php_emoji_to_unicode

参考：

[UTF-16](https://en.wikipedia.org/wiki/UTF-16)

[Emoji](https://en.wikipedia.org/wiki/Emoji)

[十分钟搞清字符集和字符编码](http://cenalulu.github.io/linux/character-encoding/)

[4 byte unicode character in Java](http://stackoverflow.com/questions/27287369/4-byte-unicode-character-in-java)

## Emoji与Unicode、UTF8

Emoji是一种特殊的字符，而不是像QQ表情一样的普通字符的转义表示。在Unicode编码中，占用了`U+1F300`到`U+1F64F`中的[部分范围](https://en.wikipedia.org/wiki/Emoji#Unicode_Blocks)。

Emoji字符的特殊之处在于，其使用的Unicode字符超出了通常使用的三字节UTF-8编码的Unicode范围，即BMP范围`U+0000`到`U+FFFF`。按照[UTF-8编码规范](https://en.wikipedia.org/wiki/UTF-8#Codepage_layout)，Emoji字符属于辅助平面范围，通常对应4字节的UTF-8编码。

## Android上Emoji的特殊表示

在Android上显示Emoji出现问题根源在于Java的char长度是两个字节，因此不能直接表示BMP范围外的Unicode字符，包括Emoji。对于BMP范围外的字符，Java没有直接编码的方案，而是[采用一种替代手段](http://stackoverflow.com/questions/27287369/4-byte-unicode-character-in-java)，使用两个char来表示一个字符，称为high surrogate和low surrogate。其中high surrogate使用的是`U+D800`–`U+DBFF`，low surrogate使用的是`U+DC00`-`U+DFFF`，这两个范围都是Unicode编码的保留范围，专门用于表示surrogate字符。

举个栗子，Unicode编码为`U+1F602`的Emoji符号。

![Face With Tears of Joy](https://emojipedia-us.s3.amazonaws.com/cache/3e/a3/3ea3af3cf1f2a75b62bec201c87cd995.png)

在Java中看一下对它的存储和编码：

```java
char[] tear = Character.toChars(0x1F602); // Face with Tears of Joy
final String s = new String(tear);
int length = s.length();
int byteLength = s.getBytes(StandardCharsets.UTF_8).length;
String escape = StringEscapeUtils.escapeJava(s);

Log.i(TAG, "s " + s);
Log.i(TAG, "length " + length);
Log.i(TAG, "byteLength " + byteLength);
Log.i(TAG, "escape " + escape);
```

输出如下：

```logcat
12-18 14:37:11.437 28246-28246/info.x7res.myapplication I/MainActivity: s ��
12-18 14:37:11.437 28246-28246/info.x7res.myapplication I/MainActivity: length 2
12-18 14:37:11.437 28246-28246/info.x7res.myapplication I/MainActivity: byteLength 4
12-18 14:37:11.437 28246-28246/info.x7res.myapplication I/MainActivity: escape \uD83D\uDE02
```

String对象的长度为`2`，编码为UTF-8字节数组后长度为`4`，单个字符unicode-escape编码结果为`\uD83D\uDE02`。因此，虽然Java不能支持直接用单个Unicode字符表示Emoji表情，但是通过使用两个surrogate字符的替代方案也能很好的支持Emoji表情的保存和编码显示。


## Lua对Emoji字符串的处理

Lua的字符串只能是ANSI编码，不支持Unicode字符的字符串。本节下文是在[触动精灵](https://www.zybuluo.com/miniknife/note/148136)框架下，在Android上的Lua解释器测试得到的结论。

在Lua中，一个Emoji字符是6个字节长度，而不是直接UTF-8编码得到的4个字节。这是在Java两个surrogate字符表示一个Emoji字符的基础上，又对这两个surrogate字符进行标准UTF-8编码，得到的6个字节的字符串。

## PHP对Emoji字符的接收和保存

对于Android或者Lua经过urlencode上传的Emoji字符，在服务器的PHP上经过自动的urldecode会得到6个字节长度的2个字符，这里的表现是与Android相匹配的。

问题出现在数据保存，虽然MySQL提供的utf8mb4编码支持4字节的UTF-8字符，但是要做匹配的另一批数据保存到了MongoDB，中文字符保存在成json格式时自动转为了unicode-escape编码，不能支持多字节的UTF-8字符或非BMP的unicode字符。因此为了与其他平台的数据做匹配，要求按照unicode-escape编码数据，即要求将`U+1F602`编码为`\uD83D\uDE02`。

PHP并没有提供Python一样便利的编解码，而且也并不认为现unicode-escape是一种编码格式，因此没有直接encode字符串的方法。对于普通的BMP范围内的字符，比如中文字符，可以通过`json_encode`方法[实现unicode-escape编码](http://stackoverflow.com/questions/7381900/php-decoding-and-encoding-json-with-unicode-characters)，与Python的处理方式类似。

```php
$nickname_unicode = trim(json_encode($nickname), '"');
```

然而，与Python不同的是，PHP(5.6)的`json_encode`方法认为`U+D800`-`U+DFFF`的范围是非法的，不能处理带有上述6字节Emoji符号的字符串，这样会得到空的结果。所以要实现保留字段的unicode-escape编码，需要重写`json_encode`方法。这里参考了[一个开源项目的一部分代码](https://github.com/amekkawi/diskusagereports/blob/master/scripts/inc/json_encode.php)。

重写的`json_encode`代码放在了[我的gist](https://gist.github.com/x7hub/32615114d4a540d64502)，注意与原本的参考代码不同的是，173-175行的`mb_convert_encoding`被注释掉，否则将使用PHP自带的`mb_convert_encoding`方法，对于Unicode保留字符同样不能正常编码。
